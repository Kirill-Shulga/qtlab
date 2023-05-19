from instrument import Instrument
from matplotlib import pyplot as plt
import pyvisa as visa
import types
import logging
from time import sleep
import numpy

class American_Magnetics_430(Instrument):

	def __init__(self, name, address, **kwargs):
		"""
		Initializes the device.
		"""
		try:
			logging.info(__name__ + ' : Initializing instrument American Magnetics Magnet 430')
			Instrument.__init__(self, name, tags=['physical'])
		
			self.name = name
			self._address = address
        
			rm = visa.ResourceManager()
			self._visainstrument = rm.open_resource(self._address, read_termination='\r\n')
		
			field = float(self._visainstrument.query("FIELD:UNITS?"))
			rate = float(self._visainstrument.query("RAMP:RATE:UNITS?"))
			if (field == 1 and rate == 0):
				print ("Units are T/sec")
			else:
				print ("Units are NOT T/sec. Proceed with caution")
		except:
			#self.statusStr("An error has occured. Cannot initialize AMI Model 430.")
			print(field, rate)
			print ("An error has occured. Cannot initialize AMI Model 430.")
            
		self.add_function("get_id")
        
	def get_id(self):
		'''Get basic info on device'''
		return self._visainstrument.query("*IDN?")

	def canstartramp(self):
		if float(self._visainstrument.query("QU?")) == 1: #check for quench
			print ("Could not ramp due to quench")
			return False
            
		state = self.get_rampingstate()
		if state == 1:
			print ("YOU ARE ALREADY RAMPING")
			return False
		elif state == 2 or 3 or 8:
			return True
		return False

	def ramp_field(self, value):
		"""
		Ramp to a certain field
		"""
		if not self.canstartramp():  
			return 'cannot start ramping yet'
        
		# Check we aren't violating field limits
		field_lim = self.get_fieldlim()
		if abs(value) > field_lim:
			return 'Field limit exceeded'
        # Then, do the actual ramp
        # Set the ramp target
		self._visainstrument.write("CONF:FIELD:TARG %f" % value)
		self._visainstrument.write("RAMP")
		state = float(self.get_rampingstate())
		while state == 1:
			state = float(self._visainstrument.query("STATE?"))
			sleep(0.3)
			sleep(2.0)
			
		# If we are now holding, it was successful
		if state != 2:
			return 'setField failed.'
            
	def get_rampingstate(self):
		results = self._visainstrument.query("STATE?")     
		return results

	def get_currentlimit(self):
		results = self._visainstrument.query("CURR:LIM?")
		return float(results)
        
	def get_voltagelimit(self):
		results = self._visainstrument.query("VOLT:LIM?")
		return float(results)
        
	def get_fieldlim(self):
		field_lim = float(self._visainstrument.query("COIL?"))*self.get_currentlimit()
		return float(field_lim)
        
	def get_field(self): #this is the current field
		results = self._visainstrument.query("FIELD:MAG?")
		return float(results)
 
	def get_fieldsetpoint(self): #this is the current field
		results = self._visainstrument.query("FIELD:TARG?")
		return float(results)
  
	def get_current(self): #this is the current ... current?
		results = self._visainstrument.query("CURRENT:MAG?")
		return float(results)

	def get_currentsetpoint(self): #this is the current field
		results = self._visainstrument.query("CURR:TARG?")
		return float(results)
        
	def get_ramprate(self):
		""" Return the ramp rate of the first segment in Tesla per second """
		results = self._visainstrument.query('RAMP:RATE:FIELD:1?').split(',')
		return float(results[0])
        
	def set_currentlimit(self, value):
		if value > 84: #Maximum current amplitude in AMI (xy) split coil
			return "That current limit exceeds value on AMI datasheet"
		self._visainstrument.write("CONF:CURR:LIM %f" % value)        
		return

	def set_voltagelimit(self, value):
		self._visainstrument.write("CONF:VOLT:LIM %f" % value)        
		return         
            
	def set_ramprate(self, rate):
		""" Set the ramp rate of the first segment in Amperes per second """
		if rate > 0.290*float(self._visainstrument.query("COIL?")): #current ramp limit of AMI (xy) split coil in Amps/sec
			return "The rate is TOO HIGH!"
		self._visainstrument.write("CONF:RAMP:RATE:SEG 1")
		self._visainstrument.write("CONF:RAMP:RATE:FIELD 1,%f,0" % rate)