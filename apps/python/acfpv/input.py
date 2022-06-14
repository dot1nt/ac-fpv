import os
import ac
import math

import config

# https://www.desmos.com/calculator/xnjxq7rowq
def getRotSpeed(input, rate, expo, super_rate):
    rate /= 100
    expo /= 100
    super_rate /= 100

    p = 1 / (1 - (abs(input) * super_rate))
    q = input * abs(input)**3 * expo + input * (1 - expo)

    return math.radians((200 * q * rate) * p)

class Input:
    def getAxis(self):
        id = config.device_id

        self.throttle = ac.ext_getJoystickAxisValue(id, config.axis_throttle)

        self.yaw = ac.ext_getJoystickAxisValue(id, config.axis_yaw)
        self.roll = ac.ext_getJoystickAxisValue(id, config.axis_roll)
        self.pitch = ac.ext_getJoystickAxisValue(id, config.axis_pitch)

        self.roll = self.roll * -1 if config.axis_roll_invert else self.roll
        self.pitch = self.pitch * -1 if config.axis_pitch_invert else self.pitch
        self.yaw = self.yaw * -1 if config.axis_yaw_invert else self.yaw
        self.throttle = self.throttle * -1 if config.axis_throttle_invert else self.throttle

        self.throttle = self.throttle if config.axis_throttle_combined else (self.throttle + 1) * 0.5
        self.throttle = max(self.throttle, 0)

    def rates(self, deltaT):
        self.roll = getRotSpeed(self.roll, config.roll_rate, config.roll_expo, config.roll_super) * deltaT
        self.pitch = getRotSpeed(self.pitch, config.pitch_rate, config.pitch_expo, config.pitch_super) * deltaT
        self.yaw = getRotSpeed(self.yaw, config.yaw_rate, config.yaw_expo, config.yaw_super) * deltaT