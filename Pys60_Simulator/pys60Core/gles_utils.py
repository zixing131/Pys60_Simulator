#
# ====================================================================
# gles_utils.py - Utility functions for OpenGL ES
#
# Ported from the C++ utils
#
# Copyright (c) 2006 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Desktop changes: Python 3 syntax; corrected fixed-point/vector math and TCameraX.
from gles import *
from math import *
import types

try:
    radians
except NameError:

    def radians(degrees):
        """Convert degrees to radians"""
        return degrees * (pi / 180)


try:
    degrees
except NameError:

    def degrees(radians):
        """Convert radians to degrees"""
        return radians * (180 / pi)


def int2fixed(i):
    """Convert an integer to fixed point"""
    return i << 16


def float2fixed(v):
    """Convert a float to fixed point"""
    return int(v * 65536.0)


def fixed2float(v):
    """Convert fixed to float"""
    return v * (1 / 65536.0)


def floats2fixed(values):
    """Convert a sequence of floats to fixed point"""
    return [float2fixed(v) for v in values]


def fixed_mul(a, b):
    """Multiply fixed values"""
    return (int(a) * int(b)) >> 16


def fixed_div(a, b):
    return int((int(a) << 16) / b)


class TVector:
    """A 3D vector that is represented by single-precision floating point x,y,z coordinates."""

    def __init__(self, aX=0.0, aY=0.0, aZ=0.0):
        self.iX = aX
        self.iY = aY
        self.iZ = aZ

    def __add__(self, other):
        # + operator
        return TVector(self.iX + other.iX, self.iY + other.iY, self.iZ + other.iZ)

    def __iadd__(self, other):
        # += operator
        ret = self + other
        self.iX = ret.iX
        self.iY = ret.iY
        self.iZ = ret.iZ
        return self

    def __sub__(self, other):
        # - operator
        return self + (other * -1)

    def __neg__(self):
        # -self operator
        return self * -1

    def __mul__(self, other):
        # * operator
        if isinstance(other, TVector):
            return self.iX * other.iX + self.iY * other.iY + self.iZ * other.iZ
        if type(other) in (float, int):
            return TVector(self.iX * other, self.iY * other, self.iZ * other)

    def Magnitude(self):
        # Calculate the magnitude of this vector. Standard trigonometric calculation:
        # sqrt(x**2 + y**2 + z**2)
        return sqrt(self * self)

    def Normalize(self):
        # Normalizes this vector, Panics if this vector = (0, 0, 0)
        magnitude = self.Magnitude()
        if magnitude == 0:
            return
        self.iX /= magnitude
        self.iY /= magnitude
        self.iZ /= magnitude

    def CrossProduct(aVector1, aVector2):
        # Computes the crossproduct of vector aVector1 and vector aVector2.
        iX = aVector1.iY * aVector2.iZ - aVector1.iZ * aVector2.iY
        iY = aVector1.iZ * aVector2.iX - aVector1.iX * aVector2.iZ
        iZ = aVector1.iX * aVector2.iY - aVector1.iY * aVector2.iX

        return TVector(iX, iY, iZ)


class TVectorx:
    """A 3D vector that is represented by fixed-point x,y,z coordinates."""

    def __init__(self, aX=0, aY=0, aZ=0):
        self.iX = int(aX)
        self.iY = int(aY)
        self.iZ = int(aZ)

    def __add__(self, other):
        # + operator
        return TVectorx(self.iX + other.iX, self.iY + other.iY, self.iZ + other.iZ)

    def __iadd__(self, other):
        # += operator
        ret = self + other
        self.iX = ret.iX
        self.iY = ret.iY
        self.iZ = ret.iZ
        return self

    def __sub__(self, other):
        # - operator
        return self + (other * int2fixed(-1))

    def __neg__(self):
        # -self operator
        return self * int2fixed(-1)

    def __mul__(self, other):
        # * operator
        if isinstance(other, TVectorx):
            return (
                fixed_mul(self.iX, other.iX)
                + fixed_mul(self.iY, other.iY)
                + fixed_mul(self.iZ, other.iZ)
            )
        if type(other) in (float, int):
            return TVectorx(
                fixed_mul(self.iX, other),
                fixed_mul(self.iY, other),
                fixed_mul(self.iZ, other),
            )
        else:
            raise TypeError("Unsupported type")

    def Magnitude(self):
        # Calculate the magnitude of this vector. Standard trigonometric calculation:
        # sqrt(x**2 + y**2 + z**2)
        src = fixed2float(self * self)
        # print src
        return float2fixed(sqrt(src))

    def Normalize(self):
        # Normalizes the vector by dividing each component with the length of the vector.
        magnitude = self.Magnitude()
        # print magnitude
        if magnitude == 0:
            return
        ret = self * float2fixed(1 / fixed2float(magnitude))
        self.iX = ret.iX
        self.iY = ret.iY
        self.iZ = ret.iZ

    def CrossProduct(aVector1, aVector2):
        # Computes the crossproduct of vector aVector1 and vector aVector2.
        iX = fixed_mul(aVector1.iY, aVector2.iZ) - fixed_mul(aVector1.iZ, aVector2.iY)
        iY = fixed_mul(aVector1.iZ, aVector2.iX) - fixed_mul(aVector1.iX, aVector2.iZ)
        iZ = fixed_mul(aVector1.iX, aVector2.iY) - fixed_mul(aVector1.iY, aVector2.iX)
        return TVectorx(iX, iY, iZ)


class FiniteStateMachine:
    # An abstraction of a finite state machine
    def __init__(self):
        self.iState = None
        self.iPrevState = None

    def SetState(self, aNewState):
        # Set the current state and trigger OnEnterState.
        if aNewState != -1:
            if aNewState != self.iState:
                if self.iPrevState != -1:
                    self.OnLeaveState(self.iState)
                self.iPrevState = self.iState
                self.iState = aNewState
                self.OnEnterState(self.iState)

    def OnLeaveState(self, aState):
        # Empty implementation
        pass

    def OnEnterState(self, iState):
        # Empty implementation
        pass


class TFlareConfig:
    # Index of the texture used by this element.
    # iIndex
    # Length scaling.
    # iLengthScale
    # Texture scaling.
    # iImageScale;
    pass


class CLensFlareEffect:
    # An abstraction of a lens flare effect.
    def __init__(
        self, aTextureNames, aFlareConfigs, aTextureManager, aScreenWidth, aScreenHeight
    ):
        raise NotImplementedError(
            "The upstream lens-flare helper depends on an absent TTexture/texture-manager implementation"
        )

        self.iFlareConfigs = aFlareConfigs
        # self.iFlareConfigCount = aFlareConfigCount

        self.iTextureManager = aTextureManager

        self.iCenterX = aScreenWidth >> 1
        self.iCenterY = aScreenHeight >> 1

    def DrawAt(self, aLightX, aLightY):
        # Renders the lens flare effect at a given screen coordinates.
        # Uses the CTextureManager::Blit, which in turn draws two triangles (forming
        # a single quad)

        # Computing the lens flare vector.
        DirX = aLightX - self.iCenterX
        DirY = aLightY - self.iCenterY

        # TReal Scale;
        # TReal BlitCenterX, BlitCenterY;
        # TReal BlitWidth_div_2, BlitHeight_div_2;

        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE)
        glEnable(GL_TEXTURE_2D)

        for i in range(len(self.iFlareConfigs)):
            TextureIndex = self.iFlareConfigs[i].iIndex
            Scale = self.iFlareConfigs[i].iLengthScale

            BlitCenterX = DirX * Scale + self.iCenterX
            BlitCenterY = DirY * Scale + self.iCenterY
            BlitWidth_div_2 = (
                self.iTextures[TextureIndex].iTextureWidth
                * self.iFlareConfigs[i].iImageScale
            ) / 4
            BlitHeight_div_2 = (
                self.iTextures[TextureIndex].iTextureHeight
                * self.iFlareConfigs[i].iImageScale
            ) / 4

            self.iTextureManager.Blit(
                self.iTextures[TextureIndex],
                (BlitCenterX - BlitWidth_div_2),
                (BlitCenterY - BlitHeight_div_2),
                (BlitCenterX + BlitWidth_div_2),
                (BlitCenterY + BlitHeight_div_2),
            )
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)


class T3DModel:
    # Abstraction of a 3D model, represented by a position vector and single-precision floating point Yaw, Pitch, Roll orientation
    def __init__(self, aPosition, aYaw, aPitch, aRoll):
        self.position = aPosition
        self.yaw = aYaw
        self.pitch = aPitch
        self.roll = aRoll

    def MakeWorldViewMatrix(aCamera, aPosition, aYaw=0, aPitch=0, aRoll=0):
        # Sets up a world + a view matrix.

        glMultMatrixf(aCamera.iViewMatrix)

        glTranslatef(
            aPosition.iX - aCamera.iPosition.iX,
            aPosition.iY - aCamera.iPosition.iY,
            aPosition.iZ - aCamera.iPosition.iZ,
        )
        if aRoll:
            glRotatef(aRoll, 0, 0, 1)
        if aYaw:
            glRotatef(aYaw, 0, 1, 0)
        if aPitch:
            glRotatef(aPitch, 1, 0, 0)

    MakeWorldViewMatrix = staticmethod(MakeWorldViewMatrix)

    def MakeBillboardWorldViewMatrix(aCamera, aPosition):
        # Sets up a billboard matrix, which is a matrix that rotates objects in such a
        # way that they always face the camera.
        # Refer to the billboard example to see how this method is used.

        # Set up a rotation matrix to orient the billboard towards the camera.
        Dir = aCamera.iLookAt - aCamera.iPosition

        # TReal Angle, SrcT, SrcB;

        SrcT = Dir.iZ
        SrcB = Dir.iX
        Angle = atan2(SrcT, SrcB)
        # The Yaw angle is computed in such a way that the object always faces the
        # camera.
        Angle = -(degrees(Angle) + 90)
        T3DModel.MakeWorldViewMatrix(aCamera, aPosition, Angle)

    MakeBillboardWorldViewMatrix = staticmethod(MakeBillboardWorldViewMatrix)


class T3DModelx:
    # Abstraction of a 3D model, represented by a position vector and fixed-point Yaw, Pitch, Roll orientation
    def __init__(
        self,
        aPosition=TVectorx(int2fixed(0), int2fixed(0), int2fixed(0)),
        aYaw=int2fixed(0),
        aPitch=int2fixed(0),
        aRoll=int2fixed(0),
    ):
        # Constructs and initializes a T3DModelx to position aPosition, with
        # orientation [aYaw, aPitch, aRoll].
        self.position = aPosition
        self.yaw = aYaw
        self.pitch = aPitch
        self.roll = aRoll

    def MakeWorldViewMatrix(aCamera, aPosition, aYaw=0, aPitch=0, aRoll=0):
        # Sets up a world + a view matrix.

        glMultMatrixx(aCamera.iViewMatrix)

        glTranslatex(
            aPosition.iX - aCamera.iPosition.iX,
            aPosition.iY - aCamera.iPosition.iY,
            aPosition.iZ - aCamera.iPosition.iZ,
        )
        if aRoll != int2fixed(0):
            glRotatex(aRoll, int2fixed(0), int2fixed(0), int2fixed(1))
        if aYaw != int2fixed(0):
            glRotatex(aYaw, int2fixed(0), int2fixed(1), int2fixed(0))
        if aPitch != int2fixed(0):
            glRotatex(aPitch, int2fixed(1), int2fixed(0), int2fixed(0))

    MakeWorldViewMatrix = staticmethod(MakeWorldViewMatrix)

    def MakeBillboardWorldViewMatrix(aCamera, aPosition):
        # Sets up a billboard matrix, which is a matrix that rotates objects in such a
        # way that they always face the camera.
        # Refer to the billboard example to see how this method is used.

        # if not aPosition:
        #  aPosition = self.position

        # Set up a rotation matrix to orient the billboard towards the camera.
        Dir = aCamera.iLookAt - aCamera.iPosition

        # TReal Angle, SrcT, SrcB;
        # return
        SrcT = fixed2float(Dir.iZ)
        SrcB = fixed2float(Dir.iX)
        angle = atan2(SrcT, SrcB)
        # The Yaw angle is computed in such a way that the object always faces the camera.
        angle = -(degrees(angle) + 90)
        T3DModelx.MakeWorldViewMatrix(aCamera, aPosition, float2fixed(angle))

    MakeBillboardWorldViewMatrix = staticmethod(MakeBillboardWorldViewMatrix)


class TCamera:
    # Abstraction of a Camera in 3D space.
    #
    # The camera is represented by the eye point, the reference point, and the up vector.
    # This class is very useful since it provides an implementation of the gluLookAt method
    # which is not part of the OpenGL ES specification.
    def __init__(
        self,
        aPosition=TVector(0, 0, 0),
        aLookAt=TVector(0, 0, -1),
        aUp=TVector(0, 1, 0),
    ):
        self.iViewMatrix = []
        self.LookAt(aPosition, aLookAt, aUp)

    def LookAt(self, aPosition, aLookAt, aUp):
        # Initializes a TCamera to aPosition, aLookAt, aUp.
        # TVector XAxis, YAxis, ZAxis;

        self.iPosition = aPosition
        self.iLookAt = aLookAt
        self.iUp = aUp

        # Get the z basis vector, which points straight ahead; the
        # difference from the position (eye point) to the look-at point.
        # This is the direction of the gaze (+z).
        ZAxis = self.iLookAt - self.iPosition

        # Normalize the z basis vector.
        ZAxis.Normalize()

        # Compute the orthogonal axes from the cross product of the gaze
        # and the Up vector.
        # print ZAxis
        # print self.iUp
        if isinstance(ZAxis, TVectorx):
            XAxis = TVectorx.CrossProduct(ZAxis, self.iUp)
        elif isinstance(ZAxis, TVector):
            XAxis = TVector.CrossProduct(ZAxis, self.iUp)
        XAxis.Normalize()
        if isinstance(ZAxis, TVectorx):
            YAxis = TVectorx.CrossProduct(XAxis, ZAxis)
        if isinstance(ZAxis, TVector):
            YAxis = TVector.CrossProduct(XAxis, ZAxis)
        # Start building the matrix. The first three rows contain the
        # basis vectors used to rotate the view to point at the look-at point.
        self.MakeIdentity()

        self.iViewMatrix[0][0] = XAxis.iX
        self.iViewMatrix[1][0] = XAxis.iY
        self.iViewMatrix[2][0] = XAxis.iZ

        self.iViewMatrix[0][1] = YAxis.iX
        self.iViewMatrix[1][1] = YAxis.iY
        self.iViewMatrix[2][1] = YAxis.iZ

        self.iViewMatrix[0][2] = -ZAxis.iX
        self.iViewMatrix[1][2] = -ZAxis.iY
        self.iViewMatrix[2][2] = -ZAxis.iZ

    def MakeIdentity(self):
        self.iViewMatrix = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]


class TCameraX(TCamera):
    """Fixed-point view matrix with the same orientation as TCamera."""

    def __init__(self, aPosition=None, aLookAt=None, aUp=None):
        self.LookAt(
            aPosition or TVectorx(),
            aLookAt or TVectorx(0, 0, -65536),
            aUp or TVectorx(0, 65536, 0),
        )

    def LookAt(self, aPosition, aLookAt, aUp):
        convert = lambda v: TVector(
            fixed2float(v.iX), fixed2float(v.iY), fixed2float(v.iZ)
        )
        floating = TCamera(convert(aPosition), convert(aLookAt), convert(aUp))
        self.iPosition, self.iLookAt, self.iUp = aPosition, aLookAt, aUp
        self.iViewMatrix = [floats2fixed(row) for row in floating.iViewMatrix]

    def MakeIdentity(self, aMatrix=None):
        result = [
            [65536 if row == column else 0 for column in range(4)] for row in range(4)
        ]
        self.iViewMatrix = result
        if aMatrix is not None:
            aMatrix[:] = [item for row in result for item in row]
            return aMatrix
        return result


class TParticle:
    # This structure is used by the class CParticleEngine.
    # It is an abstraction of a particle.
    # Position
    # TVector iPosition
    # Velocity
    # TVector iVelocity
    # Acceleration
    # TVector iAcceleration
    # Empty implementation
    pass


class CParticleEngine:
    # Abstraction of a particle engine.
    # Particles engines are used to create special effects like Rain, Smoke, Snow, Sparks, etc...
    def __init__(self, aParticlesCount, aPosition):
        # Constructs a CParticleEngine object with aParticlesCount particles at
        # position aPosition.
        self.iParticlesCount = aParticlesCount
        self.iParticles = [TParticle() for x in range(self.iParticlesCount)]

        self.position = aPosition

    def ResetEngine(self):
        # Resets the particle engine
        for p in self.iParticles:
            self.ResetParticle(p)

    def ResetParticle(self, aIndex):
        # Resets the particle at index aIndex
        pass

    def UpdateEngine(self, aElapsedTime):
        # Updates the engine.
        pass

    def RenderEngine(self, aCamera):
        # Renders the system.
        pass


class Utils:
    # A set of useful functions.
    pass
