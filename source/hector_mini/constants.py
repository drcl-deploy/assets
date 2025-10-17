from dataclasses import dataclass
from ..actuator_params import *

NATURAL_FREQ = 10 * 2.0 * 3.1415926535  # 10Hz
DAMPING_RATIO = 2.0

STIFFNESS_02 = ARMATURE_ROBOSTRIDE02 * NATURAL_FREQ**2

DAMPING_02 = 2.0 * DAMPING_RATIO * ARMATURE_ROBOSTRIDE02 * NATURAL_FREQ

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
    "left_hip_yaw_joint": STIFFNESS_02,
    "right_hip_yaw_joint": STIFFNESS_02,
    "left_hip_roll_joint": STIFFNESS_02,
    "right_hip_roll_joint": STIFFNESS_02,
    "left_hip_pitch_joint": STIFFNESS_02,
    "right_hip_pitch_joint": STIFFNESS_02,
    "left_knee_joint": STIFFNESS_02,
    "right_knee_joint": STIFFNESS_02,
    "left_calf_joint": STIFFNESS_02,
    "right_calf_joint": STIFFNESS_02,
    "left_ankle_joint": STIFFNESS_02,
    "right_ankle_joint": STIFFNESS_02,
}

DAMPING = {
    "left_hip_yaw_joint": DAMPING_02,
    "right_hip_yaw_joint": DAMPING_02,
    "left_hip_roll_joint": DAMPING_02,
    "right_hip_roll_joint": DAMPING_02,
    "left_hip_pitch_joint": DAMPING_02,
    "right_hip_pitch_joint": DAMPING_02,
    "left_knee_joint": DAMPING_02,
    "right_knee_joint": DAMPING_02,
    "left_calf_joint": DAMPING_02,
    "right_calf_joint": DAMPING_02,
    "left_ankle_joint": DAMPING_02,
    "right_ankle_joint": DAMPING_02,
}

EFFORT_LIMIT = {
    "left_hip_yaw_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_hip_yaw_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "left_hip_roll_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_hip_roll_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "left_hip_pitch_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_hip_pitch_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "left_knee_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_knee_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "left_calf_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_calf_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "left_ankle_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_ankle_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
}

VELOCITY_LIMIT = {
    "left_hip_yaw_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_hip_yaw_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "left_hip_roll_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_hip_roll_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "left_hip_pitch_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_hip_pitch_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "left_knee_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_knee_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "left_calf_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_calf_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "left_ankle_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_ankle_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
}

# Robstride 02, TODO: Consider couping on ankle, knee
ARMATURE = {
    "left_hip_yaw_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_hip_yaw_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "left_hip_roll_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_hip_roll_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "left_hip_pitch_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_hip_pitch_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "left_knee_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_knee_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "left_calf_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_calf_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "left_ankle_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_ankle_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
}

# 0.25 * effort / stiffness, in the same per-joint dict style
ACTION_SCALE = {
    name: 0.25 * EFFORT_LIMIT[name] / STIFFNESS[name]
    for name in JOINT_NAMES_EXPR
    if name in EFFORT_LIMIT and name in STIFFNESS and STIFFNESS[name] != 0
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
                            "left_hip_pitch_joint", 
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