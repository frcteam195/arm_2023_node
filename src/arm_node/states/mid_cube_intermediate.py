import numpy

from arm_node.arm import Arm
from arm_node.positions import *
from arm_node.states.util import *
from arm_node.state_machine import ArmStateMachine

from ck_utilities_py_node.motor import *
from ck_utilities_py_node.solenoid import *
from ck_utilities_py_node.StateMachine import StateMachine

TRANSITIONS = [
    ArmStateMachine.States.MID_CUBE_FRONT,
    ArmStateMachine.States.MID_CUBE_BACK,
    ArmStateMachine.States.MID_CUBE_AUTO_FRONT,
    ArmStateMachine.States.MID_CUBE_AUTO_BACK,
]

class IntermediateMidCubeState(StateMachine.State):

    def __init__(self, machine, arm, side=ArmStateMachine.GoalSides.FRONT):
        self.machine: ArmStateMachine = machine
        self.arm: Arm = arm
        self.side: ArmStateMachine.GoalSides = side
        self.default_position: ArmPosition = POS_MID_CUBE_INTERMEDIATE

        if side is ArmStateMachine.GoalSides.BACK:
            self.default_position = mirror_position(self.default_position)

    def get_enum(self):
        if self.side is ArmStateMachine.GoalSides.FRONT:
            return ArmStateMachine.States.INTERMEDIATE_MID_CUBE_FRONT
        else:
            return ArmStateMachine.States.INTERMEDIATE_MID_CUBE_BACK

    def entry(self):
        self.arm.disable_brakes()
        self.arm.config_lower_arm_fast()
        if self.arm.is_retracted():
            self.arm.config_arm_fast()
        self.arm.retract()

    def step(self):
        self.arm.wrist_goal = WristPosition.Left_90
        self.arm.set_motion_magic(self.default_position)

    def transition(self) -> Enum:
        if self.arm.is_at_setpoint_raw(0.1, 0.1) and \
           self.side is ArmStateMachine.get_goal_side(self.machine.goal_state) and \
           self.machine.goal_state in TRANSITIONS:
            return self.machine.goal_state
        elif self.arm.is_at_setpoint_raw(0.06, 0.06) and self.machine.goal_state not in TRANSITIONS:
            return transition_to_intermediate(self.side is ArmStateMachine.GoalSides.FRONT)
        else:
            return self.get_enum()
