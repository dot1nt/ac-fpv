import ac
import math
import config
import time

def dot(v1, v2):
    a = v1[0]*v2[0][0] + v1[1]*v2[1][0] + v1[2]*v2[2][0]
    b = v1[0]*v2[0][1] + v1[1]*v2[1][1] + v1[2]*v2[2][1]
    c = v1[0]*v2[0][2] + v1[1]*v2[1][2] + v1[2]*v2[2][2]

    return (a,b,c)

def rotToVec(rot, val):
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

def drag(drag_coefficient, surface_area, air_density, velocity):
        return (drag_coefficient * surface_area * ((air_density * (velocity * abs(velocity))) / 2))

# https://www.desmos.com/calculator/xnjxq7rowq
def getRotSpeed(input, rate, expo, super_rate):
    rate /= 100
    expo /= 100
    super_rate /= 100

    p = 1 / (1 - (abs(input) * super_rate))
    q = input * abs(input)**3 * expo + input * (1 - expo)

    return math.radians((200 * q * rate) * p)


class GyroFlow:
    def __init__(self):
        self.filename = config.filename
        self.enabled = True if self.filename != "" else False

        self.t = 0

    def start(self):
        if not self.enabled:
            return

        timestamp = time.time()

        with open(self.filename, "w") as f:
            f.write("""GYROFLOW IMU LOG
version,1.1
orientation,ZyX
timestamp,{0}
tscale,{1}
gscale,1
t, gx, gy, gz
""".format(timestamp, 1/config.fps))

    def add(self, gx, gy, gz):
        if not self.enabled:
            return

        self.t += 1

        with open(self.filename, "a") as f:
            f.write("{}, {}, {}, {}\n".format(self.t, gx, gy, gz))


class Drone:
    def __init__(self):
        self.running = False

        self.position = [0, 0, 0]
        self.rotation = (0, 0, 0)
        self.velocity = (0, 0, 0)
        self.acceleration = (0, 0, 0)
        self.throttle_mag = (0, 0, 0)
        self.speed = 0  #speed (ms-1)

        self.gyrodata = GyroFlow()
    
    def setFov(self, val):
        ac.ext_setCameraFov(float(val))

    def getPos(self):
        cam_position = ac.ext_getCameraPosition()
        self.position[0] = cam_position[2]
        self.position[1] = cam_position[0]
        self.position[2] = cam_position[1]

    def getRot(self):
        roll = ac.ext_getCameraRollRad()
        pitch = ac.ext_getCameraPitchRad()
        yaw = ac.ext_getCameraYawRad()

        self.rotation = (roll, pitch, yaw)

    def rotate(self, roll_input, pitch_input, yaw_input, camera_angle, deltaT):
        roll_speed = getRotSpeed(roll_input, config.roll_rate, config.roll_expo, config.roll_super)
        pitch_speed = getRotSpeed(pitch_input, config.pitch_rate, config.pitch_expo, config.pitch_super)
        yaw_speed = getRotSpeed(yaw_input, config.yaw_rate, config.yaw_expo, config.yaw_super) 

        camera_angle_rad = math.radians(camera_angle)

        roll = roll_speed * math.cos(camera_angle_rad) - yaw_speed * math.sin(camera_angle_rad)
        pitch = pitch_speed
        yaw =  yaw_speed * math.cos(camera_angle_rad) + roll_speed * math.sin(camera_angle_rad)

        self.gyrodata.add(roll, pitch, yaw)

        ac.freeCameraRotateRoll(roll * deltaT)
        ac.freeCameraRotatePitch(pitch * deltaT)
        ac.freeCameraRotateHeading(yaw * deltaT)

    def throttle(self, val):
        rot = list(self.rotation)

        if math.degrees(rot[0]) > -90:
            rot[1] -= math.radians(config.cam_angle)
        else:
            rot[1] += math.radians(config.cam_angle)

        vec = rotToVec(rot, val)

        self.throttle_mag = (vec[0], vec[1], vec[2])

    def physics(self, deltaT):

        new_position = [0, 0, 0]

        force_gravity = (-config.gravity * (config.mass / 1000))
        force_drag = [0, 0, 0]
        force_throttle = [0, 0, 0]
        force_total = [0, 0, 0]

        new_accel = [0, 0, 0]
        new_velocity = [0, 0, 0]

        for a in range(len(self.position)):
            new_position[a] = self.position[a] + self.velocity[a] * deltaT
            force_drag[a] = drag((config.drag / 100), (config.surface_area / 10000), config.air_density, self.velocity[a])
            force_throttle[a] = self.throttle_mag[a] * (config.power_to_weight * -force_gravity)

        force_total[0] = -force_drag[0] + force_throttle[0]
        force_total[1] = -force_drag[1] + -force_throttle[1]
        force_total[2] = force_gravity - force_drag[2] + force_throttle[2]

        for a in range(len(self.position)):
            new_accel[a] = force_total[a] / (config.mass / 1000)
            new_velocity[a] = self.velocity[a] + (self.acceleration[a] + new_accel[a]) * deltaT
            self.position[a] = new_position[a]

        self.speed = math.sqrt(new_velocity[0]**2 + new_velocity[1]**2 + new_velocity[2]**2) #ms-1

        pos = (self.position[1], self.position[2], self.position[0])

        self.velocity = new_velocity
        self.acceleration = new_accel

        ac.ext_setCameraPosition(tuple(pos))