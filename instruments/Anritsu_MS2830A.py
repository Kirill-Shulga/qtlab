from instrument import Instrument
import pyvisa as visa
import types
import logging
from time import sleep
import numpy

class Anritsu_MS2830A(Instrument):
    '''
    This is the driver for the Anritsu MS2830A Signal Analizer

    Usage:
    Initialize with
    <name> = instruments.create('<name>', 'Anritsu_MS2830A', address='<GBIP address>, reset=<bool>')
    '''

    def __init__(self, name, address, reset=False):
        '''
        Initializes the Anritsu_MS2830A, and communicates with the wrapper.

        Input:
          name (string)    : name of the instrument
          address (string) : GPIB address
          reset (bool)     : resets to default values, default=False
        '''
        logging.info(__name__ + ' : Initializing instrument Agilent_E8257D')
        Instrument.__init__(self, name, tags=['physical'])

        # Add some global constants
        self._address = address
        self._visainstrument = visa.ResourceManager().open_resource(self._address)

        self.add_parameter('startfreq', type=float,
			flags=Instrument.FLAG_GETSET,
			minval=9e6, maxval=26.5e9,
			units='Hz', tags=['sweep'])			
			
        self.add_parameter('stopfreq', type=float,
			flags=Instrument.FLAG_GETSET,
			minval=9e6, maxval=26.5e9,
			units='Hz', tags=['sweep'])						
			
        self.add_parameter('span', type=float,
			flags=Instrument.FLAG_GETSET,
			minval=0, maxval=26.5e9,
			units='Hz', tags=['sweep'])	
            
        self.add_parameter('bandwidth', type=float,
			flags=Instrument.FLAG_GETSET,
			minval=1, maxval=3e6,
			units='Hz', tags=['sweep'])	
            
        self.add_parameter('video_bw', type=float,
            flags=Instrument.FLAG_GETSET,
            minval=0, maxval=1e9,
            units='Hz', tags=['sweep']) 
            
        self.add_parameter('centerfreq', type=float,
            flags=Instrument.FLAG_GETSET,
            minval=0, maxval=20e9,
            units='Hz', tags=['sweep'])

        self.add_parameter('nop', type=int,
			flags=Instrument.FLAG_GETSET,
			minval=11, maxval=30001,tags=['sweep'])            
            
        self.add_parameter('averages', type=int,
			flags=Instrument.FLAG_GETSET,
			minval=2, maxval=9999,tags=['sweep']) 

        self.add_parameter('frequency',
            flags=Instrument.FLAG_GETSET, units='Hz', minval=9e6, maxval=26.5e9, type=float, tags=['sweep'])
            
        self.add_parameter('continuous_mode', type=bool, flags=Instrument.FLAG_GETSET)

        self.add_function('reset')
        self.add_function ('get_all')
        self.add_function('get_freqpoints')
        self.add_function('get_tracedata')
        self.add_function('get_sweep_time')
        self.add_function('set_sweep_time')
        self.add_function('set_marker_freq')
        self.add_function('set_marker_zone_width')
        self.add_function('set_marker_integration_type')
        self.add_function('get_marker_value')

        if (reset):
            self.reset()
        else:
            self.get_all()

    def reset(self):
        '''
        Resets the instrument to default values

        Input:
            None

        Output:
            None
        '''
        logging.info(__name__ + ' : resetting instrument')
        self._visainstrument.write('*RST')
        self.get_all()

    def get_all(self):

        logging.info(__name__ + ' : get all')
        #self.get_power()
        #self.get_phase()
        self.get_frequency()

    def do_get_frequency(self):

        logging.debug(__name__ + ' : get central frequency')
        return float(self._visainstrument.query('FREQ:CENT?'))

    def do_set_frequency(self, freq):

        logging.debug(__name__ + ' : set frequency to %f' % freq)
        self._visainstrument.write('FREQ:CENT %f' % freq)
        
    def do_get_averages(self):

        logging.debug(__name__ + ' : get start frequency')
        return float(self._visainstrument.query('AVER:COUN?'))

    def do_set_averages(self, averages):

        logging.debug(__name__ + ' : set averages to %f' % averages)
        self._visainstrument.write('AVER:COUN %f' % averages) 
        
    def do_get_startfreq(self):

        logging.debug(__name__ + ' : get start frequency')
        return float(self._visainstrument.query('FREQ:STAR?'))

    def do_set_startfreq(self, freq):

        logging.debug(__name__ + ' : set start frequency to %f' % freq)
        self._visainstrument.write('FREQ:STAR %f' % freq)     
        
    def do_get_nop(self):

        logging.debug(__name__ + ' : get stop frequency')
        return float(self._visainstrument.query('SWE:POIN?'))

    def do_set_nop(self, nop):

        logging.debug(__name__ + ' : set stop frequency to %f' % nop)
        self._visainstrument.write('SWE:POIN %f' % nop)   
        
    def do_get_stopfreq(self):

        logging.debug(__name__ + ' : get number of points')
        return float(self._visainstrument.query('FREQ:STOP?'))

    def do_set_stopfreq(self, freq):

        logging.debug(__name__ + ' : set number of points to %f' % freq)
        self._visainstrument.write('FREQ:STOP %f' % freq)  
        
    def do_set_centerfreq(self, freq):
        logging.debug(__name__ + ' : setting center frequency to  %s' % freq)
        self._visainstrument.write('FREQ:CENT %f' % freq)  

    def do_get_centerfreq(self):
        logging.debug(__name__ + ' : get center frequency')
        return float(self._visainstrument.query('FREQ:CENT?'))  

    def do_get_span(self):
        logging.debug(__name__ + ' : get central frequency')
        return float(self._visainstrument.query('FREQ:SPAN?'))

    def do_set_span(self, span):
        logging.debug(__name__ + ' : set span to %f' % span)
        self._visainstrument.write('FREQ:SPAN %f' % span)
        
    def do_get_bandwidth(self):
        logging.debug(__name__ + ' : get bandwidth')
        return float(self._visainstrument.query('BAND?'))

    def do_set_bandwidth(self, band):
        logging.debug(__name__ + ' : set bandwidth to %f' % band)
        self._visainstrument.write('BAND %f' % band)
        
    def do_get_video_bw(self):
        logging.debug(__name__ + ' : get video bandwidth')
        return float(self._visainstrument.query('BAND:VID?'))

    def do_set_video_bw(self, band):
        logging.debug(__name__ + ' : set video bandwidth to %f' % band)
        self._visainstrument.write('BAND:VID %f' % band)
        
    def get_sweep_time(self):
        logging.debug(__name__ + ' : Get the time needed for one sweep')
        return float(self._visainstrument.query('SWE:TIME?'))*1e3

    def set_sweep_time(self, t):
        logging.debug(__name__ + ' : set the time needed for one sweep to %f' % t)
        self._visainstrument.write('SWE:TIME %f' % t)       
        
  
    def do_get_trace(self, span):
        logging.debug(__name__ + ' : get central frequency')
        return float(self._visainstrument.query('FREQ:SPAN?'))  
        
    def do_calibration(self):
        logging.debug(__name__ + ' : full calibration')
        self._visainstrument.write('CAL:ALL')    

    def do_get_temperature(self, span):
        logging.debug(__name__ + ' : get the temperature when the last time all the calibrations were performed. ')
        return float(self._visainstrument.query('CAL:TEMP:ALL? '))  
     
    def get_tracedata(self):
        sleeptime = self.get_sweep_time()/1e3
        self._visainstrument.write('INIT:SWP')
        #self._visainstrument.query('*WAI')
        sleep(sleeptime*1.5)
        data = self._visainstrument.query('TRAC? TRAC1').split(',')
        for point_id, point_value in enumerate(data):
            data[point_id] = float(point_value)
        return data

    def get_freqpoints(self):
        self._start = self.get_startfreq()
        self._stop = self.get_stopfreq()
        self._nop = self.get_nop()
        self._freqpoints = numpy.linspace(self._start,self._stop,self._nop)
        return self._freqpoints
        
    def do_set_continuous_mode(self, mode):
        logging.debug(__name__ + ' : set continuous_mode to %s' % mode)
        self._visainstrument.write('INIT:CONT %s' % int(mode))
		
    def do_get_continuous_mode(self):
        logging.debug(__name__ + ' : get continuous mode status')
        stat = self._visainstrument.ask('INIT:CONT?')
        
    def set_marker_freq(self, freq, marker):
        logging.debug(__name__ + ' : set marker frequency to %s' % freq)
        self._visainstrument.write('CALC:MARK%s:X %s' %(int(marker),int(freq)))

    def set_marker_zone_width(self, width, marker):
        logging.debug(__name__ + ' : set marker zone witdh to %s' % width)
        self._visainstrument.write('CALC:MARK%s:WIDT %s' %(int(marker),int(width)))
        
    def set_marker_integration_type(self, types):
        '''
        INTegration Total Power in the zone band
        DENSity Power per 1 Hz in the zone band
        PEAK Peak power in the zone
        '''
        logging.debug(__name__ + ' : set marker integration type to %s' % types)
        self._visainstrument.write('CALC:MARK:RES %s' %(types))
        
    def get_marker_value(self, marker):
        return float(self._visainstrument.query('CALC:MARK%s:Y?' %(int(marker))))
        
    def set_detector(self, detector_type):	
        if detector_type == 'rms':
            self._visainstrument.write('DET:TRAC AVER')
            self._visainstrument.write('AVER:TYPE RMS')
        else:
            self._visainstrument.write('DET:TRAC {0}'.format(detector_type))
            #raise(ValueError('QtLab driver only support setting rms detector.'))