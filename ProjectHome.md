**A thank you to those who have responded to me with their support and ideas. However this project has been lacking development and fell behind. I am no longer supporting the project or releasing any updates. I will leave this project online for others to use and learn. The community and demand is too small right now to invest enough time in keeping this going. Thanks for your support.**

# Introduction #
PyMoBu is a python package that contains many enhancements and features for Autodesk's MotionBuilder Python scripting. The goal is to not reinvent the entire MotionBuilder Python module, but create new classes that contain powerful methods for working with MotionBuilder's native Python objects.

In addition, a number of useful tools come with PyMoBu that make performing common operations easier.

**Note:** PyMoBu objects are not compatible with native MotionBuilder python functions. This is a limitation of the C++ python wrapper that I was unable to get around and ultimately had use this method of implementation.

### Online Documentation Available: ###

<a href='http://www.scottenglert.com/pymobu/documentation-0.1/'>Version 0.1</a>

## Core Functionality ##
Functions similar to Maya's, such as ls, select, delete, deselect, and help have been created. Making it easier to get a list of objects based on a variety of parameters making it much more powerful than any of MotionBuilder's current functions.

<a href='http://www.scottenglert.com/pymobu/core_capture.html'><b>Watch Demo Video of Core Functions</b></a>

```
# Convert any FBComponent to a PyMoBu object
fbCube = FBFindModelByName('Cube')
print fbCube
# Result: <pyfbsdk.FBModel object at 0x173D54B0>

pymobuCube = fbCube.ConvertToPyMoBu()
print pymobuCube
# Result: PMBModel('Cube')

# List all components that begin with 'Cube' and are selected
ls('Cube*', selected=True)
# Result: [PMBModel('Cube'), PMBModel('Cube 1')]

# Toggle the selection of all components that begin with 'Marker'
select('Marker*', toggle=True)

# Delete all components named 'Cube'
delete('Cube*')

# Get help on an object and display it in a new window
help(FBApplication)
```

## Data Types ##
Math operators and other matrix/vector related functions are added to FBMatrix, FBVector3d, and FBVector2d classes. These include but not limited to: addition, subtraction, multiplication, division, cross product, dot product, inverse matrix, and more.

These are automatically inserted upon importing the PyMoBu module.

```
vectorA = FBVector3d(1,0,0)
vectorB = FBVector3d(0,1,0)

# Vector cross product
vectorA.Cross(vectorB)
# Result: FBVector3d(0,0,1)

# Vector dot product
vectorA.Dot(vectorB)
# Result: 0.0
```

## Components ##
Enhancements to MotionBuilder components include adding, removing, swapping, and getting object namespaces. Powerful component property listing, adding, and removing.

<a href='http://www.scottenglert.com/pymobu/component_capture.html'><b>Watch Demo Video of Component Functions</b></a>

```
# List all properties that are booleans
pymobuCube.ListProperties(type='Bool')

# Add a property
pymobuCube.AddProperty(name='MyProperty', type='Vector3D')

# List all user properties
pymobuCube.ListProperties(IsUserProperty=True)
```

### Constraints ###
Individual constraint classes are created that offer specific methods for that type of constraint. It is now easier to create and manage constraints in MotionBuilder. Adding, removing, and getting objects connected to constraints is very simple as well as setting the various properties of a constraint. This was one of the main focuses for PyMoBu and contains many useful methods.

<a href='http://www.scottenglert.com/pymobu/constraint_capture.html'> <b>Watch Demo Video of Constraint Functions</b></a>

```
# Create an aim constraint named 'MyAim'
myAimConstraint = CreateConstraint('Aim', 'MyAim')
# Result: PMBAimConstraint('MyAim')

# Specific methods for each constraint type
myAimConstraint.GetUpVector()
# Result: FBVector3d(0, 1, 0)

GetConstraintsByType('Aim')
# Result: [PMBAimConstraint('MyAim')]
```

### Models ###
It is now easier to get and set matrices and vectors. More improvements are coming.

```
pymobuCube.GetTranslation(worldSpace=True)
# Result: FBVector3d(10,5,15)

pymobuCube.GetMatrix(type='Rotation')
# Result: (1.000000, 0.000000, 0.000000, 0.000000)
#         (0.000000, 1.000000, 0.000000, 0.000000)
#         (0.000000, 0.000000, 1.000000, 0.000000)
#         (0.000000, 0.000000, 0.000000, 1.000000)
```