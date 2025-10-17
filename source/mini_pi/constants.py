import copy
from dataclasses import dataclass
from ..actuator_params import *

NATURAL_FREQ = 10 * 2.0 * 3.1415926535  # 10Hz
DAMPING_RATIO = 2.0

STIFFNESS_504736NE = ARMATURE_504736NE * NATURAL_FREQ**2

DAMPING_504736NE = 2.0 * DAMPING_RATIO * ARMATURE_504736NE * NATURAL_FREQ

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
    "r_hip_pitch_joint":STIFFNESS_504736NE,
    "r_hip_roll_joint":STIFFNESS_504736NE,
    "r_thigh_joint":STIFFNESS_504736NE,
    "r_calf_joint":STIFFNESS_504736NE,
    "r_ankle_pitch_joint":STIFFNESS_504736NE,
    "r_ankle_roll_joint":STIFFNESS_504736NE,
    "l_hip_pitch_joint":STIFFNESS_504736NE,
    "l_hip_roll_joint":STIFFNESS_504736NE,
    "l_thigh_joint":STIFFNESS_504736NE,
    "l_calf_joint":STIFFNESS_504736NE,
    "l_ankle_pitch_joint":STIFFNESS_504736NE,
    "l_ankle_roll_joint":STIFFNESS_504736NE,
}

DAMPING = {
    "r_hip_pitch_joint":DAMPING_504736NE,
    "r_hip_roll_joint":DAMPING_504736NE,
    "r_thigh_joint":DAMPING_504736NE,
    "r_calf_joint":DAMPING_504736NE,
    "r_ankle_pitch_joint":DAMPING_504736NE,
    "r_ankle_roll_joint":DAMPING_504736NE,
    "l_hip_pitch_joint":DAMPING_504736NE,
    "l_hip_roll_joint":DAMPING_504736NE,
    "l_thigh_joint":DAMPING_504736NE,
    "l_calf_joint":DAMPING_504736NE,
    "l_ankle_pitch_joint":DAMPING_504736NE,
    "l_ankle_roll_joint":DAMPING_504736NE,
}

EFFORT_LIMIT = {
    "r_hip_pitch_joint":ACTUATOR_504736NE.effort_limit,
    "r_hip_roll_joint":ACTUATOR_504736NE.effort_limit,
    "r_thigh_joint":ACTUATOR_504736NE.effort_limit,
    "r_calf_joint":ACTUATOR_504736NE.effort_limit,
    "r_ankle_pitch_joint":ACTUATOR_504736NE.effort_limit,
    "r_ankle_roll_joint":ACTUATOR_504736NE.effort_limit,
    "l_hip_pitch_joint":ACTUATOR_504736NE.effort_limit,
    "l_hip_roll_joint":ACTUATOR_504736NE.effort_limit,
    "l_thigh_joint":ACTUATOR_504736NE.effort_limit,
    "l_calf_joint":ACTUATOR_504736NE.effort_limit,
    "l_ankle_pitch_joint":ACTUATOR_504736NE.effort_limit,
    "l_ankle_roll_joint":ACTUATOR_504736NE.effort_limit,
}

VELOCITY_LIMIT = {
    "r_hip_pitch_joint":ACTUATOR_504736NE.velocity_limit,
    "r_hip_roll_joint":ACTUATOR_504736NE.velocity_limit,
    "r_thigh_joint":ACTUATOR_504736NE.velocity_limit,
    "r_calf_joint":ACTUATOR_504736NE.velocity_limit,
    "r_ankle_pitch_joint":ACTUATOR_504736NE.velocity_limit,
    "r_ankle_roll_joint":ACTUATOR_504736NE.velocity_limit,
    "l_hip_pitch_joint":ACTUATOR_504736NE.velocity_limit,
    "l_hip_roll_joint":ACTUATOR_504736NE.velocity_limit,
    "l_thigh_joint":ACTUATOR_504736NE.velocity_limit,
    "l_calf_joint":ACTUATOR_504736NE.velocity_limit,
    "l_ankle_pitch_joint":ACTUATOR_504736NE.velocity_limit,
    "l_ankle_roll_joint":ACTUATOR_504736NE.velocity_limit,
}


ARMATURE = {
    "r_hip_pitch_joint":ACTUATOR_504736NE.reflected_inertia,
    "r_hip_roll_joint":ACTUATOR_504736NE.reflected_inertia,
    "r_thigh_joint":ACTUATOR_504736NE.reflected_inertia,
    "r_calf_joint":ACTUATOR_504736NE.reflected_inertia,
    "r_ankle_pitch_joint":ACTUATOR_504736NE.reflected_inertia,
    "r_ankle_roll_joint":ACTUATOR_504736NE.reflected_inertia,
    "l_hip_pitch_joint":ACTUATOR_504736NE.reflected_inertia,
    "l_hip_roll_joint":ACTUATOR_504736NE.reflected_inertia,
    "l_thigh_joint":ACTUATOR_504736NE.reflected_inertia,
    "l_calf_joint":ACTUATOR_504736NE.reflected_inertia,
    "l_ankle_pitch_joint":ACTUATOR_504736NE.reflected_inertia,
    "l_ankle_roll_joint":ACTUATOR_504736NE.reflected_inertia,
}

# 0.25 * effort / stiffness, in the same per-joint dict style
ACTION_SCALE = {
    name: 0.25 * EFFORT_LIMIT[name] / STIFFNESS[name]
    for name in JOINT_NAMES_EXPR
    if name in EFFORT_LIMIT and name in STIFFNESS and STIFFNESS[name] != 0
}

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

END_EFFECTORS = {
    "l_foot": {
        "body_name": "l_ankle_roll_link",
        "actuated_joints": ["l_hip_pitch_joint", 
                            "l_hip_roll_joint", 
                            "l_thigh_joint", 
                            "l_calf_joint", 
                            "l_ankle_pitch_joint",
                            "l_ankle_roll_joint"
                            ],
        "links_in_chain": [
            "l_hip_pitch_link",
            "l_hip_roll_link",
            "l_thigh_link",
            "l_calf_link",
            "l_ankle_pitch_link",
            "l_ankle_roll_link",
        ],
        "commanded_contact": True,
    },
    "r_foot": {
        "body_name": "r_ankle_roll_link",
        "actuated_joints": [
                            "r_hip_pitch_joint",
                            "r_hip_roll_joint",
                            "r_thigh_joint",
                            "r_calf_joint",
                            "r_ankle_pitch_joint",
                            "r_ankle_roll_joint"
                            ],
        "links_in_chain": [
            "r_hip_pitch_link",
            "r_hip_roll_link",
            "r_thigh_link",
            "r_calf_link",
            "r_ankle_pitch_link",
            "r_ankle_roll_link",
        ],
        "commanded_contact": True,
    },
}