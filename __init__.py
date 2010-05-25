# PyMoBu - Python enhancement for Autodesk's MotionBuilder
# Copyright (C) 2010  Scott Englert
# scott@scottenglert.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
PyMoBu

An enhancement for Autodesk's MotionBuilder Python implementation.
PyMoBu offers stronger and more user-friendly object classes and
functions that wrap around existing MotionBuilder objects.

It is easy to convert your existing object to a PyMoBu one by
calling the 'ConvertToPyMoBu' method on that object. 

Supported MB versions:
2010
'''
import logging
from pyfbsdk import FBSystem
from datatypes import insertMathClasses
from core import *
from components import *

__version__ = '0.1'
__author__ = "Scott Englert - scott@scottenglert.com"

__MBVersion__ = FBSystem().Version

insertMathClasses()

#################################
## setup logging                #
#################################
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
#if not logger.handlers: 
#    # add a stream handler if there are no current handlers for this logging instance
#    _console = logging.StreamHandler()
#    _console.setLevel(logging.INFO)
#    _formatter = logging.Formatter('%(levelname)-10s %(message)s')
#    _console.setFormatter(_formatter)
#    logger.addHandler(_console)
#
#def setLoggingLevel(level):
#    '''
#    Set the logging level for this module.
#    Valid levels are: NOTSET, DEBUG, INFO, WARNING, ERROR, and CRITICAL
#    '''
#    kLoggingLevels = {'DEBUG': logging.DEBUG,
#                      'INFO': logging.INFO,
#                      'WARNING': logging.WARNING,
#                      'ERROR': logging.ERROR,
#                      'CRITICAL': logging.CRITICAL,
#                      'NOTSET' : logging.NOTSET}
#    try:
#        level = level.upper()
#        logger.setLevel(kLoggingLevels[level])
#        for handler in logger.handlers:
#            handler.setLevel(kLoggingLevels[level])
#    except KeyError:
#        raise Exception("Can not set level. '%s' is invalid level" % level)

################################
# set up help                  #
################################