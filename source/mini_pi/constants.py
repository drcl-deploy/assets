JOINT_NAMES_EXPR = [
    "r_hip_pitch_joint",
    "r_hip_roll_joint",
    "r_thigh_joint",
    "r_calf_joint",
    "r_ankle_pitch_joint",
    "r_ankle_roll_joint",
    "l_hip_pitch_joint",
    "l_hip_roll_joint",
    "l_thigh_joint",
    "l_calf_joint",
    "l_ankle_pitch_joint",
    "l_ankle_roll_joint",
]

DEFAULT_JOINT_POS = {
    "r_hip_pitch_joint":0.0,
    "r_hip_roll_joint":0.0,
    "r_thigh_joint":0.0,
    "r_calf_joint":0.0,
    "r_ankle_pitch_joint":0.0,
    "r_ankle_roll_joint":0.0,
    "l_hip_pitch_joint":0.0,
    "l_hip_roll_joint":0.0,
    "l_thigh_joint":0.0,
    "l_calf_joint":0.0,
    "l_ankle_pitch_joint":0.0,
    "l_ankle_roll_joint":0.0,
}

STIFFNESS = {
    "r_hip_pitch_joint":10.0,
    "r_hip_roll_joint":10.0,
    "r_thigh_joint":10.0,
    "r_calf_joint":10.0,
    "r_ankle_pitch_joint":10.0,
    "r_ankle_roll_joint":10.0,
    "l_hip_pitch_joint":10.0,
    "l_hip_roll_joint":10.0,
    "l_thigh_joint":10.0,
    "l_calf_joint":10.0,
    "l_ankle_pitch_joint":10.0,
    "l_ankle_roll_joint":10.0,
}

DAMPING = {
    "r_hip_pitch_joint":0.5,
    "r_hip_roll_joint":0.5,
    "r_thigh_joint":0.5,
    "r_calf_joint":0.5,
    "r_ankle_pitch_joint":0.5,
    "r_ankle_roll_joint":0.5,
    "l_hip_pitch_joint":0.5,
    "l_hip_roll_joint":0.5,
    "l_thigh_joint":0.5,
    "l_calf_joint":0.5,
    "l_ankle_pitch_joint":0.5,
    "l_ankle_roll_joint":0.5,
}

EFFORT_LIMIT = {
    "r_hip_pitch_joint":20.0,
    "r_hip_roll_joint":20.0,
    "r_thigh_joint":20.0,
    "r_calf_joint":20.0,
    "r_ankle_pitch_joint":20.0,
    "r_ankle_roll_joint":20.0,
    "l_hip_pitch_joint":20.0,
    "l_hip_roll_joint":20.0,
    "l_thigh_joint":20.0,
    "l_calf_joint":20.0,
    "l_ankle_pitch_joint":20.0,
    "l_ankle_roll_joint":20.0,
}

VELOCITY_LIMIT = {
    "r_hip_pitch_joint":20.0,
    "r_hip_roll_joint":20.0,
    "r_thigh_joint":20.0,
    "r_calf_joint":20.0,
    "r_ankle_pitch_joint":20.0,
    "r_ankle_roll_joint":20.0,
    "l_hip_pitch_joint":20.0,
    "l_hip_roll_joint":20.0,
    "l_thigh_joint":20.0,
    "l_calf_joint":20.0,
    "l_ankle_pitch_joint":20.0,
    "l_ankle_roll_joint":20.0,
}


ARMATURE = {
    "r_hip_pitch_joint":0.01,
    "r_hip_roll_joint":0.01,
    "r_thigh_joint":0.01,
    "r_calf_joint":0.01,
    "r_ankle_pitch_joint":0.01,
    "r_ankle_roll_joint":0.01,
    "l_hip_pitch_joint":0.01,
    "l_hip_roll_joint":0.01,
    "l_thigh_joint":0.01,
    "l_calf_joint":0.01,
    "l_ankle_pitch_joint":0.01,
    "l_ankle_roll_joint":0.01,
}


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

FOOT_CONTACT_BODIES = [
    "l_ankle_roll_link",
    "r_ankle_roll_link",
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
