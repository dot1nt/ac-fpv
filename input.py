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

    def rates(self):
        r = self.roll
        p = self.pitch
        y = self.yaw

        roll_rate = config.roll_rate / 100
        roll_expo = config.roll_expo / 100
        pitch_rate = config.pitch_rate / 100
        pitch_expo = config.pitch_expo / 100
        yaw_rate = config.yaw_rate / 100
        yaw_expo = config.yaw_expo / 100

        self.roll = (((1 - roll_expo) * r**3) + (roll_expo * r)) * roll_rate
        self.pitch = (((1 - pitch_expo) * p**3) + (pitch_expo * p)) * pitch_rate
        self.yaw = (((1 - yaw_expo) * y**3) + (yaw_expo * y)) * yaw_rate

        self.throttle *= config.scale / 10000