import ac
import math
import config

def dot(v1, v2):
    a = v1[0]*v2[0][0] + v1[1]*v2[1][0] + v1[2]*v2[2][0]
    b = v1[0]*v2[0][1] + v1[1]*v2[1][1] + v1[2]*v2[2][1]
    c = v1[0]*v2[0][2] + v1[1]*v2[1][2] + v1[2]*v2[2][2]

    return (a,b,c)

def rot_to_vec(rot, val):
    r = rot[0]
    p = rot[1]
    y = rot[2]

    m_x = [ [1,                 0,              0], 
            [0,                 math.cos(r),    -math.sin(r)],
            [0,                 math.sin(r),    math.cos(r)]]

    m_y = [	[math.cos(p),       0,              math.sin(p)],
            [0,                 1,              0],
            [-math.sin(p),      0,              math.cos(p)]]

    m_z = [ [math.cos(y),       -math.sin(y),   0],
            [math.sin(y),       math.cos(y),    0],
            [0,                 0,              1]]

    vec = [0, 0, val]

    x = dot(vec, m_x)
    y = dot(x, m_y)
    z = dot(y, m_z)

    return z

def drag(val, drag):
    return val + val**2 * drag if val < 0 else val - val**2 * drag

class Drone:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
    
    def setFov(self, val):
        ac.ext_setCameraFov(float(val))

    def getPos(self):
        self.position = ac.ext_getCameraPosition()

    def getRot(self):
        roll = ac.ext_getCameraRollRad()
        pitch = ac.ext_getCameraPitchRad()
        yaw = ac.ext_getCameraYawRad()

        self.rotation = (roll, pitch, yaw)

    def roll(self, val):
        ac.freeCameraRotateRoll(val)

    def pitch(self, val):
        ac.freeCameraRotatePitch(val)

    def yaw(self, val):
        ac.freeCameraRotateHeading(val)

    def throttle(self, val):
        rot = list(self.rotation)

        if rot[0] > -1.57:
            rot[1] -= math.radians(config.cam_angle)
        else:
            rot[1] += math.radians(config.cam_angle)

        vec = rot_to_vec(rot, val)

        self.x += vec[0]
        self.y += -vec[1]
        self.z += vec[2]

    def physics(self, deltaT):
        _drag = config.drag * deltaT / 10
        gravity = config.gravity * deltaT / 1000

        self.x = drag(self.x, _drag)
        self.y = drag(self.y, _drag)
        self.z = drag(self.z, _drag)

        self.z -= gravity

    def move(self):

        pos = list(self.position)
        pos[2] += self.x
        pos[0] += self.y
        pos[1] += self.z

        ac.ext_setCameraPosition(tuple(pos))