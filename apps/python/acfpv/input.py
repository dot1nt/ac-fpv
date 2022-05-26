import os
import ac

import config

class Input:
    def getAxis(self):
        id = config.device_id

        self.throttle = ac.ext_getJoystickAxisValue(id, 0) + 1
        self.yaw = ac.ext_getJoystickAxisValue(id, 3)
        self.roll = ac.ext_getJoystickAxisValue(id, 1)
        self.pitch = ac.ext_getJoystickAxisValue(id, 2)

    def rates(self, deltaT):
        r = self.roll
        p = self.pitch
        y = self.yaw

        roll_rate = config.roll_rate * deltaT
        roll_expo = config.roll_expo * deltaT
        pitch_rate = config.pitch_rate * deltaT
        pitch_expo = config.pitch_expo * deltaT
        yaw_rate = config.yaw_rate * deltaT
        yaw_expo = config.yaw_expo * deltaT

        self.roll = (((1 - roll_expo) * r**3) + (roll_expo * r)) * roll_rate
        self.pitch = (((1 - pitch_expo) * p**3) + (pitch_expo * p)) * pitch_rate
        self.yaw = (((1 - yaw_expo) * y**3) + (yaw_expo * y)) * yaw_rate

        self.throttle *= config.scale * deltaT / 100