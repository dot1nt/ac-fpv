import sys
import os
import platform

import ac
import acsys

import input
import drone
import config

config.load()
drone = drone.Drone()
joystick = input.Input()

def addSpinner(appWindow, name, val, scale, pos, callback):
    spinner = ac.addSpinner(appWindow, name)
    ac.setPosition(spinner, pos[0], pos[1])
    ac.setRange(spinner, scale[0], scale[1])
    ac.setSize(spinner, 100, 20)
    ac.setValue(spinner, val)
    ac.addOnValueChangeListener(spinner, callback)

# setup callbacks
for setting in config.s_rates + config.s_physics + config.s_drone:
    exec('def f_{0}(val): config.{0} = val'.format(setting))

def start(*x):
    if drone.running:
        ac.setCameraMode(2)
        drone.running = False
        ac.setText(b_start, "Start")
        drone.__init__()
    else:
        ac.setCameraMode(6)
        ac.setText(b_start, "Stop")
        drone.running = True
        drone.gyrodata.start()

def initApp():
    global l_speed
    global b_start

    appWindow = ac.newApp("ac-fpv")
    ac.setSize(appWindow, 340, 400)

    l_speed = ac.addLabel(appWindow, "Speed: 0 km/h | 0 m/s")
    ac.setPosition(l_speed, 120, 50)

    b_start = ac.addButton(appWindow, "Start")
    ac.setPosition(b_start, 10, 50)
    ac.setSize(b_start, 100, 22)
    ac.addOnClickedListener(b_start, start)

    addSpinner(appWindow, "Roll Rate", config.roll_rate, (1.0, 300.0), (10, 100), f_roll_rate)
    addSpinner(appWindow, "Pitch Rate", config.pitch_rate, (1.0, 300.0), (120, 100), f_pitch_rate)
    addSpinner(appWindow, "Yaw Rate", config.yaw_rate, (1.0, 300.0), (230, 100), f_yaw_rate)

    addSpinner(appWindow, "Roll Expo", config.roll_expo, (0.0, 100.0), (10, 150), f_roll_expo)
    addSpinner(appWindow, "Pitch Expo", config.pitch_expo, (0.0, 100.0), (120, 150), f_pitch_expo)
    addSpinner(appWindow, "Yaw Expo", config.yaw_expo, (0.0, 100.0), (230, 150), f_yaw_expo)

    addSpinner(appWindow, "Roll Super", config.roll_super, (0.0, 200.0), (10, 200), f_roll_super)
    addSpinner(appWindow, "Pitch Super", config.pitch_super, (0.0, 200.0), (120, 200), f_pitch_super)
    addSpinner(appWindow, "Yaw Super", config.yaw_super, (0.0, 200.0), (230, 200), f_yaw_super)

    addSpinner(appWindow, "Drag", config.drag, (1.0, 200.0), (10, 270), f_drag)
    addSpinner(appWindow, "Mass (g)", config.mass, (1.0, 5000.0), (120, 270), f_mass)
    addSpinner(appWindow, "Power-to-weight", config.power_to_weight, (1.0, 10.0), (230, 270), f_power_to_weight)
    
    addSpinner(appWindow, "Surface area", config.surface_area, (5,  2000), (10, 320), f_surface_area)
    addSpinner(appWindow, "Camera Angle", config.cam_angle, (0.0, 180.0), (120, 320), f_cam_angle)
    addSpinner(appWindow, "Camera FOV", config.cam_fov, (40.0, 150.0), (230, 320), f_cam_fov)

    b_save = ac.addButton(appWindow, "Save")
    ac.setSize(b_save, 100, 22)
    ac.setPosition(b_save, 120, 365)
    ac.addOnClickedListener(b_save, config.save)

def acMain(ac_version):
    initApp()

    return "ac-fpv"

def acUpdate(deltaT):
    if not drone.running:
        return

    drone.setFov(config.cam_fov)

    drone.getRot()
    drone.getPos()

    joystick.getAxis()

    drone.rotate(-joystick.roll, -joystick.pitch, -joystick.yaw, config.cam_angle, deltaT)
    drone.throttle(joystick.throttle)

    drone.physics(deltaT)

    ac.setText(l_speed, "Speed: {:.0f} km/h | {:.0f} m/s".format((drone.speed * 3.6), drone.speed))