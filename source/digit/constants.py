BAD_CONTACT_BODIES = [
    "torso_base",
]

FOOT_CONTACT_BODIES = [
    "left_toe_roll",
    "right_toe_roll",
]

ROOT_LINK_NAME = "torso_base"

END_EFFECTORS = {
    "l_foot": {
        "body_name": "left_leg_toe_roll",
    },
    "r_foot": {
        "body_name": "right_leg_toe_roll",
    },
    "l_wrist": {
        "body_name": "left_arm_wrist_yaw",
    },
    "r_wrist": {
        "body_name": "right_arm_wrist_yaw",
    },
}
