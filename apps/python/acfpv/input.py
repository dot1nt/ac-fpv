import os
import ac

import config

class Input:
    def getAxis(self):
        id = config.device_id

        self.throttle = ac.ext_getJoystickAxisValue(id, config.axis_throttle)
        self.yaw = ac.ext_getJoystickAxisValue(id, config.axis_yaw)
        self.roll = ac.ext_getJoystickAxisValue(id, config.axis_roll)
        self.pitch = ac.ext_getJoystickAxisValue(id, config.axis_pitch)

        self.throttle = self.throttle * -1 if config.axis_throttle_invert > 0 else self.throttle
        self.yaw = self.yaw * -1 if config.axis_yaw_invert > 0 else self.yaw
        self.roll = self.roll * -1 if config.axis_roll_invert > 0 else self.roll
        self.pitch = self.pitch * -1 if config.axis_pitch_invert > 0 else self.pitch

        self.throttle = self.throttle if config.axis_throttle_combined > 0 else (self.throttle + 1) * 0.5
        self.throttle = max(self.throttle, 0)

    def rates(self, deltaT):
        self.roll = self.inputScale(self.roll, config.roll_expo, config.roll_rate) * deltaT
        self.pitch = self.inputScale(self.pitch, config.pitch_expo, config.pitch_rate) * deltaT
        self.yaw = self.inputScale(self.yaw, config.yaw_expo, config.yaw_rate) * deltaT

    def inputScale(self, input, exponent, rate):
        return (((1 - (exponent / 100)) * input**3) + ((exponent / 100) * input)) * rate