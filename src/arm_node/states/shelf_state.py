from arm_node.arm import Arm
from arm_node.positions import *
from arm_node.states.util import *
from arm_node.state_machine import ArmStateMachine

from ck_utilities_py_node.motor import *
from ck_utilities_py_node.solenoid import *
from ck_utilities_py_node.StateMachine import StateMachine


class ShelfState(StateMachine.State):

    def __init__(self, machine, arm, is_front=True):
        self.machine: ArmStateMachine = machine
        self.arm: Arm = arm
        self.is_front = is_front

        self.position: ArmPosition = POS_SHELF
        if not is_front:
            self.position = mirror_position(self.position)

    def get_enum(self):
        if self.is_front:
            return ArmStateMachine.States.SHELF_FRONT
        else:
            return ArmStateMachine.States.SHELF_BACK

    def entry(self):
        self.arm.disable_brakes()
            
    def step(self):
        standard_step(self.arm, self.position)

    def transition(self) -> Enum:
        if self.machine.goal_state is not self.get_enum():
            return transition_to_intermediate(self.is_front)

        return self.get_enum()