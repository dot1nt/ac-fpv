import sys
import os
import platform

if platform.architecture()[0] == "64bit":
    sysdir = "stdlib64"
else:
    sysdir = "stdlib"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), sysdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

import ac
import acsys

from input import Input
import drone
import config

config.load()

drone = drone.Drone()
joystick = Input()

def addSpinner(appWindow, name, val, scale, pos, callback):
    spinner = ac.addSpinner(appWindow, name)
    ac.setPosition(spinner, pos[0], pos[1])
    ac.setRange(spinner, scale[0], scale[1])
    ac.setSize(spinner, 100, 20)
    ac.setValue(spinner, val)
    ac.addOnValueChangeListener(spinner, callback)

def f_roll_rate(val): config.roll_rate = val
def f_pitch_rate(val): config.pitch_rate = val
def f_yaw_rate(val): config.yaw_rate = val

def f_roll_expo(val): config.roll_expo = val
def f_pitch_expo(val): config.pitch_expo = val
def f_yaw_expo(val): config.yaw_expo = val

def f_scale(val): config.scale = val
def f_drag(val): config.drag = val
def f_gravity(val): config.gravity = val

def f_cam_angle(val): config.cam_angle = val

def initApp():
    appWindow = ac.newApp("ac-fpv")
    ac.setSize(appWindow, 340, 270)

    addSpinner(appWindow, "Roll Rate", config.roll_rate, (0.0, 100.0), (10, 50), f_roll_rate)
    addSpinner(appWindow, "Pitch Rate", config.pitch_rate, (0.0, 100.0), (120, 50), f_pitch_rate)
    addSpinner(appWindow, "Yaw Rate", config.yaw_rate, (0.0, 100.0), (230, 50), f_yaw_rate)

    addSpinner(appWindow, "Roll Expo", config.roll_expo, (0.0, 100.0), (10, 100), f_roll_expo)
    addSpinner(appWindow, "Pitch Expo", config.pitch_expo, (0.0, 100.0), (120, 100), f_pitch_expo)
    addSpinner(appWindow, "Yaw Expo", config.yaw_expo, (0.0, 100.0), (230, 100), f_yaw_expo)

    addSpinner(appWindow, "Throttle Scale", config.scale, (0.0, 200.0), (10, 150), f_scale)
    addSpinner(appWindow, "Drag", config.drag, (0.0, 100.0), (120, 150), f_drag)
    addSpinner(appWindow, "Gravity", config.gravity, (0.0, 100.0), (230, 150), f_gravity)

    addSpinner(appWindow, "Camera Angle", config.cam_angle, (0.0, 90.0), (10, 200), f_cam_angle)

    b_save = ac.addButton(appWindow, "Save")
    ac.setSize(b_save, 100, 20)
    ac.setPosition(b_save, 120, 240)
    ac.addOnClickedListener(b_save, config.save)

def acMain(ac_version):
    initApp()

    return "ac-fpv"

def acUpdate(deltaT):
    drone.getRot()
    drone.getPos()

    joystick.getAxis()
    joystick.rates()

    drone.roll(-joystick.roll)
    drone.pitch(-joystick.pitch)
    drone.yaw(-joystick.yaw)
    drone.throttle(joystick.throttle)

    drone.physics()

    drone.move()