JOINT_NAMES_EXPR = [
    "left_hip_yaw_joint",
    "right_hip_yaw_joint",
    "left_hip_roll_joint",
    "right_hip_roll_joint",
    "left_hip_pitch_joint",
    "right_hip_pitch_joint",
    "left_knee_joint",
    "right_knee_joint",
    "left_calf_joint",
    "right_calf_joint",
    "left_ankle_joint",
    "right_ankle_joint",
]

DEFAULT_JOINT_POS = {
    "left_hip_yaw_joint": 0.0,  # 0
    "right_hip_yaw_joint": 0.0,  # 6
    "left_hip_roll_joint": 0.0,  # 1
    "right_hip_roll_joint": 0.0,  # 7
    "left_hip_pitch_joint": -0.4,  # 2
    "right_hip_pitch_joint": -0.4,  # 8
    "left_knee_joint": 0.5,  # 3
    "right_knee_joint": 0.5,  # 14
    "left_calf_joint": 0.1,  # 4
    "right_calf_joint": 0.1,  # 9
    "left_ankle_joint": -0.3,  # 5
    "right_ankle_joint": -0.3,  # 10
}

STIFFNESS = {
    "left_hip_yaw_joint": 10.0,
    "right_hip_yaw_joint": 10.0,
    "left_hip_roll_joint": 10.0,
    "right_hip_roll_joint": 10.0,
    "left_hip_pitch_joint": 10.0,
    "right_hip_pitch_joint": 10.0,
    "left_knee_joint": 10.0,
    "right_knee_joint": 10.0,
    "left_calf_joint": 10.0,
    "right_calf_joint": 10.0,
    "left_ankle_joint": 10.0,
    "right_ankle_joint": 10.0,
}

DAMPING = {
    "left_hip_yaw_joint": 1.0,
    "right_hip_yaw_joint": 1.0,
    "left_hip_roll_joint": 1.0,
    "right_hip_roll_joint": 1.0,
    "left_hip_pitch_joint": 1.0,
    "right_hip_pitch_joint": 1.0,
    "left_knee_joint": 1.0,
    "right_knee_joint": 1.0,
    "left_calf_joint": 1.0,
    "right_calf_joint": 1.0,
    "left_ankle_joint": 1.0,
    "right_ankle_joint": 1.0,
}

EFFORT_LIMIT = {
    "left_hip_yaw_joint": 17.0,
    "right_hip_yaw_joint": 17.0,
    "left_hip_roll_joint": 17.0,
    "right_hip_roll_joint": 17.0,
    "left_hip_pitch_joint": 17.0,
    "right_hip_pitch_joint": 17.0,
    "left_knee_joint": 17.0,
    "right_knee_joint": 17.0,
    "left_calf_joint": 17.0,
    "right_calf_joint": 17.0,
    "left_ankle_joint": 17.0,
    "right_ankle_joint": 17.0,
}

VELOCITY_LIMIT = {
    "left_hip_yaw_joint": 22.0,
    "right_hip_yaw_joint": 22.0,
    "left_hip_roll_joint": 22.0,
    "right_hip_roll_joint": 22.0,
    "left_hip_pitch_joint": 22.0,
    "right_hip_pitch_joint": 22.0,
    "left_knee_joint": 22.0,
    "right_knee_joint": 22.0,
    "left_calf_joint": 22.0,
    "right_calf_joint": 22.0,
    "left_ankle_joint": 22.0,
    "right_ankle_joint": 22.0,
}

BAD_CONTACT_BODIES = [
    "body",
    "left_hip1",
    "right_hip1",
    "left_hip2",
    "right_hip2",
    "left_bracket_link",
    "right_bracket_link",
]

FOOT_CONTACT_BODIES = [
    "left_ankle_link",
    "right_ankle_link",
]

# Robstride 02, TODO: Consider couping on ankle, knee
ARMATURE = {
    "left_hip_yaw_joint": 0.00414,
    "right_hip_yaw_joint": 0.00414,
    "left_hip_roll_joint": 0.00414,
    "right_hip_roll_joint": 0.00414,
    "left_hip_pitch_joint": 0.00414,
    "right_hip_pitch_joint": 0.00414,
    "left_knee_joint": 0.00414,
    "right_knee_joint": 0.00414,
    "left_calf_joint": 0.00414,
    "right_calf_joint": 0.00414,
    "left_ankle_joint": 0.00414,
    "right_ankle_joint": 0.00414,
}

MPCL = [
    [-1.57, 1.57],  # l_hip_yaw_joint
    [-1.57, 1.57],  # r_hip_yaw_joint
    [-1.0, 1.0],  # l_hip_roll_joint
    [-1.0, 1.0],  # r_hip_roll_joint
    [-1.0, 2.57],  # l_hip_pitch_joint
    [-1.0, 2.57],  # r_hip_pitch_joint
    [0.1, 1.57],  # l_knee_joint
    [0.1, 1.57],  # r_knee_joint
    [-1.57, 1.57],  # l_calf_joint
    [-1.57, 1.57],  # r_calf_joint
    [-2.0, 2.0],  # l_ankle_joint
    [-2.0, 2.0],  # r_ankle_joint
]


ROOT_LINK_NAME = "body"
TRACKED_EE_LINKS = [
    {"name": "l_foot", "body_name": "left_ankle_link", "cmd_attr": "cmd_left_foot_pos"},
    {
        "name": "r_foot",
        "body_name": "right_ankle_link",
        "cmd_attr": "cmd_right_foot_pos",
    },
]

SAMPLING_RANGE = {
    "left_foot_pos": [[-0.0, 0.15, 0.01], [0.0, 0.15, 0.2]],  # Lower limit, upper limit
    "right_foot_pos": [[0.0, -0.15, 0.01], [0.0, -0.15, 0.01]],
}

END_EFFECTORS = {
    "l_foot": {
        "body_name": "left_ankle_link",
        "actuated_joints": ["left_hip_yaw_joint", 
                            "left_hip_roll_joint", 
                            "left_hip_roll_joint", 
                            "left_knee_joint", 
                            "left_calf_joint",
                            "left_ankle_joint",
                            ],
        "links_in_chain": [
            "left_hip1",
            "left_hip2",
            "left_hip_pitch_joint",
            "left_bracket_link",
            "left_calf_link",
            "left_ankle_link",
        ],
        "commanded_contact": True,
    },
    "r_foot": {
        "body_name": "right_ankle_link",
        "actuated_joints": [
                            "right_hip_yaw_joint", 
                            "right_hip_roll_joint", 
                            "right_hip_pitch_joint", 
                            "right_knee_joint", 
                            "right_calf_joint", 
                            "right_ankle_joint"
                            ],
        "links_in_chain": [
            "right_hip1",
            "right_hip2",
            "right_hip_pitch_joint",
            "right_bracket_link",
            "right_calf_link",
            "right_ankle_link",
        ],
        "commanded_contact": True,
    },
}