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

################################
# setup logging                #
################################
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers: 
    # add a stream handler if there are no current handlers for this logging instance
    _console = logging.StreamHandler()
    _console.setLevel(logging.INFO)
    _formatter = logging.Formatter('%(levelname)-10s %(message)s')
    _console.setFormatter(_formatter)
    logger.addHandler(_console)

def setLoggingLevel(level):
    '''
    Set the logging level for this module.
    Valid levels are: NOTSET, DEBUG, INFO, WARNING, ERROR, and CRITICAL
    '''
    kLoggingLevels = {'DEBUG': logging.DEBUG,
                      'INFO': logging.INFO,
                      'WARNING': logging.WARNING,
                      'ERROR': logging.ERROR,
                      'CRITICAL': logging.CRITICAL,
                      'NOTSET' : logging.NOTSET}
    try:
        level = level.upper()
        logger.setLevel(kLoggingLevels[level])
        for handler in logger.handlers:
            handler.setLevel(kLoggingLevels[level])
    except KeyError:
        raise Exception("Can not set level. '%s' is invalid level" % level)

################################
# set up decorators            #
################################
def decorated(origFunc, newFunc, decoration=None):
    """
    Copies the original function's name/docs/signature to the new function, so that the docstrings
    contain relevant information again. 
    Most importantly, it adds the original function signature to the docstring of the decorating function,
    as well as a comment that the function was decorated. Supports nested decorations.
    """
    if not hasattr(origFunc, '_decorated'):
        # a func that has yet to be treated - add the original argspec to the docstring
        import inspect
        newFunc.__doc__ = "Original Arguments: %s\n\n%s" % (
            inspect.formatargspec(*inspect.getargspec(origFunc)), 
            inspect.getdoc(origFunc) or "")
    else:
        newFunc.__doc__ = origFunc.__doc__ or ""
    newFunc.__doc__ += "\n(Decorated by %s)" % (decoration or "%s.%s" % (newFunc.__module__, newFunc.__name__))
    newFunc.__name__ = origFunc.__name__
    newFunc.__module__ = origFunc.__module__
    newFunc.__dict__ = origFunc.__dict__    # share attributes
    newFunc._decorated = True   # stamp the function as decorated

def decorator(func):
    """
    Decorator for decorators. Calls the 'decorated' function above for the decorated function, to preserve docstrings.
    """
    def decoratorFunc(origFunc, *x):
        args = (origFunc,) + x
        if x:
            origFunc = x[0]
        newFunc = func(*args)
        decorated(origFunc, newFunc, "%s.%s" % (func.__module__, func.__name__))
        return newFunc
    decorated(func,decoratorFunc, "%s.%s" % (__name__, "decorator"))
    return decoratorFunc