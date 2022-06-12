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

def f_drag(val): config.drag = val
def f_mass(val): config.mass = val
def f_power_to_weight(val): config.power_to_weight = val
def f_wingspan(val): config.wingspan = val

def f_cam_angle(val): config.cam_angle = val
def f_cam_fov(val): config.cam_fov = val

def initApp():
    global speed_label

    appWindow = ac.newApp("ac-fpv")
    ac.setSize(appWindow, 340, 320)

    speed_label = ac.addLabel(appWindow, "Speed: 0 km/h | 0 m/s")
    ac.setPosition(speed_label, 10, 50)

    addSpinner(appWindow, "Roll Rate", config.roll_rate, (1.0, 50.0), (10, 100), f_roll_rate)
    addSpinner(appWindow, "Pitch Rate", config.pitch_rate, (1.0, 50.0), (120, 100), f_pitch_rate)
    addSpinner(appWindow, "Yaw Rate", config.yaw_rate, (1.0, 50.0), (230, 100), f_yaw_rate)

    addSpinner(appWindow, "Roll Expo", config.roll_expo, (0.0, 100.0), (10, 150), f_roll_expo)
    addSpinner(appWindow, "Pitch Expo", config.pitch_expo, (0.0, 100.0), (120, 150), f_pitch_expo)
    addSpinner(appWindow, "Yaw Expo", config.yaw_expo, (0.0, 100.0), (230, 150), f_yaw_expo)

    addSpinner(appWindow, "Drag", config.drag, (1.0, 200.0), (120, 200), f_drag)
    addSpinner(appWindow, "Mass (g)", config.mass, (1.0, 5000.0), (230, 200), f_mass)
    addSpinner(appWindow, "Power-to-weight", config.power_to_weight, (1.0, 10.0), (10, 200), f_power_to_weight)
    addSpinner(appWindow, "Wingspan (mm)", config.wingspan, (50,  1000), (10, 250), f_wingspan)

    addSpinner(appWindow, "Camera Angle", config.cam_angle, (0.0, 180.0), (120, 250), f_cam_angle)
    addSpinner(appWindow, "Camera FOV", config.cam_fov, (40.0, 150.0), (230, 250), f_cam_fov)

    b_save = ac.addButton(appWindow, "Save")
    ac.setSize(b_save, 100, 20)
    ac.setPosition(b_save, 120, 285)
    ac.addOnClickedListener(b_save, config.save)

def acMain(ac_version):
    initApp()

    return "ac-fpv"

def acUpdate(deltaT):
    if ac.getCameraMode() != 6:
        drone.__init__()
        return

    drone.setFov(config.cam_fov)

    drone.getRot()

    drone.getPos()

    joystick.getAxis()
    joystick.rates(deltaT)

    drone.roll(-joystick.roll)
    drone.pitch(-joystick.pitch)
    drone.yaw(-joystick.yaw)
    drone.throttle(joystick.throttle)

    drone.physics(deltaT)

    ac.setText(speed_label, "Speed: {:.0f} km/h | {:.0f} m/s".format((drone.speed * 3.6), drone.speed))