"""
Defines all the arm positions in degrees.
"""

from dataclasses import dataclass
import rospy

ALLOWED_DEVIATION_PCT = 0.05
BASE_ALLOWED_DEVIATION = abs(rospy.get_param("/arm_node/baseArmMaster_forwardSoftLimit") -
                             rospy.get_param("/arm_node/baseArmMaster_reverseSoftLimit")) * ALLOWED_DEVIATION_PCT
UPPER_ALLOWED_DEVIATION = abs(rospy.get_param("/arm_node/upperArmMaster_forwardSoftLimit") -
                              rospy.get_param("/arm_node/upperArmMaster_reverseSoftLimit")) * ALLOWED_DEVIATION_PCT


@dataclass
class ArmPosition:
    """
    Class containing the base and upper arm position.
    """
    base_position: float = 0.0
    upper_position: float = 0.0


POS_HOME = ArmPosition(0.0, 0.0)

POS_STEAL = ArmPosition(16.70, 82.08)  # Fake

POS_GROUND_CUBE = ArmPosition(8.06, 36.0)
POS_GROUND_CONE = ArmPosition(-1.55, 29.16)
POS_GROUND_DEAD_CONE = ArmPosition(12.74, 27.36)

POS_SHELF = ArmPosition(-14.98, 77.4)

POS_LOW_SCORE = ArmPosition(21.38, 40.68)
POS_MID_CUBE = ArmPosition(16.34, 83.88)
POS_HIGH_CUBE = ArmPosition(18.5, 117.0)
POS_MID_CONE = ArmPosition(17.06, 109.8)
POS_HIGH_CONE = ArmPosition(21.74, 128.88)

POS_INTERMEDIATE = ArmPosition(-16.41, 28.0)
POS_HIGH_INTERMEDIATE = ArmPosition(-16.41, 90.0)


def mirror_position(position: ArmPosition) -> ArmPosition:
    """
    Mirrors the provided position.
    """
    mirrored_base = 0 - position.base_position
    mirrored_upper = 0 - position.upper_position
    return ArmPosition(mirrored_base, mirrored_upper)


def rotation_to_angle(rotation: ArmPosition) -> ArmPosition:
    """
    Returns the arm position in degrees based on the provided rotation.
    """
    position = ArmPosition()
    position.base_position = rotation.base_position * 360.0
    position.upper_position = rotation.upper_position * 360.0
    return position
