import os
import sys
import numpy
import ctypes

from functools import partial

from poppy.creatures import AbstractPoppyCreature

from .primitives.postures import StandPosture, Wave


class HeolHumanoid(AbstractPoppyCreature):
    @classmethod
    def setup(cls, robot):
        robot.attach_primitive(StandPosture(robot, 2.), 'stand')
        robot.attach_primitive(Wave(robot), 'wave')
    
        if robot.simulated:
            cls.vrep_hack(robot)
            cls.add_vrep_methods(robot)
        
     

    @classmethod
    def vrep_hack(cls, robot):
        # fix vrep orientation bug
        wrong_motor = [robot.l_hip_motor_z, robot.l_thigh_x, robot.l_ankle_x, robot.r_hip_y, robot.r_hip_motor_z, robot.r_thigh_x, robot.r_ankle_x, robot.spine_z, robot.chest_x,  robot.r_shoulder_x, robot.head_z,robot.r_shoulder_motor_y,robot.l_shoulder_motor_y, robot.l_forearm_y, robot.r_forearm_y]
        
        for m in wrong_motor:
            m.direct = not m.direct
            m.offset = -m.offset
            
    @classmethod
    def add_vrep_methods(cls, robot):
        from pypot.vrep.controller import VrepController
        from pypot.vrep.io import remote_api

        def set_vrep_force(robot, vector_force, shape_name):
            """ Set a force to apply on the robot. """
            vrep_io = next(c for c in robot._controllers
                           if isinstance(c, VrepController)).io

            raw_bytes = (ctypes.c_ubyte * len(shape_name)).from_buffer_copy(shape_name)
            vrep_io.call_remote_api('simxSetStringSignal', 'shape',
                                    raw_bytes, sending=True)

            packedData = remote_api.simxPackFloats(vector_force)
            raw_bytes = (ctypes.c_ubyte * len(packedData)).from_buffer_copy(packedData)
            vrep_io.call_remote_api('simxSetStringSignal', 'force',
                                    raw_bytes, sending=True)

        robot.set_vrep_force = partial(set_vrep_force, robot)