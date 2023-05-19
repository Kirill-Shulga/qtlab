import os
import sys
import logging
import runpy

basedir = "C:/qtlab_replacement"
_execdir = basedir
sys.path.append(os.path.abspath(os.path.join(basedir, 'src')))
sys.path.append(os.path.abspath(os.path.join(basedir, 'scripts')))
sys.path.append(os.path.abspath(os.path.join(basedir, 'instruments')))
sys.path.append(basedir)

import setup_logging
#from init_instruments import *
#def execfile(filename):
#	exec(compile(open(filename, "rb").read(), filename, 'exec'), globals(), locals())
#execfile('src/setup_logging.py')
#execfile('init_instruments.py')