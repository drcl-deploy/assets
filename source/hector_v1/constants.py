import copy
from dataclasses import dataclass
from ..mot_params import *

NATURAL_FREQ = 10 * 2.0 * 3.1415926535  # 10Hz
DAMPING_RATIO = 2.0

STIFFNESS_A1 = ARMATURE_UNITREE_A1 * NATURAL_FREQ**2
STIFFNESS_A1_KNEE = ARMATURE_UNITREE_A1_KNEE * NATURAL_FREQ**2

DAMPING_A1 = 2.0 * DAMPING_RATIO * ARMATURE_UNITREE_A1 * NATURAL_FREQ
DAMPING_A1_KNEE = 2.0 * DAMPING_RATIO * ARMATURE_UNITREE_A1_KNEE * NATURAL_FREQ

JOINT_NAMES_EXPR = [
    "l_hip_yaw_joint",
    "r_hip_yaw_joint",
    "l_hip_roll_joint",
    "r_hip_roll_joint",
    "l_hip_pitch_joint",
    "r_hip_pitch_joint",
    "l_knee_joint",
    "r_knee_joint",
    "l_ankle_joint",
    "r_ankle_joint",
]

DEFAULT_JOINT_POS = {
    "l_hip_yaw_joint": 0.0,
    "r_hip_yaw_joint": 0.0,
    "l_hip_roll_joint": 0.0,
    "r_hip_roll_joint": 0.0,
    "l_hip_pitch_joint": 0.0,
    "r_hip_pitch_joint": 0.0,
    "l_knee_joint": 0.0,
    "r_knee_joint": 0.0,
    "l_ankle_joint": 0.0,
    "r_ankle_joint": 0.0,
}

STIFFNESS = {
    "l_hip_yaw_joint": STIFFNESS_A1,
    "r_hip_yaw_joint": STIFFNESS_A1,
    "l_hip_roll_joint": STIFFNESS_A1,
    "r_hip_roll_joint": STIFFNESS_A1,
    "l_hip_pitch_joint": STIFFNESS_A1,
    "r_hip_pitch_joint": STIFFNESS_A1,
    "l_knee_joint": STIFFNESS_A1_KNEE,  # kp*knee_gear_ratio^2
    "r_knee_joint": STIFFNESS_A1_KNEE,  # kp*knee_gear_ratio^2
    "l_ankle_joint": STIFFNESS_A1,
    "r_ankle_joint": STIFFNESS_A1,
}

DAMPING = {
    "l_hip_yaw_joint": DAMPING_A1,
    "r_hip_yaw_joint": DAMPING_A1,
    "l_hip_roll_joint": DAMPING_A1,
    "r_hip_roll_joint": DAMPING_A1,
    "l_hip_pitch_joint": DAMPING_A1,
    "r_hip_pitch_joint": DAMPING_A1,
    "l_knee_joint": DAMPING_A1_KNEE,  # kp*knee_gear_ratio^2
    "r_knee_joint": DAMPING_A1_KNEE,  # kp*knee_gear_ratio^2
    "l_ankle_joint": DAMPING_A1,
    "r_ankle_joint": DAMPING_A1,
}


EFFORT_LIMIT = {
    "l_hip_yaw_joint": ACTUATOR_UNITREE_A1.effort_limit,
    "r_hip_yaw_joint": ACTUATOR_UNITREE_A1.effort_limit,
    "l_hip_roll_joint": ACTUATOR_UNITREE_A1.effort_limit,
    "r_hip_roll_joint": ACTUATOR_UNITREE_A1.effort_limit,
    "l_hip_pitch_joint": ACTUATOR_UNITREE_A1.effort_limit,
    "r_hip_pitch_joint": ACTUATOR_UNITREE_A1.effort_limit,
    "l_knee_joint": ACTUATOR_UNITREE_A1_KNEE.effort_limit,  # kp*knee_gear_ratio^2
    "r_knee_joint": ACTUATOR_UNITREE_A1_KNEE.effort_limit,  # kp*knee_gear_ratio^2
    "l_ankle_joint": ACTUATOR_UNITREE_A1.effort_limit,
    "r_ankle_joint": ACTUATOR_UNITREE_A1.effort_limit,
}


VELOCITY_LIMIT = {
    "l_hip_yaw_joint": ACTUATOR_UNITREE_A1.velocity_limit,
    "r_hip_yaw_joint": ACTUATOR_UNITREE_A1.velocity_limit,
    "l_hip_roll_joint": ACTUATOR_UNITREE_A1.velocity_limit,
    "r_hip_roll_joint": ACTUATOR_UNITREE_A1.velocity_limit,
    "l_hip_pitch_joint": ACTUATOR_UNITREE_A1.velocity_limit,
    "r_hip_pitch_joint": ACTUATOR_UNITREE_A1.velocity_limit,
    "l_knee_joint": ACTUATOR_UNITREE_A1_KNEE.velocity_limit,  # kp*knee_gear_ratio^2
    "r_knee_joint": ACTUATOR_UNITREE_A1_KNEE.velocity_limit,  # kp*knee_gear_ratio^2
    "l_ankle_joint": ACTUATOR_UNITREE_A1.velocity_limit,
    "r_ankle_joint": ACTUATOR_UNITREE_A1.velocity_limit,
}

ARMATURE = {
    "l_hip_yaw_joint": ACTUATOR_UNITREE_A1.reflected_inertia,
    "r_hip_yaw_joint": ACTUATOR_UNITREE_A1.reflected_inertia,
    "l_hip_roll_joint": ACTUATOR_UNITREE_A1.reflected_inertia,
    "r_hip_roll_joint": ACTUATOR_UNITREE_A1.reflected_inertia,
    "l_hip_pitch_joint": ACTUATOR_UNITREE_A1.reflected_inertia,
    "r_hip_pitch_joint": ACTUATOR_UNITREE_A1.reflected_inertia,
    "l_knee_joint": ACTUATOR_UNITREE_A1_KNEE.reflected_inertia,  # kp*knee_gear_ratio^2
    "r_knee_joint": ACTUATOR_UNITREE_A1_KNEE.reflected_inertia,  # kp*knee_gear_ratio^2
    "l_ankle_joint": ACTUATOR_UNITREE_A1.reflected_inertia,
    "r_ankle_joint": ACTUATOR_UNITREE_A1.reflected_inertia,
}

# 0.25 * effort / stiffness, in the same per-joint dict style
ACTION_SCALE = {
    name: 0.25 * EFFORT_LIMIT[name] / STIFFNESS[name]
    for name in JOINT_NAMES_EXPR
    if name in EFFORT_LIMIT and name in STIFFNESS and STIFFNESS[name] != 0
}


MPCL = [
    # [-0.7900000214576721, 0.7900000214576721], # l_hip_yaw_joint
    # [-0.7900000214576721, 0.7900000214576721], # r_hip_yaw_joint
    # [-0.7900000214576721, 0.7900000214576721], # l_hip_roll_joint
    # [-0.7900000214576721, 0.7900000214576721], # r_hip_roll_joint
    [-0.523599, 0.523599],  # l_hip_yaw_joint
    [-0.523599, 0.523599],  # r_hip_yaw_joint
    [-0.349066, 0.7900000214576721],  # l_hip_roll_joint
    [-0.7900000214576721, 0.349066],  # r_hip_roll_joint
    [-1.0499999523162842, 1.1299999952316284],  # l_hip_pitch_joint
    [-1.0499999523162842, 1.1299999952316284],  # r_hip_pitch_joint
    [-1.74, 3.5],  # l_knee_joint, joint limits * knee_gear_ratio
    [-1.74, 3.5],  # r_knee_joint, joint limits * knee_gear_ratio
    [-1.5700000524520874, 0.7900000214576721],  # l_ankle_joint
    [-1.5700000524520874, 0.7900000214576721],  # r_ankle_joint
]

BAD_CONTACT_BODIES = [
    "torso",
    "l_hip",
    "r_hip",
    "l_hip2",
    "r_hip2",
    "l_thigh",
    "r_thigh",
]

FOOT_CONTACT_BODIES = [
    "l_toe",
    "r_toe",
]


ROOT_LINK_NAME = "torso"
TRACKED_EE_LINKS = [
    {"name": "l_foot", "body_name": "l_toe", "cmd_attr": "cmd_left_foot_pos"},
    {"name": "r_foot", "body_name": "r_toe", "cmd_attr": "cmd_right_foot_pos"},
]

SAMPLING_RANGE = {
    "left_foot_pos": [
        [-0.0, 0.15, 0.01],
        [0.0, 0.15, 0.22],
    ],  # Lower limit, upper limit
    "right_foot_pos": [[0.0, -0.15, 0.01], [0.0, -0.15, 0.01]],
}


END_EFFECTORS = {
    "l_foot": {
        "body_name": "l_toe",
        "actuated_joints": ["l_hip_yaw_joint", 
                            "r_hip_yaw_joint", 
                            "l_hip_pitch_joint", 
                            "l_knee_joint", 
                            "l_ankle_joint"
                            ],
        "links_in_chain": [
            "l_hip",
            "l_hip2",
            "l_thigh",
            "l_calf",
            "l_toe",
        ],
        "commanded_contact": True,
    },
    "r_foot": {
        "body_name": "r_toe",
        "actuated_joints": [
                            "r_hip_yaw_joint", 
                            "r_hip_roll_joint", 
                            "r_hip_pitch_joint", 
                            "r_knee_joint", 
                            "r_ankle_joint"
                            ],
        "links_in_chain": [
            "r_hip",
            "r_hip2",
            "r_thigh",
            "r_calf",
            "r_toe",
        ],
        "commanded_contact": True,
    },
}