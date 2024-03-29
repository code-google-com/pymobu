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

Google code project page:
http://code.google.com/p/pymobu/

Supported MB versions:
2010
'''
import sys
from cStringIO import StringIO

from pyfbsdk import FBSystem
from pythonidelib import GenDoc

from datatypes import insertMathClasses
from core import *
from components import *

__version__ = '0.1'
__author__ = "Scott Englert - scott@scottenglert.com"

__MBVersion__ = FBSystem().Version

insertMathClasses()

################################
# set up help                  #
################################
_stdout = sys.stdout
def help(topic):
    '''Creates a window that displays help information'''
    from pyfbsdk import FBAddRegionParam, FBAttachType, FBMemo, ShowTool
    from pyfbsdk_additions import CreateUniqueTool
    
    win = CreateUniqueTool('Help')
    win.StartSizeX = 400
    win.StartSizeY = 500
    
    helpText = FBMemo()
    
    x = FBAddRegionParam(0, FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(0, FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0, FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(0, FBAttachType.kFBAttachBottom,"")
    
    win.AddRegion("helpText", "helpText", x, y, w, h)

    win.SetControl("helpText", helpText)
    
    ShowTool(win)
    
    try:
        sys.stdout = StringIO()
        GenDoc(topic)
        helpText.Text = sys.stdout.getvalue()
    finally:
        sys.stdout = _stdout
    