from configparser import ConfigParser
import os 

config_file = os.path.join(os.path.dirname(__file__), 'config.ini')

def load():
    config = ConfigParser()
    config.read(config_file)

    global device_id;	           device_id = config.getint('Input', 'device_id')
    global axis_throttle;          axis_throttle = config.getint('Input', 'axis_throttle')
    global axis_throttle_invert;   axis_throttle_invert = config.getint('Input', 'axis_throttle_invert')
    global axis_throttle_combined; axis_throttle_combined = config.getint('Input', 'axis_throttle_combined')
    global axis_yaw;	           axis_yaw = config.getint('Input', 'axis_yaw')
    global axis_yaw_invert;        axis_yaw_invert = config.getint('Input', 'axis_yaw_invert')
    global axis_roll;	           axis_roll = config.getint('Input', 'axis_roll')
    global axis_roll_invert;       axis_roll_invert = config.getint('Input', 'axis_roll_invert')
    global axis_pitch;	           axis_pitch = config.getint('Input', 'axis_pitch')
    global axis_pitch_invert;      axis_pitch_invert = config.getint('Input', 'axis_pitch_invert')

    global roll_rate;	           roll_rate = config.getint('Rates', 'roll_rate') 
    global roll_expo;	           roll_expo = config.getint('Rates', 'roll_expo')
    global pitch_rate;	           pitch_rate = config.getint('Rates', 'pitch_rate')
    global pitch_expo;	           pitch_expo = config.getint('Rates', 'pitch_expo')
    global yaw_rate;	           yaw_rate = config.getint('Rates', 'yaw_rate')
    global yaw_expo;	           yaw_expo = config.getint('Rates', 'yaw_expo')

    global mass; 	               mass = config.getint('Physics', 'mass')
    global drag;		           drag = config.getint('Physics', 'drag')
    global power_to_weight;		   power_to_weight = config.getint('Physics', 'power_to_weight')
    global wingspan;		       wingspan = config.getint('Physics', 'wingspan')

    global cam_angle;	           cam_angle = config.getint('Drone', 'cam_angle')
    global cam_fov;                cam_fov = config.getint('Drone', 'cam_fov')

def save(*x):
    config = ConfigParser()
    config['Input'] = {
        'device_id': str(device_id),
        'axis_throttle': str(axis_throttle),
        'axis_throttle_invert': str(axis_throttle_invert),
        'axis_throttle_combined': str(axis_throttle_combined),
        'axis_yaw': str(axis_yaw),
        'axis_yaw_invert': str(axis_yaw_invert),
        'axis_roll': str(axis_roll),
        'axis_roll_invert': str(axis_roll_invert),
        'axis_pitch': str(axis_pitch),
        'axis_pitch_invert': str(axis_pitch_invert)
    }

    config['Rates'] = {
        'roll_rate': str(roll_rate),
        'roll_expo': str(roll_expo),
        'pitch_rate': str(pitch_rate),
        'pitch_expo': str(pitch_expo),
        'yaw_rate': str(yaw_rate),
        'yaw_expo': str(yaw_expo)
    }

    config['Physics'] = {
        'mass': str(mass),
        'drag': str(drag),
        'power_to_weight': str(power_to_weight),
        'wingspan': str(wingspan)
    }

    config['Drone'] = {
        'cam_angle': str(cam_angle),
        'cam_fov': str(cam_fov)
    }

    with open(config_file, 'w') as configfile:
        config.write(configfile)