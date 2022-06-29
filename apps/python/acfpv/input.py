import os
import ac
import math

import config

class Input:
    def getAxis(self):
        id = config.device_id

        self.throttle = ac.ext_getJoystickAxisValue(id, config.axis_throttle)
        self.roll = ac.ext_getJoystickAxisValue(id, config.axis_roll)
        self.pitch = ac.ext_getJoystickAxisValue(id, config.axis_pitch)
        self.yaw = ac.ext_getJoystickAxisValue(id, config.axis_yaw)

        self.throttle = self.throttle * -1 if config.axis_throttle_invert else self.throttle
        self.roll = self.roll * -1 if config.axis_roll_invert else self.roll
        self.pitch = self.pitch * -1 if config.axis_pitch_invert else self.pitch
        self.yaw = self.yaw * -1 if config.axis_yaw_invert else self.yaw
        
        self.throttle = self.throttle if config.axis_throttle_combined else (self.throttle + 1) * 0.5
        self.throttle = max(self.throttle, 0)