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
Constraint Module

Individual constraint classes and related functions

You can instantiate a PyMoBu constraint passing a MotionBuilder
constraint into one of the specific constraint classes.

You can also create a specific constraint through either the class's
'Create' method or through the CreateConstraint function.
'''
import logging
from pyfbsdk import *
from pymobu.components import PMBBox
#from pymobu import decorator

logger = logging.getLogger(__name__)

# create a dictionary of constraint name / indices
kConstraintTypes = dict((FBConstraintManager().TypeGetName(i), i) for i in xrange(FBConstraintManager().TypeGetCount()))

# -----------------------------------------------------
# Constraint Utility Functions
# -----------------------------------------------------
def GetConstraintByName(name, includeNamespace=True):
    '''Returns a constraint that matches it's long name'''
    for const in FBSystem().Scene.Constraints:
        if includeNamespace:
            constraintName = const.LongName
        else:
            constraintName = const.Name 
        if name == constraintName:
            return ConvertToPMBConstraint(const)

def GetConstraintsByType(type):
    '''Returns a list of constraints that are of a given type (Aim, Position, ect)'''
    ret = []
    for constraint in FBSystem().Scene.Constraints:
        if not isinstance(constraint, PMBBaseConstraint):
            classType = getattr(kConstraintClassDict.get(constraint.Description), 'constraintType')
        else:
            classType = getattr(constraint, 'constraintType')
        if classType == type:
            ret.append(ConvertToPMBConstraint(constraint))
    return ret

def GetCharacterByName(name):
    '''Finds a character with the same long name and returns it'''
    for char in FBSystem().Scene.Characters:
        if name == char.LongName:
            return ConvertToPMBConstraint(char)

def CreateConstraint(type, name=None):
    '''
    Create a constraint with the given type and optionally with a name
    @param type: name of constraint type found in kConstraintTypes
    @param name: name to give constraint. Default is used if None 
    '''
    try:
        constraint = FBConstraintManager().TypeCreateConstraint(kConstraintTypes[type])               
    except KeyError:
        raise Exception("Invalid constraint type '%s'" % type)
    
    FBSystem().Scene.Constraints.append(constraint)
    
    if name:
        constraint.Name = name
    
    return ConvertToPMBConstraint(constraint)

def ConvertToPMBConstraint(constraint):
    '''Converts the given constraint to a PyMoBu constraint type based on constraint description'''
    if isinstance(constraint, PMBConstraint):
        return constraint
    elif isinstance(constraint, FBConstraint):
        try:
            constClass = kConstraintClassDict[constraint.Description]
            return constClass(constraint)
        except KeyError:
            logger.warning("Not Implemented: Unable to convert constraint '%s'. No PyMoBu class available" % constraint.LongName)
            return constraint
    else:
        raise TypeError("Object is not an instance of FBConstraint. Got '%s' instead." % constraint.__class__.__name__)

FBConstraint.ConvertToPyMoBu = ConvertToPMBConstraint

# -----------------------------------------------------
# Constraint Functions (used in constraint classes)
# Not to be used separately
# -----------------------------------------------------
@property
def _AffectXProperty(self):
    '''Get/set the AffectX property (boolean)'''
    return self.component.PropertyList.Find("AffectX").Data

@_AffectXProperty.setter
def _AffectXProperty(self, state):
    self.component.PropertyList.Find("AffectX").Data = state

@property
def _AffectYProperty(self):
    '''Get/set the AffectY property (boolean)'''
    return self.component.PropertyList.Find("AffectY").Data

@_AffectYProperty.setter
def _AffectYProperty(self, state):
    self.component.PropertyList.Find("AffectY").Data = state

@property
def _AffectZProperty(self):
    '''Get/set the AffectZ property (boolean)'''
    return self.component.PropertyList.Find("AffectZ").Data

@_AffectZProperty.setter
def _AffectZProperty(self, state):
    self.component.PropertyList.Find("AffectZ").Data = state

def _RefFuncIndexWrapper(func, idx):
    '''Wraps another function that uses reference indices and returns that function'''
    def _wrappedFunc(self, *args, **kwargs):
        return func(self, idx=idx, *args, **kwargs)
    return _wrappedFunc

def _GetSingleRef(self, idx):
    '''Returns a single object in the constraint'''
    def _wrappedFunc(self):
        return self.component.ReferenceGet(idx)
    return _wrappedFunc
    
def _SetSingleRef(self, model, idx):
    '''Sets the constrained object, either by name or model object'''
    _RemoveSingleRef(self, idx)
    model = getattr(model, 'component', model)
    self.component.ReferenceAdd(idx, model)
    
def _RemoveSingleRef(self, idx):
    '''Removes the constrained object from the constraint'''
    while self.component.ReferenceGetCount(idx):
        constrained = _GetSingleRef(self, idx)
        self.component.ReferenceRemove(idx, constrained)
        
def _GetMultiRef(self, idx):
    '''Returns a list of objects in the constraint'''
    return [self.component.ReferenceGet(idx, i) for i in xrange(self.component.ReferenceGetCount(idx))]
    
def _AddMultiRef(self, models, idx):
    '''Adds multiple objects to the constraint'''
    if not hasattr(models, "__iter__"):
        models = [models]
    
    for m in models:
        m = getattr(m, 'component', m)
        self.component.ReferenceAdd(idx, m)
    
def _RemoveMultiRef(self, models, idx):
    '''Removes the given objects from the constraint'''
    if not hasattr(models, "__iter__"):
        models = [models]

    for m in models:
        m = getattr(m, 'component', m)
        self.component.ReferenceRemove(idx, m)
    
# -----------------------------------------------------
# Unique Constraint Classes
# -----------------------------------------------------
class PMBConstraint(PMBBox):
    '''base class for PyMoBu Constraints'''

    @classmethod
    def Create(cls, name=None):
        '''Create this type of constraint with the given name'''
        return CreateConstraint(type=cls.constraintType, name=name)
    
    @classmethod
    def Convert(cls, component):
        return ConvertToPMBConstraint(component)

class ConstrainedSourceMixIn(object):
    '''Mix-in class for the constrained / multiple source constraint types'''
    # Constrained reference
    SetConstrainedObject = _RefFuncIndexWrapper(_SetSingleRef, 0)
    GetConstrainedObject = _RefFuncIndexWrapper(_GetSingleRef, 0)
    RemoveConstrainedObject = _RefFuncIndexWrapper(_RemoveSingleRef, 0)
    
    # Source reference
    GetSourceObject = _RefFuncIndexWrapper(_GetMultiRef, 1)
    AddSourceObject= _RefFuncIndexWrapper(_AddMultiRef, 1)
    RemoveSourceObject = _RefFuncIndexWrapper(_RemoveMultiRef, 1)
    
class PMBCharacter(PMBConstraint):
    '''PyMoBu Character Class'''
        
    @classmethod
    def Create(cls, name):
        return cls(FBCharacter(name))
    
    def GetSlots(self, returnNames=False):
        '''Returns list of character mapping slots'''
        slots = []
        for property in self.component.PropertyList:
            slotName = getattr(property, 'Name', '')
            if slotName.endswith('Link'):
                if returnNames:
                    slots.append(slotName)
                else:
                    slots.append(property)
        return slots
     
    def ExportMapping(self, filePath, stripPrefix=None):
        '''
        Saves the character map as a template for later use
        @param filePath: file to store the mapping
        @param stripPrefix: remove a prefix from the model name  
        '''
        import cPickle as pickle
        
        mapping = self.GetCharacterMapping(True, False, stripPrefix)
        
        dumpFile = file(filePath, "w")
        pickle.dump(mapping, dumpFile, 0)
        dumpFile.close()
        
    def ImportMapping(self, filePath, addPrefix=None):
        '''
        Applies a character template to the character
        @param filePath: mapping file to import
        @param addPrefix: append a prefix onto the model names  
        '''
        import cPickle as pickle
        
        dumpFile = file(filePath)
        dumpData = pickle.load(dumpFile)
        dumpFile.close()
        
        for slot, model in dumpData.iteritems():
            if model and addPrefix:
                model = addPrefix + model
            self.SetSlotModel(slot, model)
    
    def GetSlotModel(self, slot):
        '''Gets the model that is assigned to the given character slot'''
        try:
            return self.component.PropertyList.Find(slot)[0]
        except IndexError:
            return None
    
    def RemoveSlotModel(self, slot):
        '''Removes the model from the given slot'''
        self.SetSlotModel(slot, None)
        
    def SetSlotModel(self, slot, model):
        '''
        Adds a model to a slot in the characterization map
        @param slot: FBPropertyListObject or slot name 
        @param model: model to add to the slot 
        '''
        if isinstance(model, basestring):
            obj = FBFindModelByName(model)
            if not obj:
                raise Exception("Object '%s' does not exist in scene. Unable to add it to character slot '%s'" % (model, slot))
        else:
            obj = model
                 
        # get the character slot
        charSlot = filter(lambda s: isinstance(s, FBPropertyListObject), [slot, self.PropertyList.Find("%sLink" % slot), self.PropertyList.Find(slot)])
        if charSlot:
            charSlot = charSlot[0]
        else:
            raise Exception("Invalid character mapping slot '%s'" % slot)
        # remove all current models from the slot
        charSlot.removeAll()
        
        if obj:
            charSlot.append(obj)
    
    def GetCharacterMapping(self, returnNames=True, skipEmpty=True, stripPrefix=None):
        '''
        Returns a dictionary of slot / model in the character mapping
        @param returnNames: return names as strings rather than FBModel objects
        @param skipEmpty: skip over slots that are empty
        @param stripPrefix: remove a prefix from name of the model  
        '''
        charSlots = self.GetSlots()
                
        mapping = {}
        for slot in charSlots:
            if not len(slot):
                if skipEmpty:
                    continue
                else:
                    model = None
            else:
                model = slot[0]
            
            if returnNames:
                slot = slot.Name
                if model:
                    model = model.LongName
                    if stripPrefix:
                        model = model.replace(stripPrefix, "")
            
            mapping[slot] = model
        
        return mapping
    
class PMBAimConstraint(PMBConstraint):
    '''Aim constraint class'''
    constraintType = 'Aim'
    kWorldUpType = {"Scene Up" : 0, "Object Up" : 1, "Object Rotation Up" : 2, "Vector" : 3, "None" : 4}
    
    # Constrained reference
    SetConstrainedObject = _RefFuncIndexWrapper(_SetSingleRef, 0)
    GetConstrainedObject = _RefFuncIndexWrapper(_GetSingleRef, 0)
    RemoveConstrainedObject = _RefFuncIndexWrapper(_RemoveSingleRef, 0)
    
    # Aim at reference
    AddAimAtObject = _RefFuncIndexWrapper(_AddMultiRef, 1)
    GetAimAtObject = _RefFuncIndexWrapper(_GetMultiRef, 1)
    RemoveAimAtObject = _RefFuncIndexWrapper(_RemoveMultiRef, 1)
    
    # World up reference
    SetWorldUpObject = _RefFuncIndexWrapper(_SetSingleRef, 2)
    GetWorldUpObject = _RefFuncIndexWrapper(_GetSingleRef, 2)
    RemoveWorldUpObject = _RefFuncIndexWrapper(_RemoveSingleRef, 2)
                   
    def SetWorldUpType(self, type):
        '''Sets the world up type'''
        try:
            self.component.PropertyList.Find("WorldUpType").Data = self.kWorldUpType[type]
        except KeyError:
            raise Exception("Invalid world up type '%s'" % type)
    
    def GetWorldUpType(self):
        '''Returns the world up type'''
        type = self.component.PropertyList.Find("WorldUpType").Data
        for t, i in self.kWorldUpType.iteritems():
            if i == type:
                return t 
    
    def GetUpVector(self):
        '''Returns the up vector'''
        return self.component.PropertyList.Find("UpVector").Data
    
    def SetUpVector(self, vector):
        '''Sets the up vector'''
        self.component.PropertyList.Find("UpVector").Data = vector
    
    def GetRotationOffset(self):
        '''Get the rotation offset vector'''
        return self.component.PropertyList.Find("RotationOffset").Data
    
    def SetRotationOffset(self, vector):
        '''Set the rotation offset vector'''
        self.component.PropertyList.Find("RotationOffset").Data = vector
    
    def GetAimVector(self):
        '''Get the aim vector'''
        return self.component.PropertyList.Find("AimVector").Data
    
    def SetAimVector(self, vector):
        '''Set the aim vector'''
        self.component.PropertyList.Find("AimVector").Data = vector
        
    AffectX = _AffectXProperty
    AffectY = _AffectYProperty
    AffectZ = _AffectZProperty
    
class PMBParentChildConstraint(ConstrainedSourceMixIn, PMBConstraint):
    '''Parent / child constraint class'''
    constraintType = 'Parent/Child'
    
    @property
    def AffectTranslationX(self):
        return self.component.PropertyList.Find("AffectTranslationX").Data
    
    @AffectTranslationX.setter
    def AffectTranslationX(self, state):
        self.component.PropertyList.Find("AffectTranslationX").Data = state
    
    @property
    def AffectTranslationY(self):
        return self.component.PropertyList.Find("AffectTranslationY").Data
    
    @AffectTranslationY.setter
    def AffectTranslationY(self, state):
        self.component.PropertyList.Find("AffectTranslationY").Data = state
    
    @property
    def AffectTranslationZ(self):
        return self.component.PropertyList.Find("AffectTranslationZ").Data
    
    @AffectTranslationZ.setter
    def AffectTranslationZ(self, state):
        self.component.PropertyList.Find("AffectTranslationZ").Data = state

    @property
    def AffectRotationX(self):
        return self.component.PropertyList.Find("AffectRotationX").Data
    
    @AffectRotationX.setter
    def AffectRotationX(self, state):
        self.component.PropertyList.Find("AffectRotationX").Data = state
    
    @property
    def AffectRotationY(self):
        return self.component.PropertyList.Find("AffectRotationY").Data
    
    @AffectRotationY.setter
    def AffectRotationY(self, state):
        self.component.PropertyList.Find("AffectRotationY").Data = state
    
    @property
    def AffectRotationZ(self):
        return self.component.PropertyList.Find("AffectRotationZ").Data
    
    @AffectRotationZ.setter
    def AffectRotationZ(self, state):
        self.component.PropertyList.Find("AffectRotationZ").Data = state 
    
    @property
    def AffectScalingX(self):
        return self.component.PropertyList.Find("AffectScalingX").Data
    
    @AffectScalingX.setter
    def AffectScalingX(self, state):
        self.component.PropertyList.Find("AffectScalingX").Data = state
    
    @property
    def AffectScalingY(self):
        return self.PropertyList.Find("AffectScalingY").Data
    
    @AffectScalingY.setter
    def AffectScalingY(self, state):
        self.component.PropertyList.Find("AffectScalingY").Data = state
    
    @property
    def AffectScalingZ(self):
        return self.component.PropertyList.Find("AffectScalingZ").Data
    
    @AffectScalingZ.setter
    def AffectScalingZ(self, state):
        self.component.PropertyList.Find("AffectScalingZ").Data = state
    
    @property
    def ScalingAffectsTranslation(self):
        return self.component.PropertyList.Find("ScalingAffectsTranslation").Data
        
    @ScalingAffectsTranslation.setter
    def ScalingAffectsTranslation(self, state):
        self.component.PropertyList.Find("ScalingAffectsTranslation").Data = state

class PMBRotationConstraint(ConstrainedSourceMixIn, PMBConstraint):
    '''Rotation (orientation) constraint class'''
    constraintType = 'Rotation'
    
    AffectX = _AffectXProperty
    AffectY = _AffectYProperty
    AffectZ = _AffectZProperty
    
    def GetRotation(self):
        return self.component.PropertyList.Find('Rotation').Data
    
    def SetRotation(self, vector):
        self.component.PropertyList.Find('Rotation').Data = vector

class PMBPositionConstraint(ConstrainedSourceMixIn, PMBConstraint):
    '''Position (point) constraint class'''
    constraintType = 'Position'
    
    AffectX = _AffectXProperty
    AffectY = _AffectYProperty
    AffectZ = _AffectZProperty
    
    def GetTranslation(self):
        return self.component.PropertyList.Find('Translation').Data
    
    def SetTranslation(self, vector):
        self.component.PropertyList.Find('Translation').Data = vector

class PMBScaleConstraint(ConstrainedSourceMixIn, PMBConstraint):
    '''Scale constraint class'''
    constraintType = 'Scale'
    kBlendMethods = dict(Average = 0, Geometric = 1)
    
    AffectX = _AffectXProperty
    AffectY = _AffectYProperty
    AffectZ = _AffectZProperty
        
    def GetScaling(self):
        return self.component.PropertyList.Find('Scaling').Data
    
    def SetScaling(self, vector):
        self.component.PropertyList.Find('Scaling').Data = vector
        
    def GetBlendMethod(self):
        '''Get the blend method'''
        currentMethod = self.component.PropertyList.Find('SourceBlendMode').Data
        for method, idx in self.kBlendMethods.iteritems():
            if currentMethod == idx:
                return method
            
    def SetBlendMethod(self, method):
        '''Set the blend method'''
        try:
            self.component.PropertyList.Find('SourceBlendMode').Data = self.kBlendMethods[method]
        except KeyError:
            raise Exception("Invalid method '%s'" % method)

class PMBThreePointsConstraint(PMBConstraint):
    '''3 Points constraint class'''
    constraintType = '3 Points'
    
    # Constrained reference
    SetConstrainedObject = _RefFuncIndexWrapper(_SetSingleRef, 0)
    GetConstrainedObject = _RefFuncIndexWrapper(_GetSingleRef, 0)
    RemoveConstrainedObject = _RefFuncIndexWrapper(_RemoveSingleRef, 0)
    
    # Origin reference
    SetOriginObject = _RefFuncIndexWrapper(_SetSingleRef, 1)
    GetOriginObject = _RefFuncIndexWrapper(_GetSingleRef, 1)
    RemoveOriginObject = _RefFuncIndexWrapper(_RemoveSingleRef, 1)
    
    # Target reference
    SetTargetObject = _RefFuncIndexWrapper(_SetSingleRef, 2)
    GetTargetObject = _RefFuncIndexWrapper(_GetSingleRef, 2)
    RemoveTargetObject = _RefFuncIndexWrapper(_RemoveSingleRef, 2)

    # Up reference
    SetUpObject = _RefFuncIndexWrapper(_SetSingleRef, 3)
    GetUpObject = _RefFuncIndexWrapper(_GetSingleRef, 3)
    RemoveUpObject = _RefFuncIndexWrapper(_RemoveSingleRef, 3)

class PMBRigidBodyConstraint(ConstrainedSourceMixIn, PMBConstraint):
    '''Rigid Body constraint class'''
    constraintType = 'Rigid Body'
    
class PMBMappingConstraint(PMBConstraint, FBConstraint):
    '''Mapping constraint class'''
    constraintType = 'Mapping'
    
    # Constrained reference
    SetConstrainedObject = _RefFuncIndexWrapper(_SetSingleRef, 0)
    GetConstrainedObject = _RefFuncIndexWrapper(_GetSingleRef, 0)
    RemoveConstrainedObject = _RefFuncIndexWrapper(_RemoveSingleRef, 0)
    
    # Reference reference
    SetReferenceObject = _RefFuncIndexWrapper(_SetSingleRef, 1)
    GetReferenceObject = _RefFuncIndexWrapper(_GetSingleRef, 1)
    RemoveReferenceObject = _RefFuncIndexWrapper(_RemoveSingleRef, 1)
            
    # Source reference
    SetSourceObject = _RefFuncIndexWrapper(_SetSingleRef, 2)
    GetSourceObject = _RefFuncIndexWrapper(_GetSingleRef, 2)
    RemoveSourceObject = _RefFuncIndexWrapper(_RemoveSingleRef, 2)
    
    # Source reference reference
    SetSourceReferenceObject = _RefFuncIndexWrapper(_SetSingleRef, 3)
    GetSourceReferenceObject = _RefFuncIndexWrapper(_GetSingleRef, 3)
    RemoveSourceReferenceObject = _RefFuncIndexWrapper(_RemoveSingleRef, 3)
    
class PMBRangeConstraint(PMBConstraint):
    '''Range constraint class'''
    constraintType = 'Range'
    
    # Constrained reference
    SetConstrainedObject = _RefFuncIndexWrapper(_SetSingleRef, 0)
    GetConstrainedObject = _RefFuncIndexWrapper(_GetSingleRef, 0)
    RemoveConstrainedObject = _RefFuncIndexWrapper(_RemoveSingleRef, 0)
    
    # Source reference
    SetSourceObject = _RefFuncIndexWrapper(_SetSingleRef, 1)
    GetSourceObject = _RefFuncIndexWrapper(_GetSingleRef, 1)
    RemoveSourceObject = _RefFuncIndexWrapper(_RemoveSingleRef, 1)
    
    # Pulling reference
    AddPullingObject = _RefFuncIndexWrapper(_AddMultiRef, 2)
    GetPullingObject = _RefFuncIndexWrapper(_GetMultiRef, 2)
    RemovePullingObject = _RefFuncIndexWrapper(_RemoveMultiRef, 2)
    
class PMBChainIKConstraint(PMBConstraint, FBConstraint):
    '''Chain IK constraint class'''
    constraintType = 'Chain IK'
    kSolverType = dict(ikRPsolver = 0, ikSCsolver = 1)
    kPoleType = dict(Vector = 0, Object = 1)
    kEvalTSAnim = dict(Never = 0, Auto = 1, Always = 2)
    
    # First joint reference
    SetFirstJoint = _RefFuncIndexWrapper(_SetSingleRef, 0)
    GetFirstJoint = _RefFuncIndexWrapper(_GetSingleRef, 0)
    RemoveFirstJoint = _RefFuncIndexWrapper(_RemoveSingleRef, 0)
    
    # End joint reference
    SetEndJoint = _RefFuncIndexWrapper(_SetSingleRef, 1)
    GetEndJoint = _RefFuncIndexWrapper(_GetSingleRef, 1)
    RemoveEndJoint = _RefFuncIndexWrapper(_RemoveSingleRef, 1)
    
    # Effector reference
    SetEffector = _RefFuncIndexWrapper(_SetSingleRef, 2)
    GetEffector = _RefFuncIndexWrapper(_GetSingleRef, 2)
    RemoveEffector = _RefFuncIndexWrapper(_RemoveSingleRef, 2)
    
    # Floor reference
    SetFloor = _RefFuncIndexWrapper(_SetSingleRef, 3)
    GetFloor = _RefFuncIndexWrapper(_GetSingleRef, 3)
    RemoveFloor = _RefFuncIndexWrapper(_RemoveSingleRef, 3)
    
    # Pulling reference
    AddPoleVectorObject = _RefFuncIndexWrapper(_AddMultiRef, 4)
    GetPoleVectorObject = _RefFuncIndexWrapper(_GetMultiRef, 4)
    RemovePoleVectorObject = _RefFuncIndexWrapper(_RemoveMultiRef, 4)
       
    def GetSolverType(self):
        '''Get the solver type'''
        solverType = self.component.PropertyList.Find('Solver Type').Data
        for type, idx in self.kSolverType.iteritems():
            if solverType == idx:
                return type

    def SetSolverType(self, type):
        '''Set the solver type'''
        try:
            self.component.PropertyList.Find('Solver Type').Data = self.kSolverType[type]
        except KeyError:
            raise Exception("Invalid solver type '%s'" % type)
    
    def GetTwist(self):
        '''Get the twist'''
        return self.component.PropertyList.Find('Twist').Data
    
    def SetTwist(self, value):
        '''Set the twist'''
        self.component.PropertyList.Find('Twist').Data = value
    
    def GetPoleType(self):
        '''Get the pole vector type'''
        poleVectorType = self.component.PropertyList.Find('PoleVectorType').Data
        for type, idx in self.kPoleType.iteritems():
            if poleVectorType == idx:
                return type
    
    def SetPoleType(self, type):
        '''Set the pole vector type'''
        try:
            self.component.PropertyList.Find('PoleVectorType').Data = self.kPoleType[type]
        except:
            raise Exception("Invalid pole type '%s'" % type)
    
    def GetPoleVector(self):
        '''Get pole vector'''
        return self.component.PropertyList.Find('PoleVector').Data
    
    def SetPoleVector(self, vector):
        '''Set the pole vector'''
        self.component.PropertyList.Find('PoleVector').Data = vector
    
    def GetPoleOffset(self):
        '''Get pole vector offset'''
        return self.component.PropertyList.Find('PoleVectorOffset').Data
    
    def SetPoleOffset(self, vector):
        '''Set the pole vector offset'''
        self.component.PropertyList.Find('PoleVectorOffset').Data = vector
    
    def GetEvalTSAnimation(self):
        '''Get the eval ts animation state'''
        animState = self.component.PropertyList.Find('EvaluateTSAnim').Data
        for state, idx in self.kEvalTSAnim.iteritems():
            if animState == idx:
                return state
    
    def SetEvalTSAnimation(self, state):
        '''Set the eval ts animation'''
        try:
            self.component.PropertyList.Find('EvaluateTSAnim').Data = self.kEvalTSAnim[state]
        except KeyError:
            raise Exception("Invalid evaluation state '%s'" % state)
    
class PMBPathConstraint(PMBConstraint):
    '''Path constraint class'''
    constraintType = 'Path'
    kWarpMode = dict(Percent = 0, Segment = 1)
    kAxes = {'X':0, '-X':1, 'Y':2, '-Y':3, 'Z':4, '-Z':5}
    
    # Constrained reference
    SetConstrainedObject = _RefFuncIndexWrapper(_SetSingleRef, 0)
    GetConstrainedObject = _RefFuncIndexWrapper(_GetSingleRef, 0)
    RemoveConstrainedObject = _RefFuncIndexWrapper(_RemoveSingleRef, 0)
    
    # Source reference
    def SetPathSource(self, model):
        '''Set the target object'''
        if not isinstance(model, FBModelPath3D):
            raise Exception("Object must be of type FBModelPath3D. Got '%s' instead" % model.__class__.__name__)
        self.RemovePathSource()
        self.component.ReferenceAdd(1, model)
    
    GetSourceObject = _RefFuncIndexWrapper(_GetSingleRef, 2)
    RemoveSourceObject = _RefFuncIndexWrapper(_RemoveSingleRef, 2)

    def GetWarpMode(self):
        '''Get the warp mode'''
        warp = self.component.PropertyList.Find('WarpMode').Data
        for mode, idx in self.kWarpMode.iteritems():
            if warp == idx:
                return mode
    
    def SetWarpMode(self, mode):
        '''Set the warp mode'''
        try:
            self.component.PropertyList.Find('WarpMode').Data = self.kWarpMode[mode]
        except KeyError:
            raise Exception("Invalid warp mode '%s'" % mode)
    
    def GetWarp(self):
        '''Get the warp value'''
        return self.component.PropertyList.Find('Warp').Data
    
    def SetWarp(self, value):
        '''Set the warp value'''
        self.component.PropertyList.Find('Warp').Data = value
    
    @property
    def FollowPath(self):
        '''Set the state of follow path'''
        return self.component.PropertyList.Find('FollowPath').Data
    
    @FollowPath.setter
    def FollowPath(self, state):
        self.component.PropertyList.Find('FollowPath').Data = state
    
    def SetUpVectorAxis(self, axis):
        '''Set the up vector axis'''
        try:
            self.component.PropertyList.Find('UpDirection').Data = self.kAxes[axis]
        except KeyError:
            raise Exception("Invalid axis '%s'" % axis)
    
    def GetUpVectorAxis(self):
        '''Get the up vector axis'''
        upAxis = self.component.PropertyList.Find('UpDirection').Data
        for axis, idx in self.kAxes.iteritems():
            if upAxis == idx:
                return axis
    
    def SetFrontVectorAxis(self, axis):
        '''Set the front vector axis'''
        try:
            self.component.PropertyList.Find('FrontDirection').Data = self.kAxes[axis]
        except KeyError:
            raise Exception("Invalid axis '%s'" % axis)
    
    def GetFrontVectorAxis(self):
        '''Get the front vector axis'''
        frontAxis = self.component.PropertyList.Find('UpDirection').Data
        for axis, idx in self.kAxes.iteritems():
            if frontAxis == idx:
                return axis
    
    def SetTranslationOffset(self, vector):
        '''Set the translation offset'''
        self.component.PropertyList.Find('Translation Offset').Data = vector
    
    def GetTranslationOffset(self):
        '''Get the translation offset'''
        return self.component.PropertyList.Find('Translation Offset').Data
    
    def SetRoll(self, value):
        '''Set the roll value'''
        self.component.PropertyList.Find('Roll').Data = value
    
    def GetRoll(self):
        '''Get the roll value'''
        return self.component.PropertyList.Find('Roll').Data
    
    def SetPitch(self, value):
        '''Set the pitch value'''
        self.component.PropertyList.Find('Pitch').Data = value
    
    def GetPitch(self):
        '''Get the pitch value'''
        return self.component.PropertyList.Find('Pitch').Data
    
    def SetYaw(self, value):
        '''Set the yaw value'''
        self.component.PropertyList.Find('Yaw').Data = value
    
    def GetYaw(self):
        '''Get the yaw value'''
        return self.component.PropertyList.Find('Yaw').Data
    
    def SetUIColor(self, color):
        '''Set the UI color'''
        self.component.PropertyList.Find('UI Color').Data = color
    
    def GetUIColor(self):
        '''Get the UI color'''
        return self.component.PropertyList.Find('UI Color').Data
    
    @property
    def ShowWarpKeyFrame(self):
        '''The state of the show warp key frame'''
        return self.component.PropertyList.Find('ShowWarp').Data
    
    @ShowWarpKeyFrame.setter
    def ShowWarpKeyFrame(self, state):
        self.component.PropertyList.Find('ShowWarp').Data = state

class PMBExpressionConstraint(PMBConstraint):
    '''Expression constraint class'''
    constraintType = 'Expression'

class PMBMultiReferentialConstraint(PMBConstraint):
    '''Multi referential constraint class'''
    constraintType = 'Multi Referential'
    
    # Rigid reference
    AddRigidObject = _RefFuncIndexWrapper(_AddMultiRef, 0)
    GetRigidObject = _RefFuncIndexWrapper(_GetMultiRef, 0)
    RemoveRigidObject = _RefFuncIndexWrapper(_RemoveMultiRef, 0)
    
    # Rigid reference
    AddParentObject = _RefFuncIndexWrapper(_AddMultiRef, 1)
    GetParentObject = _RefFuncIndexWrapper(_GetMultiRef, 1)
    RemoveParentObject = _RefFuncIndexWrapper(_RemoveMultiRef, 1)
    
##########
## TODO ##
##########
    def SetActiveReference(self, model):
        pass
    
    def GetActiveReference(self):
        pass
    
    def SetOffsetTranslation(self, model, vector):
        '''Set the offset translation for the given model'''
        if hasattr(model, 'Name'):
            model = model.Name
        propertyName = '%s.Offset.Translation' % model
        self.component.PropertyList.Find(propertyName).Data = vector
    
    def GetOffsetTranslation(self, model):
        '''Get the offset translation for the given model'''
        if hasattr(model, 'Name'):
            model = model.Name
        propertyName = '%s.Offset.Translation' % model
        return self.component.PropertyList.Find(propertyName).Data
    
    def SetOffsetRotation(self, model, vector):
        '''Set the offset rotation for the given model'''
        if hasattr(model, 'Name'):
            model = model.Name
        propertyName = '%s.Offset.Rotation' % model
        self.component.PropertyList.Find(propertyName).Data = vector
    
    def GetOffsetRotation(self, model):
        '''Get the offset rotation for the given model'''
        if hasattr(model, 'Name'):
            model = model.Name
        propertyName = '%s.Offset.Rotation' % model
        return self.component.PropertyList.Find(propertyName).Data
        
class PMBConstraintRelation(PMBConstraint):
    '''Relation constraint class'''
    constraintType = 'Relation'
    
    def GetBoxByName(self, name):
        '''Find a box in the constraint with a specific name'''
        for box in self.component.Boxes:
            if box.Name == name:
                return box
    
    def GetSenders(self):
        pass
    
    def GetReceivers(self):
        pass

# Assign the classes to the description of each constraint
kConstraintClassDict = {"Aim" : PMBAimConstraint,
                        "Position From Positions" : PMBPositionConstraint,
                        "Rotation From 3 Positions" : PMBThreePointsConstraint,
                        "Single Chain IK" : PMBChainIKConstraint,
                        "Expressions" : PMBExpressionConstraint,
                        "Simple Mapping" : PMBMappingConstraint,
                        "Multi-Referential" : PMBMultiReferentialConstraint,
                        "Parent-Child" : PMBParentChildConstraint,
                        "Path Constraint" : PMBPathConstraint,
                        "Range" : PMBRangeConstraint,
                        "Relations" : PMBConstraintRelation,
                        "Rigid Body" : PMBRigidBodyConstraint,
                        "Rotation From Rotations" : PMBRotationConstraint,
                        "Scale From Scales" : PMBScaleConstraint,
                        "Character" : PMBCharacter}