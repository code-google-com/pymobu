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
Module for more general functions
'''
import re
from pyfbsdk import *

# get the whole list of components
kAllSceneComponents = FBSystem().Scene.Components

def deselect(pattern=None, **kwargs):
    '''
    Deselects objects that match the given parameters
    See ls function for available arguments
    '''
    kwargs['selected'] = True
    
    if not hasattr(pattern, '__iter__'):
        pattern = [pattern]
    
    for item in pattern:
        matched = ls(pattern=item, **kwargs)
        for obj in matched:
            obj.Selected = False

def select(pattern=None, add=False, toggle=False, **kwargs):
    '''
    Selects objects that match the given parameters
    @param add: add the matched objects to the selection
    @param toggle: toggles the selection of the matched objects
    See ls function for additional arguments
    '''
    if not hasattr(pattern, "__iter__"):
        pattern = [pattern]
    
    kwargs.pop('selected', None)
    
    if not add and not toggle:
        deselect(pattern=None, **kwargs)
    
    if toggle:
        def selectFunc(x):
            x.Selected = not x.Selected
    else:
        def selectFunc(x):
            x.Selected = True
                
    for item in pattern:
        matched = ls(pattern=item, **kwargs)
        map(selectFunc, matched)
    
def delete(pattern=None, **kwargs):
    '''
    Deletes objects that match the given parameters
    See ls function for additional arguments
    '''
    if not hasattr(pattern, "__iter__"):
        pattern = [pattern]
    
    for item in pattern:
        matched = ls(pattern=item, **kwargs)
        for obj in matched:
            obj.FBDelete()

def ls(pattern=None, type=None, selected=None, includeNamespace=True):
    '''
    Similar to Maya's ls command - returns list of objects that match the given parameters
    @param pattern: name of an object with with optional wild cards '*'
    @param type: object to compare if the component is of that type (either string or python class/type)
    @param selected: True/False if the object is selected or not. Default is either
    @param includeNamespace: does the search use the complete name (with namespace)  Default True
    '''
    # set up the name testing based on the pattern
    if pattern:
        # create a name return function
        if includeNamespace:
            getName = lambda x: getattr(x, 'LongName', x.Name)
        else:
            getName = lambda x: x.Name
        
        # if there is a wild card in the pattern
        if '*' in pattern:
            pattern = pattern.replace('*', '.*')
            # name testing function
            passesNameTest = lambda x: re.match(pattern, getName(x))
        else:
            passesNameTest = lambda x: pattern == getName(x)       
    else:
        passesNameTest = lambda x: True

    # for getting selection test
    if selected is not None:
        passesSelectionTest = lambda x: x.Selected == selected
    else:
        passesSelectionTest = lambda x: True
    
    # for testing the type of component
    if type:
        # if they gave a string, evaluate it
        if isinstance(type, basestring):
            try:
                type = eval(type)
            except NameError:
                raise NameError("Can not find object type '%s' in current namespace" % type)

        passesTypeTest = lambda x: isinstance(x, type)
    # no type was given so its True by default
    else:
        passesTypeTest = lambda x: True
               
    matchList = []
    for cmpnt in kAllSceneComponents:
        # if we did not pass the selection test, continue on
        if not passesSelectionTest(cmpnt):
            continue
        # do the same for matching type
        if not passesTypeTest(cmpnt):
            continue
        
        if passesNameTest(cmpnt):
            matchList.append(cmpnt)
                   
    return matchList