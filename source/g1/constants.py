BAD_CONTACT_BODIES = [
    "pelvis",
    "torso_link",
]

ROOT_LINK_NAME = "torso_link"
TRACKED_EE_LINKS = [
    {
        "name": "l_foot",
        "body_name": "left_ankle_roll_link",
        "cmd_attr": "cmd_left_foot_pos",
    },
    {
        "name": "r_foot",
        "body_name": "right_ankle_roll_link",
        "cmd_attr": "cmd_right_foot_pos",
    },
]

FOOT_CONTACT_BODIES = [
    "left_ankle_roll_link",
    "right_ankle_roll_link",
]


SAMPLING_RANGE = {
    "left_foot_pos": [[-0.0, 0.15, 0.01], [0.0, 0.15, 0.3]],  # Lower limit, upper limit
    "right_foot_pos": [[0.0, -0.15, 0.01], [0.0, -0.15, 0.01]],
}

END_EFFECTORS = {
    "l_foot": {
        "body_name": "left_ankle_roll_link",
    },
    "r_foot": {
        "body_name": "right_ankle_roll_link",
    },
    "l_wrist": {
        "body_name": "left_palm_link",
    },
    "r_wrist": {
        "body_name": "right_palm_link",
    },
}
