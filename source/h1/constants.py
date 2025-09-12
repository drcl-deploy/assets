BAD_CONTACT_BODIES = [
    "pelvis",
    "torso_link",
    "left_hip_roll_link",
    "right_hip_roll_link",
]

ROOT_LINK_NAME = "torso_link"
TRACKED_EE_LINKS = [
    {"name": "l_foot", "body_name": "left_ankle_link", "cmd_attr": "cmd_left_foot_pos"},
    {
        "name": "r_foot",
        "body_name": "right_ankle_link",
        "cmd_attr": "cmd_right_foot_pos",
    },
]

SAMPLING_RANGE = {
    "left_foot_pos": [[-0.0, 0.15, 0.01], [0.0, 0.15, 0.4]],  # Lower limit, upper limit
    "right_foot_pos": [[0.0, -0.15, 0.01], [0.0, -0.15, 0.1]],
}
