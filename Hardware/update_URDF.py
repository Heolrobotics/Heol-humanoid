import json

try:
    import xmltodict
except ImportError:
    raise ImportError('A module required is not installed on your system, please run this command in your terminal: pip install xmltodict')

from numpy import deg2rad


# Dynamixel torque limit (N.m)
DXL2EFFORT = {
    'MX-28': 3.1,
    'MX-64': 7.3,
    'AX-12': 1.8,
    'XL-320': 0.39
}

# Dynamixel velocity (rad/s)
DXL2VEL = {
    'MX-28': 7.,
    'MX-64': 8.2,
    'AX-12': 10.,
    'XL-320': 11.9
}

# Robot color
COLOR = '1 0.2 0.2 1.0'  # RGB Alpha

# Motor to not inverse rotation 
good_motors = ['l_hip_y','l_shoulder_motor_y','r_shoulder_motor_y','l_forearm_y','r_forearm_y','l_knee_x','l_foot_y','r_foot_y']


# Masses (kg)
MASS = {
    'pelvis': 0,
    'r_hip': 0,
    'r_hip_motor': 0,
    'r_thigh': 0,
    'r_shin': 0,
    'r_foot': 0,
    'l_hip': 0,
    'l_hip_motor': 0,
    'l_thigh': 0,
    'l_shin': 0,
    'l_foot': 0,
    'abs_motors': 0,
    'abdomen': 0,
    'spine': 0,
    'bust_motors': 0,
    'chest': 0,
    'neck': 0,
    'head': 0,
    'l_shoulder': 0,
    'l_shoulder_motor': 0,
    'l_upper_arm': 0,
    'l_forearm': 0,
    'r_shoulder': 0,
    'r_shoulder_motor': 0,
    'r_upper_arm': 0,
    'r_forearm': 0
}


def update_URDF_from_config(urdf_path, config_path):
    with open(urdf_path) as f:
        urdf = xmltodict.parse(f.read())

    with open(config_path) as f:
        conf = json.load(f)

    confmotors = conf['motors']
    joints = urdf['robot']['joint']
    links = urdf['robot']['link']

    # Update joint properties
    wrong_motors=[]
    for j in joints:
        name = j['@name']
        dxl = confmotors[name]['type']
        ll, ul = confmotors[name]['angle_limit']

        j['limit']['@lower'] = str(deg2rad(ll))
        j['limit']['@upper'] = str(deg2rad(ul))
        j['limit']['@effort'] = str(DXL2EFFORT[dxl])
        j['limit']['@velocity'] = str(DXL2VEL[dxl])
    
        # Update motors rotation    
        if name not in good_motors:
            list = j['axis']['@xyz'].split()
            new_list=[ '1' if i=='-1' else '-1' if i=='1' else i for i in list]
            j['axis']['@xyz']=' '.join(new_list)
            wrong_motors.append(name)
            
            
                
                

    
    # Update link properties
    for l in links:
        name = l['@name']
        mesh = l['visual']['geometry']['mesh']['@filename']
        if '_visual' not in mesh:
            pos = mesh.find('.')
            l['visual']['geometry']['mesh']['@filename'] = mesh[0:10]+mesh[24:pos]+'_visual.STL'
        mesh = l['collision']['geometry']['mesh']['@filename']
        if '_respondable' not in mesh:
            pos = mesh.find('.')
            l['collision']['geometry']['mesh']['@filename'] = mesh[0:10]+mesh[24:pos]+'_respondable.STL'

        l['visual']['material']['color']['@rgba'] = COLOR
        #l['mass'] = MASS[name]
        
    

    new_urdf = xmltodict.unparse(urdf, pretty=True)

    pos = urdf_path.find('.U')
    urdf_path_new = urdf_path[0:pos]+'_vrep.URDF'
    with open(urdf_path_new, 'w') as f:
        f.write(new_urdf)
        
    return wrong_motors


if __name__ == '__main__':

    urdf_path = './URDF/robots/Heol_Humanoid.URDF'
    config_path = '../software/heol_humanoid/configuration/heol_humanoid.json'
    

    wrong_motors=update_URDF_from_config(urdf_path, config_path)
    print("The URDF file has been updated")
    print("Motors axis changed for :")
    print wrong_motors
