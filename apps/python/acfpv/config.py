from configparser import ConfigParser
import os 

config_file = os.path.join(os.path.dirname(__file__), 'config.ini')

def load():
    config = ConfigParser()
    config.read(config_file)

    global device_id;	device_id = config.getint('Input', 'device_id')
    global scale;		scale = config.getint('Input', 'scale') 

    global roll_rate;	roll_rate = config.getint('Rates', 'roll_rate') 
    global roll_expo;	roll_expo = config.getint('Rates', 'roll_expo')
    global pitch_rate;	pitch_rate = config.getint('Rates', 'pitch_rate')
    global pitch_expo;	pitch_expo = config.getint('Rates', 'pitch_expo')
    global yaw_rate;	yaw_rate = config.getint('Rates', 'yaw_rate')
    global yaw_expo;	yaw_expo = config.getint('Rates', 'yaw_expo')

    global gravity; 	gravity = config.getint('Physics', 'gravity')
    global drag;		drag = config.getint('Physics', 'drag')

    global cam_angle;	cam_angle = config.getint('Drone', 'cam_angle')
    global cam_fov;     cam_fov = config.getint('Drone', 'cam_fov')

def save(*x):
    config = ConfigParser()
    config['Input'] = {
        'device_id': str(device_id),
        'scale': str(scale)
    }

    config['Rates'] = {
        'roll_rate': str(roll_rate),
        'roll_expo': str(roll_expo),
        'pitch_rate': str(pitch_rate),
        'pitch_expo': str(pitch_expo),
        'yaw_rate': str(yaw_rate),
        'yaw_expo': str(yaw_expo),
    }

    config['Physics'] = {
        'gravity': str(gravity),
        'drag': str(drag)
    }

    config['Drone'] = {
        'cam_angle': str(cam_angle),
        'cam_fov': str(cam_fov)
    }

    with open(config_file, 'w') as configfile:
        config.write(configfile)