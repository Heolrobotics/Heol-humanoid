# original author : Lappeyre Matthieu

import os

# Remove parts that should not be 3D printed:
JUNK = ['XL-320', 'Edison','SPU']

# sort and rename parts to be 3D printed
TRUNK_PARTS_FOLDER = 'trunk'
TRUNK_NAME_MAPPING = {

    'backpack-1':'backpack',
    'U_torso-1': 'IMU_support',
    'chest-1': 'chest',
    'chest-2': 'chest_down',
    'pelvis_spine_eq-1': 'pelvis_spine',
}

ARMS_PARTS_FOLDER = 'arms'
ARMS_NAME_MAPPING = {
    'hand-1': 'hand_left',
    'hand-2': 'hand_right',
    'shoulder-6' : 'shoulder',
}

LEGS_PARTS_FOLDER = 'legs'
LEGS_NAME_MAPPING = {
    'foot-1': 'foot',
    'hip_left-1': 'hip_left',
    'hip_main-1 equerre-1': 'equerre',
    'hip_right-1': 'hip_right',
    'leg-4' : 'leg',
    'dos-1' : 'dos',
    'Part1^pelvis-1.STL': 'renfort',
    'thighV0_1-1 arm_leg-1' : 'arm_leg',
    'thighV0_1-4 double_rotation-1': 'double_rotation',
    'thighV0_1-4 pelvis_spine-1': 'assem_foot',
}

HEAD_PARTS_FOLDER = 'head'
HEAD_NAME_MAPPING = {
    'down_head': 'down_head',
    'up_head': 'up_head',
}


def delete_stl_files(stl_folder_path, pattern_to_delete):
    exported_stl_files = os.listdir(stl_folder_path)

    for filename in exported_stl_files:
        for name in pattern_to_delete:
            if name in filename:
                # try:
                os.remove(os.path.join(stl_path, filename))
                print '{} removed'.format(filename)
                # except OSError:
                #     raise 'A problem occured during the removing of {}'.format(filename)


def rename_stl_files(stl_folder_path, name_mapping, dest_path=None, specific_folder=None):
    if dest_path is None:
        dest_path = '.'

    if specific_folder is None:
        specific_folder = '.'

    exported_stl_files = os.listdir(stl_folder_path)
    destination_path = os.path.join(stl_folder_path, dest_path, specific_folder)

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    for filename in exported_stl_files:
        for name, new_name in name_mapping.iteritems():
            if name in filename:
                # try:
                print '{} moved'.format(new_name)
                os.rename(os.path.join(stl_folder_path, filename), os.path.join(destination_path, new_name + '.STL'))
                # except OSError as err:
                #     print("OS error: {0}".format(err))

if __name__ == '__main__':
    RAW_STL_FOLDER = '.'
    OUTPUT_STL_FOLDER = 'STL_3D_printed_parts'

    stl_path = os.path.join('.', RAW_STL_FOLDER)

    delete_stl_files(stl_path, JUNK)

    rename_stl_files(stl_path, TRUNK_NAME_MAPPING, OUTPUT_STL_FOLDER, TRUNK_PARTS_FOLDER)
    rename_stl_files(stl_path, ARMS_NAME_MAPPING, OUTPUT_STL_FOLDER, ARMS_PARTS_FOLDER)
    rename_stl_files(stl_path, LEGS_NAME_MAPPING, OUTPUT_STL_FOLDER, LEGS_PARTS_FOLDER)
    rename_stl_files(stl_path, HEAD_NAME_MAPPING, OUTPUT_STL_FOLDER, HEAD_PARTS_FOLDER)

    delete_stl_files(stl_path, ['.STL', ])
