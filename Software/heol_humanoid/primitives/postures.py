import time

from pypot.primitive import Primitive
from pypot.primitive.utils import Sinus, SimplePosture


class StandPosture(SimplePosture):
    @property
    def target_position(self):
        pos = dict([(m.name, 0.) for m in self.robot.motors])
        pos['l_thigh_x'] = pos['r_thigh_x'] = 90
        return pos


class Wave(Primitive):
    def setup(self):
        for m in self.robot.r_arm:
            m.compliant = False

    def run(self):
        self.robot.goto_position({
            'r_shoulder_x': 120,
            'r_shoulder_motor_y': 45,
            'r_upper_arm_z': 0,
            'r_forearm_y': 30,
            }, 1, wait=True)

        self.robot.r_forearm_y.moving_speed = 0
        s = Sinus(self.robot, 25., [self.robot.r_forearm_y], amp=50, offset=30, freq=0.75)
        s.start()
        time.sleep(3)
        s.stop()

        self.robot.goto_position({
            'r_shoulder_x': 0,
            'r_shoulder_motor_y': 0,
            'r_upper_arm_z': 0,
            'r_forearm_y': 0,
            }, 1, wait=True)
