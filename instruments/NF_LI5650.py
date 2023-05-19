from instruments.instrument import Instrument
import pyvisa as visa
import types
import time
import logging
import numpy
import sys

class NF_LI5650(Instrument):

    def __init__(self, name, address):
        logging.info(__name__ + ' : Initializing instrument LI5650 NF Lock In Amplifier')
        Instrument.__init__(self, name, tags=['physical'])
        
        self.name = name
        self.address = address
        
        self.instrument = None
        
#--------------------------------------------------------------------------
# frequently used fuctions
        
    def make_connection(self):
        rm = visa.ResourceManager()
        try:
            self.instrument = rm.open_resource(self.address)
            print('connection to ' + self.name )
            print('*IDN? ', self.instrument.query("*IDN?"))
        except:
            print('connection to ' + self.name +' faild.' )


    def read_outp_in_string(self):
        voltage = self.instrument.query(':FETC?') 
        return voltage

    def read_outp_in_ascii(self):
        voltage = self.instrument.query_ascii_values(":FETC?")   
        return voltage
        
    def set_IntOsc_frequency(self, freq, unit):
        command = "SOUR:FREQ " + str(freq) + unit
        freq = self.instrument.write(command)   
  
    def get_IntOsc_frequency(self):
        readfreq = self.instrument.query_ascii_values(":SOUR:FREQ?")    
        return readfreq
  
    
    def set_IntOsc_amp(self, amp):
        command = "SOUR:VOLT " + str(amp)
        freq = self.instrument.write(command)   
  
    def get_IntOsc_amp(self):
        readamp = self.instrument.query_ascii_values(":SOUR:VOLT?")    
        return readamp
        
    def get_timeconstant(self):
        return self.instrument.query_ascii_values(":FILT:TCON?")
        
    def set_timeconstant(self, time):
        command = ":FILT:TCON " + str(time)
        freq = self.instrument.write(command)
        
    def get_slope(self):
        return self.instrument.query_ascii_values(":FILT:SLOP?")
    
    def set_slope(self, attenuation):
        command = ":FILT:SLOP " + str(attenuation)
        freq = self.instrument.write(command)
        
    def set_offset_Auto(self):
        return self.instrument.write(":CALCulate1:OFFSet:AUTO:ONCE")
        
    def set_offset_ON(self):
        return self.instrument.write(":CALC1:OFFS:STAT 1")
    
    def set_offset_OFF(self):
        return self.instrument.write(":CALC1:OFFS:STAT 0")
        
    def get_multiplier(self):
        return self.instrument.query_ascii_values(":CALC1:MULT?")
        
    def set_multiplier(self, multiplier):
        command = ":CALC1:MULT " + str(multiplier)
        freq = self.instrument.write(command)
        
    def get_sensitivity(self):
        return self.instrument.query_ascii_values(":CURR:AC:RANG?")
        
    def set_sensitivity(self, current):
        command = ":CURR:AC:RANG " + str(current)
        freq = self.instrument.write(command)
        
    def set_phase_Auto(self):
        return self.instrument.write(":PHAS:AUTO:ONCE")
        
