from configparser import ConfigParser
import os 

config_file = os.path.join(os.path.dirname(__file__), 'config.ini')

s_inputs = ["device_id", "axis_roll", "axis_pitch", "axis_yaw", "axis_throttle",
            "axis_throttle_invert", "axis_roll_invert", "axis_pitch_invert", "axis_pitch_invert", "axis_yaw_invert", 
            "axis_throttle_combined"]

s_rates =  ["roll_rate", "roll_expo", "roll_super",
            "pitch_rate", "pitch_expo", "pitch_super",
            "yaw_rate", "yaw_expo", "yaw_super"]

s_physics = ["gravity", "air_density", "drag", "mass", "power_to_weight", "surface_area"]

s_drone = ["cam_fov", "cam_angle"]

def load():
    config = ConfigParser()
    config.read(config_file)

    for setting in s_inputs:
        exec('global {0}; {0} = config.getint("Input", "{0}")'.format(setting))
    
    for setting in s_rates:
        exec('global {0}; {0} = config.getint("Rates", "{0}")'.format(setting))

    for setting in s_physics:
        exec('global {0}; {0} = config.getfloat("Physics", "{0}")'.format(setting))

    for setting in s_drone:
        exec('global {0}; {0} = config.getfloat("Drone", "{0}")'.format(setting))

def save(*x):
    config = ConfigParser()

    config['Input'] = {}
    for setting in s_inputs:
        config['Input'][setting] = str(globals()[setting])

    config['Rates'] = {}
    for setting in s_rates:
        config['Rates'][setting] = str(globals()[setting])

    config['Physics'] = {}
    for setting in s_physics:
        config['Physics'][setting] = str(globals()[setting])

    config['Drone'] = {}
    for setting in s_drone:
        config['Drone'][setting] = str(globals()[setting])

    with open(config_file, 'w') as configfile:
        config.write(configfile)