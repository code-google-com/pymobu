# License from PyEuclid
# Modified by Scott Englert for PyMoBu
#
# Copyright (c) 2006 Alex Holkner
# Alex.Holkner@mail.google.com
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
# 
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
'''
Matrix and vector module for PyMoBu - will work as stand alone library
Modified code from PyEuclid module - http://code.google.com/p/pyeuclid/
See license in source code.

Works with FBMatrix, FBVector3d, and FBVector2d

To use, import this module and call insertMathClasses function to integrate
insert these as base classes.
'''
import math
import operator
from pyfbsdk import FBVector3d
from pyfbsdk import FBVector2d
from pyfbsdk import FBMatrix

class PMBMatrix(object):
    '''Base class for FBMatrix'''      
    
    def __copy__(self):
        return self.__class__(self)

    Copy = __copy__

    def __mul__(self, other):
        if isinstance(other, FBMatrix):
            Aa = self[0]
            Ab = self[1]
            Ac = self[2]
            Ad = self[3]
            Ae = self[4]
            Af = self[5]
            Ag = self[6]
            Ah = self[7]
            Ai = self[8]
            Aj = self[9]
            Ak = self[10]
            Al = self[11]
            Am = self[12]
            An = self[13]
            Ao = self[14]
            Ap = self[15]
            Ba = other[0]
            Bb = other[1]
            Bc = other[2]
            Bd = other[3]
            Be = other[4]
            Bf = other[5]
            Bg = other[6]
            Bh = other[7]
            Bi = other[8]
            Bj = other[9]
            Bk = other[10]
            Bl = other[11]
            Bm = other[12]
            Bn = other[13]
            Bo = other[14]
            Bp = other[15]
            C = self.__class__()
            C[0] = Aa * Ba + Ab * Be + Ac * Bi + Ad * Bm
            C[1] = Aa * Bb + Ab * Bf + Ac * Bj + Ad * Bn
            C[2] = Aa * Bc + Ab * Bg + Ac * Bk + Ad * Bo
            C[3] = Aa * Bd + Ab * Bh + Ac * Bl + Ad * Bp
            C[4] = Ae * Ba + Af * Be + Ag * Bi + Ah * Bm
            C[5] = Ae * Bb + Af * Bf + Ag * Bj + Ah * Bn
            C[6] = Ae * Bc + Af * Bg + Ag * Bk + Ah * Bo
            C[7] = Ae * Bd + Af * Bh + Ag * Bl + Ah * Bp
            C[8] = Ai * Ba + Aj * Be + Ak * Bi + Al * Bm
            C[9] = Ai * Bb + Aj * Bf + Ak * Bj + Al * Bn
            C[10] = Ai * Bc + Aj * Bg + Ak * Bk + Al * Bo
            C[11] = Ai * Bd + Aj * Bh + Ak * Bl + Al * Bp
            C[12] = Am * Ba + An * Be + Ao * Bi + Ap * Bm
            C[13] = Am * Bb + An * Bf + Ao * Bj + Ap * Bn
            C[14] = Am * Bc + An * Bg + Ao * Bk + Ap * Bo
            C[15] = Am * Bd + An * Bh + Ao * Bl + Ap * Bp
            return C
        elif isinstance(other, FBVector3d):
            A = self
            B = other
            V = FBVector3d()
            V.X = A[0] * B.X + A[1] * B.Y + A[2] * B.Z
            V.Y = A[4] * B.X + A[5] * B.Y + A[6] * B.Z
            V.z = A[8] * B.X + A[9] * B.Y + A[10] * B.Z
            return V

    def Transform(self, other):
        A = self
        B = other
        P = FBVector3d()
        P.X = A[0] * B.X + A[1] * B.Y + A[2] * B.Z + A[3]
        P.Y = A[4] * B.X + A[5] * B.Y + A[6] * B.Z + A[7]
        P.Z = A[8] * B.X + A[9] * B.Y + A[10] * B.Z + A[11]
        w =   A[12] * B.X + A[13] * B.Y + A[14] * B.Z + A[15]
        if w <> 0:
            P.X /= w
            P.Y /= w
            P.Z /= w
        return P

    def Scale(self, x, y, z):
        self *= self.__class__.NewScale(x, y, z)
        return self

    def Translate(self, x, y, z):
        self *= self.__class__.NewTranslate(x, y, z)
        return self 

    def RotateX(self, angle):
        self *= self.__class__.NewRotateX(angle)
        return self

    def RotateY(self, angle):
        self *= self.__class__.NewRotateY(angle)
        return self

    def RotateZ(self, angle):
        self *= self.__class__.NewRotateZ(angle)
        return self

    def RotateAxis(self, angle, axis):
        self *= self.__class__.NewRotateAxis(angle, axis)
        return self

    def RotateEuler(self, heading, attitude, bank):
        self *= self.__class__.NewRotateEuler(heading, attitude, bank)
        return self

    def RotateTriple_axis(self, x, y, z):
        self *= self.__class__.NewRotateTripleAxis(x, y, z)
        return self

    def Transpose(self):
        (self[0], self[4], self[8], self[12],
         self[1], self[5], self[9], self[13],
         self[2], self[6], self[10], self[14],
         self[3], self[7], self[11], self[15]) = \
        (self[0], self[1], self[2], self[3],
         self[4], self[5], self[6], self[7],
         self[8], self[9], self[10], self[11],
         self[12], self[13], self[14], self[15])

    def Transposed(self):
        M = self.Copy()
        M.Transpose()
        return M

    @classmethod
    def New(cls, *values):
        M = cls()
        M[:] = values
        return M
    
    @classmethod
    def NewIdentity(cls):
        self = cls()
        return self

    @classmethod
    def NewScale(cls, x, y, z):
        self = cls()
        self[0] = x
        self[5] = y
        self[10] = z
        return self
    
    @classmethod
    def NewTranslate(cls, x, y, z):
        self = cls()
        self[3] = x
        self[7] = y
        self[11] = z
        return self
    
    @classmethod
    def NewRotateX(cls, angle):
        self = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        self[5] = self[10] = c
        self[6] = -s
        self[9] = s
        return self
    
    @classmethod
    def NewRotateY(cls, angle):
        self = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        self[0] = self[10] = c
        self[2] = s
        self[8] = -s
        return self    
    
    @classmethod
    def NewRotateZ(cls, angle):
        self = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        self[0] = self[5] = c
        self[1] = -s
        self[4] = s
        return self
    
    @classmethod
    def NewRotateAxis(cls, angle, axis):
        assert(isinstance(axis, FBVector3d))
        vector = axis.Normalized()
        x = vector.X
        y = vector.Y
        z = vector.Z

        self = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        c1 = 1. - c
        
        # from the glRotate man page
        self[0] = x * x * c1 + c
        self[1] = x * y * c1 - z * s
        self[2] = x * z * c1 + y * s
        self[4] = y * x * c1 + z * s
        self[5] = y * y * c1 + c
        self[6] = y * z * c1 - x * s
        self[8] = x * z * c1 - y * s
        self[9] = y * z * c1 + x * s
        self[10] = z * z * c1 + c
        return self

    @classmethod
    def NewRotateEuler(cls, heading, attitude, bank):
        # from http://www.euclideanspace.com/
        ch = math.cos(heading)
        sh = math.sin(heading)
        ca = math.cos(attitude)
        sa = math.sin(attitude)
        cb = math.cos(bank)
        sb = math.sin(bank)

        self = cls()
        self[0] = ch * ca
        self[1] = sh * sb - ch * sa * cb
        self[2] = ch * sa * sb + sh * cb
        self[4] = sa
        self[5] = ca * cb
        self[6] = -ca * sb
        self[8] = -sh * ca
        self[9] = sh * sa * cb + ch * sb
        self[10] = -sh * sa * sb + ch * cb
        return self
    
    @classmethod
    def NewRotateTripleAxis(cls, x, y, z):
      m = cls()
      
      m[0], m[1], m[2] = x.X, y.X, z.X
      m[4], m[5], m[6] = x.Y, y.Y, z.Y
      m[8], m[9], m[10] = x.Z, y.Z, z.Z
      
      return m
  
    @classmethod
    def NewLookAt(cls, eye, at, up):
      z = (eye - at).Normalized()
      x = up.Cross(z).Normalized()
      y = z.Cross(x)
      
      m = cls.NewRotateTripleAxis(x, y, z)
      m[3], m[7], m[11] = eye.X, eye.Y, eye.Z
      return m
    
    @classmethod
    def NewPerspective(cls, fov_y, aspect, near, far):
        # from the gluPerspective man page
        f = 1 / math.tan(fov_y / 2)
        self = cls()
        assert near != 0.0 and near != far
        self[0] = f / aspect
        self[5] = f
        self[10] = (far + near) / (near - far)
        self[11] = 2 * far * near / (near - far)
        self[14] = -1
        self[15] = 0
        return self

    def Determinant(self):
        return ((self[0] * self[5] - self[4] * self[1])
              * (self[10] * self[15] - self[14] * self[11])
              - (self[0] * self[9] - self[8] * self[1])
              * (self[6] * self[15] - self[14] * self[7])
              + (self[0] * self[13] - self[12] * self[1])
              * (self[6] * self[11] - self[10] * self[7])
              + (self[4] * self[9] - self[8] * self[5])
              * (self[2] * self[15] - self[14] * self[3])
              - (self[4] * self[13] - self[12] * self[5])
              * (self[2] * self[11] - self[10] * self[3])
              + (self[8] * self[13] - self[12] * self[9])
              * (self[2] * self[7] - self[6] * self[3]))

    def Inverse(self):
        tmp = self.__class__()
        d = self.Determinant();

        if abs(d) < 0.001:
            # No inverse, return identity
            return tmp
        else:
            d = 1.0 / d;

            tmp[0] = d * (self[5] * (self[10] * self[15] - self[14] * self[11]) + self[9] * (self[14] * self[7] - self[6] * self[15]) + self[13] * (self[6] * self[11] - self[10] * self[7]));
            tmp[4] = d * (self[6] * (self[8] * self[15] - self[12] * self[11]) + self[10] * (self[12] * self[7] - self[4] * self[15]) + self[14] * (self[4] * self[11] - self[8] * self[7]));
            tmp[8] = d * (self[7] * (self[8] * self[13] - self[12] * self[9]) + self[11] * (self[12] * self[5] - self[4] * self[13]) + self[15] * (self[4] * self[9] - self[8] * self[5]));
            tmp[12] = d * (self[4] * (self[13] * self[10] - self[9] * self[14]) + self[8] * (self[5] * self[14] - self[13] * self[6]) + self[12] * (self[9] * self[6] - self[5] * self[10]));
            
            tmp[1] = d * (self[9] * (self[2] * self[15] - self[14] * self[3]) + self[13] * (self[10] * self[3] - self[2] * self[11]) + self[1] * (self[14] * self[11] - self[10] * self[15]));
            tmp[5] = d * (self[10] * (self[0] * self[15] - self[12] * self[3]) + self[14] * (self[8] * self[3] - self[0] * self[11]) + self[2] * (self[12] * self[11] - self[8] * self[15]));
            tmp[9] = d * (self[11] * (self[0] * self[13] - self[12] * self[1]) + self[15] * (self[8] * self[1] - self[0] * self[9]) + self[3] * (self[12] * self[9] - self[8] * self[13]));
            tmp[13] = d * (self[8] * (self[13] * self[2] - self[1] * self[14]) + self[12] * (self[1] * self[10] - self[9] * self[2]) + self[0] * (self[9] * self[14] - self[13] * self[10]));
            
            tmp[2] = d * (self[13] * (self[2] * self[7] - self[6] * self[3]) + self[1] * (self[6] * self[15] - self[14] * self[7]) + self[5] * (self[14] * self[3] - self[2] * self[15]));
            tmp[6] = d * (self[14] * (self[0] * self[7] - self[4] * self[3]) + self[2] * (self[4] * self[15] - self[12] * self[7]) + self[6] * (self[12] * self[3] - self[0] * self[15]));
            tmp[10] = d * (self[15] * (self[0] * self[5] - self[4] * self[1]) + self[3] * (self[4] * self[13] - self[12] * self[5]) + self[7] * (self[12] * self[1] - self[0] * self[13]));
            tmp[14] = d * (self[12] * (self[5] * self[2] - self[1] * self[6]) + self[0] * (self[13] * self[6] - self[5] * self[14]) + self[4] * (self[1] * self[14] - self[13] * self[2]));
            
            tmp[3] = d * (self[1] * (self[10] * self[7] - self[6] * self[11]) + self[5] * (self[2] * self[11] - self[10] * self[3]) + self[9] * (self[6] * self[3] - self[2] * self[7]));
            tmp[7] = d * (self[2] * (self[8] * self[7] - self[4] * self[11]) + self[6] * (self[0] * self[11] - self[8] * self[3]) + self[10] * (self[4] * self[3] - self[0] * self[7]));
            tmp[11] = d * (self[3] * (self[8] * self[5] - self[4] * self[9]) + self[7] * (self[0] * self[9] - self[8] * self[1]) + self[11] * (self[4] * self[1] - self[0] * self[5]));
            tmp[15] = d * (self[0] * (self[5] * self[10] - self[9] * self[6]) + self[4] * (self[9] * self[2] - self[1] * self[10]) + self[8] * (self[1] * self[6] - self[5] * self[2]));

        return tmp;

class PMBVector2d(object):
    '''Base class for FBVector2d'''
    
    def __copy__(self):
        return self.__class__(self)
    
    Copy = __copy__

    def __eq__(self, other):
        if isinstance(other, FBVector2d):
            return self.X == other.X and \
                   self.Y == other.Y
        elif hasattr(other, '__len__') and len(other) == 2:
            return self.X == other[0] and \
                   self.Y == other[1]
        else:
            raise Exception("Invalid vector length. Vector '%s' must have 2 items for comparison." % other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self.X != 0 or self.Y != 0

    def __iadd__(self, other):
        if isinstance(other, FBVector2d):
            self.X += other.X
            self.Y += other.Y
        else:
            self.X += other[0]
            self.Y += other[1]
        return self
    
    def __isub__(self, other):
        if isinstance(other, FBVector2d):
            self.X -= other.X
            self.Y -= other.Y
        else:
            self.X -= other[0]
            self.Y -= other[1]
        return self

    def __mul__(self, other):
        if isinstance(other, (int, long, float)):
            return self.__class__(self.X * other, self.Y * other)
        else:
            raise TypeError("Multiplier must be instance of (int, long, or float). '%s' given." % other.__class__.__name__)

    def __imul__(self, other):
        if isinstance(other, (int, long, float)):
            self.X *= other
            self.Y *= other
            return self
        else:
            raise TypeError("Multiplier must be instance of (int, long, or float). '%s' given." % other.__class__.__name__)

    def __div__(self, other):
        if isinstance(other, (int, long, float)):
            return self.__class__(operator.div(self.X, other), operator.div(self.Y, other))
        else:
            raise TypeError("Divider must be instance of (int, long, or float). '%s' given." % other.__class__.__name__)

    def __truediv__(self, other):
        if isinstance(other, (int, long, float)):
            return self.__class__(operator.truediv(self.X, other), operator.truediv(self.Y, other))
        else:
            raise TypeError("Divider must be instance of (int, long, or float). '%s' given." % other.__class__.__name__)

    def __neg__(self):
        return self.__class__(-self.X, -self.Y)

    def __abs__(self):
        return math.sqrt(self.X ** 2 + self.Y ** 2)
    
    Magnitude = __abs__

    def MagnitudeSquared(self):
        return self.X ** 2 + self.Y ** 2

    def Normalize(self):
        d = self.Magnitude()
        if d:
            self.X /= d
            self.Y /= d
        return self

    def Normalized(self):
        d = self.Magnitude()
        if d:
            return self.__class__(self.X / d, 
                           self.Y / d)
        return self.copy()

    def Dot(self, other):
        if isinstance(other, FBVector2d):
            return self.X * other.X + \
               self.Y * other.Y
        else:
            raise TypeError("Object '%s' must be instance of FBVector2d." % other)

    def Cross(self):
        return self.__class__(self.Y, -self.X)

    def Reflect(self, normal):
        # assume normal is normalized
        if isinstance(normal, FBVector2d):
            d = 2 * (self.X * normal.X + self.Y * normal.Y)
            return self.__class__(self.X - d * normal.X,
                       self.Y - d * normal.Y)
        else:
            raise TypeError("Object '%s' must be instance of FBVector2d." % other)
    
    @property
    def X(self):
        return self[0]
    
    @X.setter
    def X(self, value):
        self[0] = value
    
    @property
    def Y(self):
        return self[1]
    
    @Y.setter
    def Y(self, value):
        self[1] = value
    
    __pos__ = __copy__

class PMBVector3d(object):
    '''Base class for FBVector3d'''
    def __copy__(self):
        return self.__class__(self)
    
    Copy = __copy__

    def __eq__(self, other):
        if isinstance(other, FBVector3d):
            return self.X == other.X and \
                   self.Y == other.Y and \
                   self.Z == other.Z
        elif hasattr(other, '__len__') and len(other) == 3:
            return self.X == other[0] and \
                   self.Y == other[1] and \
                   self.Z == other[2]
        else:
            raise Exception("Invalid vector length. Vector '%s' must have 3 items for comparison." % other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self.X != 0 or self.Y != 0 or self.Z != 0

    def __iadd__(self, other):
        if isinstance(other, FBVector3d):
            self.X += other.X
            self.Y += other.Y
            self.Z += other.Z
        else:
            self.X += other[0]
            self.Y += other[1]
            self.Z += other[2]
        return self

    def __isub__(self, other):
        if isinstance(other, FBVector3d):
            self.X -= other.X
            self.Y -= other.Y
            self.Z -= other.Z
        else:
            self.X -= other[0]
            self.Y -= other[1]
            self.Z -= other[2]
        return self
   
    def __mul__(self, other):
        if isinstance(other, FBVector3d):
            copy = self.Copy()
            return copy.Dot(other)
        elif isinstance(other, (int, long, float)): 
            return self.__class__(self.X * other,
                           self.Y * other,
                           self.Z * other)
        else:
            raise TypeError("Multiplier must be instance of (int, long, or float). '%s' given." % other.__class__.__name__)

    def __imul__(self, other):
        if isinstance(other, (int, long, float)):
            self.X *= other
            self.Y *= other
            self.Z *= other
            return self
        else:
            raise TypeError("Multiplier must be instance of (int, long, or float). '%s' given." % other.__class__.__name__)

    def __div__(self, other):
        if type(other) in (int, long, float):
            return self.__class__(operator.div(self.X, other),
                       operator.div(self.Y, other),
                       operator.div(self.Z, other))
        else:
            raise TypeError("Divider must be instance of (int, long, or float). '%s' given." % other.__class__.__name__)

    def __truediv__(self, other):
        if type(other) in (int, long, float):
            return self.__class__(operator.truediv(self.X, other),
                       operator.truediv(self.Y, other),
                       operator.truediv(self.Z, other))
        else:
            raise TypeError("Divider must be instance of (int, long, or float). '%s' given." % other.__class__.__name__)

    def __neg__(self):
        return self.__class__(-self.X,
                        -self.Y,
                        -self.Z)

    def __abs__(self):
        return math.sqrt(self.X ** 2 + \
                         self.Y ** 2 + \
                         self.Z ** 2)
    
    Magnitude = __abs__

    def MagnitudeSquared(self):
        return self.X ** 2 + \
               self.Y ** 2 + \
               self.Z ** 2

    def Normalize(self):
        d = self.Magnitude()
        if d:
            self.X /= d
            self.Y /= d
            self.Z /= d
        return self

    def Normalized(self):
        d = self.Magnitude()
        if d:
            return self.__class__(self.X / d, 
                           self.Y / d, 
                           self.Z / d)
        return self.Copy()

    def Dot(self, other):
        if isinstance(other, FBVector3d):
            return self.X * other.X + \
               self.Y * other.Y + \
               self.Z * other.Z
        else:
            raise TypeError("Object '%s' must be instance of FBVector3d." % other)

    def Cross(self, other):
        if isinstance(other, FBVector3d):
            return self.__class__(self.Y * other.Z - self.Z * other.Y,
                       -self.X * other.Z + self.Z * other.X,
                       self.X * other.Y - self.Y * other.X)
        else:
            raise TypeError("Object '%s' must be instance of FBVector3d." % other)
        
    def Reflect(self, normal):
        # assume normal is normalized
        if isinstance(normal, FBVector3d):
            d = 2 * (self.X * normal.X + self.Y * normal.Y + self.Z * normal.Z)
            return self.__class__(self.X - d * normal.X,
                       self.Y - d * normal.Y,
                       self.Z - d * normal.Z)
        else:
            raise TypeError("Object '%s' must be instance of FBVector3d." % normal)
    
    def Angle(self, other):
        '''Returns angle between two Vectors.'''
        if isinstance(normal, FBVector3d):
            q = self.Normalized().Dot(other.Normalized())
            if q < -1.0:
                return math.pi
            elif q > 1.0:
                return 0.0
            else:
                return math.acos(q)
        else:
            raise TypeError("Object '%s' must be instance of FBVector3d." % other)
    
    @property
    def X(self):
        return self[0]
    
    @X.setter
    def X(self, value):
        self[0] = value
    
    @property
    def Y(self):
        return self[1]
    
    @Y.setter
    def Y(self, value):
        self[1] = value
    
    @property
    def Z(self):
        return self[2]
    
    @Z.setter
    def Z(self, value):
        self[2] = value
    
    __pos__ = __copy__

# -----------------------------------------------------
# Integrations
# -----------------------------------------------------
# Set the these classes as the base class of the 
# MotionBuilder classes so they inherit the methods
# -----------------------------------------------------
def insertMathClasses():
    _baseClasses = list(FBMatrix.__bases__)
    if PMBMatrix not in _baseClasses:
        _baseClasses.insert(0, PMBMatrix)
        FBMatrix.__bases__ = tuple(_baseClasses)
    
    _baseClasses = list(FBVector3d.__bases__)
    if PMBVector3d not in _baseClasses:
        _baseClasses.insert(0, PMBVector3d)
        FBVector3d.__bases__ = tuple(_baseClasses)
    
    _baseClasses = list(FBVector2d.__bases__)
    if PMBVector2d not in _baseClasses:
        _baseClasses.insert(0, PMBVector2d)
        FBVector2d.__bases__ = tuple(_baseClasses)