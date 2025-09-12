MPCL = [
    [-1.25, 1.75],  # l_hip_pitch_joint
    [-0.12, 0.5],  # l_hip_roll_joint
    [-0.3, 0.6],  # l_thigh_joint
    [-0.65, 1.65],  # l_calf_joint
    [-0.5, 1.3],  # l_ankle_pitch_joint
    [-0.15, 0.15],  # l_ankle_roll_joint
    [-1.25, 1.75],  # r_hip_pitch_joint
    [-0.5, 0.12],  # r_hip_roll_joint
    [-0.6, 0.3],  # r_thigh_joint
    [-0.65, 1.65],  # r_calf_joint
    [-0.5, 1.3],  # r_ankle_pitch_joint
    [-0.15, 0.15],  # r_ankle_roll_joint
]


BAD_CONTACT_BODIES = [
    "base_link",
    "r_thigh_link",
    "l_thigh_link",
]


ROOT_LINK_NAME = "base_link"
TRACKED_EE_LINKS = [
    {
        "name": "l_foot",
        "body_name": "l_ankle_roll_link",
        "cmd_attr": "cmd_left_foot_pos",
    },
    {
        "name": "r_foot",
        "body_name": "r_ankle_roll_link",
        "cmd_attr": "cmd_right_foot_pos",
    },
]

SAMPLING_RANGE = {
    "left_foot_pos": [
        [-0.0, 0.15, 0.01],
        [0.0, 0.15, 0.14],
    ],  # Lower limit, upper limit
    "right_foot_pos": [[0.0, -0.15, 0.01], [0.0, -0.15, 0.01]],
}
