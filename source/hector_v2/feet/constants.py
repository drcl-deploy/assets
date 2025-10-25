import copy
from dataclasses import dataclass
from source.actuator_params import *

NATURAL_FREQ = 10 * 2.0 * 3.1415926535  # 10Hz
DAMPING_RATIO = 2.0

STIFFNESS_01 = ARMATURE_ROBOSTRIDE01 * NATURAL_FREQ**2
STIFFNESS_A1 = ARMATURE_UNITREE_A1 * NATURAL_FREQ**2
STIFFNESS_01_ELBOW = ARMATURE_ROBOSTRIDE01_ELBOW * NATURAL_FREQ**2
STIFFNESS_A1_KNEE = ARMATURE_UNITREE_A1_KNEE * NATURAL_FREQ**2

DAMPING_01 = 2.0 * DAMPING_RATIO * ARMATURE_ROBOSTRIDE01 * NATURAL_FREQ
DAMPING_A1 = 2.0 * DAMPING_RATIO * ARMATURE_UNITREE_A1 * NATURAL_FREQ
DAMPING_01_ELBOW = 2.0 * DAMPING_RATIO * ARMATURE_ROBOSTRIDE01_ELBOW * NATURAL_FREQ
DAMPING_A1_KNEE = 2.0 * DAMPING_RATIO * ARMATURE_UNITREE_A1_KNEE * NATURAL_FREQ

# common joint parameters
JOINT_NAMES_EXPR = [
    "l_hip_yaw",
    "l_hip_roll",
    "l_hip_pitch",
    "l_knee",
    "l_ankle",
    "r_hip_yaw",
    "r_hip_roll",
    "r_hip_pitch",
    "r_knee",
    "r_ankle",
    "l_shoulder_yaw",
    "l_shoulder_pitch",
    "l_shoulder_roll",
    "l_elbow",
    "r_shoulder_yaw",
    "r_shoulder_pitch",
    "r_shoulder_roll",
    "r_elbow",
]

DEFAULT_JOINT_POS = {
    "l_hip_yaw": 0.0,
    "l_shoulder_yaw": 0.0,
    "r_hip_yaw": 0.0,
    "r_shoulder_yaw": 0.0,
    "l_hip_roll": 0.0,
    "l_shoulder_pitch": 0.785,
    "r_hip_roll": 0.0,
    "r_shoulder_pitch": 0.785,
    "l_hip_pitch": 0.7848373651504517,
    "l_shoulder_roll": 0.0,
    "r_hip_pitch": 0.7848373651504517,
    "r_shoulder_roll": 0.0,
    "l_knee": -1.57,
    "l_elbow": -1.57,
    "r_knee": -1.57,
    "r_elbow": -1.57,
    "l_ankle": 0.7848373651504517,
    "r_ankle": 0.7848373651504517,
}

DEFAULT_MOTOR_POS = copy.deepcopy(DEFAULT_JOINT_POS)
DEFAULT_MOTOR_POS["l_knee"] = -3.14  # -1.57*knee_gear_ratio
DEFAULT_MOTOR_POS["r_knee"] = -3.14  # -1.57*knee_gear_ratio
DEFAULT_MOTOR_POS["l_elbow"] = -2.22469  # -1.57*elbow_gear_ratio
DEFAULT_MOTOR_POS["r_elbow"] = -2.22469  # -1.57*elbow_gear_ratio
DEFAULT_MOTOR_POS["l_ankle"] = -0.78
DEFAULT_MOTOR_POS["r_ankle"] = -0.78

# common actuator parameters
STIFFNESS = {
    "l_hip_yaw": STIFFNESS_A1,
    "l_shoulder_yaw": STIFFNESS_01,
    "r_hip_yaw": STIFFNESS_A1,
    "r_shoulder_yaw": STIFFNESS_01,
    "l_hip_roll": STIFFNESS_A1,
    "l_shoulder_pitch": STIFFNESS_01,
    "r_hip_roll": STIFFNESS_A1,
    "r_shoulder_pitch": STIFFNESS_01,
    "l_hip_pitch": STIFFNESS_A1,
    "l_shoulder_roll": STIFFNESS_01,
    "r_hip_pitch": STIFFNESS_A1,
    "r_shoulder_roll": STIFFNESS_01,
    "l_knee": STIFFNESS_A1_KNEE,  # kp*knee_gear_ratio^2
    "l_elbow": STIFFNESS_01_ELBOW,  # kp*elbow_gear_ratio^2
    "r_knee": STIFFNESS_A1_KNEE,  # kp*knee_gear_ratio^2
    "r_elbow": STIFFNESS_01_ELBOW,  # kp*elbow_gear_ratio^2
    "l_ankle": STIFFNESS_A1,
    "r_ankle": STIFFNESS_A1,
}

DAMPING = {
    "l_hip_yaw": DAMPING_A1,
    "l_shoulder_yaw": DAMPING_01,
    "r_hip_yaw": DAMPING_A1,
    "r_shoulder_yaw": DAMPING_01,
    "l_hip_roll": DAMPING_A1,
    "l_shoulder_pitch": DAMPING_01,
    "r_hip_roll": DAMPING_A1,
    "r_shoulder_pitch": DAMPING_01,
    "l_hip_pitch": DAMPING_A1,
    "l_shoulder_roll": DAMPING_01,
    "r_hip_pitch": DAMPING_A1,
    "r_shoulder_roll": DAMPING_01,
    "l_knee": DAMPING_A1_KNEE,  # kp*knee_gear_ratio^2
    "l_elbow": DAMPING_01_ELBOW,  # kp*elbow_gear_ratio^2
    "r_knee": DAMPING_A1_KNEE,  # kp*knee_gear_ratio^2
    "r_elbow": DAMPING_01_ELBOW,  # kp*elbow_gear_ratio^2
    "l_ankle": DAMPING_A1,
    "r_ankle": DAMPING_A1,
}

EFFORT_LIMIT = {
    "l_hip_yaw": ACTUATOR_UNITREE_A1.effort_limit,
    "l_shoulder_yaw": ACTUATOR_ROBOSTRIDE01.effort_limit,
    "r_hip_yaw": ACTUATOR_UNITREE_A1.effort_limit,
    "r_shoulder_yaw": ACTUATOR_ROBOSTRIDE01.effort_limit,
    "l_hip_roll": ACTUATOR_UNITREE_A1.effort_limit,
    "l_shoulder_pitch": ACTUATOR_ROBOSTRIDE01.effort_limit,
    "r_hip_roll": ACTUATOR_UNITREE_A1.effort_limit,
    "r_shoulder_pitch": ACTUATOR_ROBOSTRIDE01.effort_limit,
    "l_hip_pitch": ACTUATOR_UNITREE_A1.effort_limit,
    "l_shoulder_roll": ACTUATOR_ROBOSTRIDE01.effort_limit,
    "r_hip_pitch": ACTUATOR_UNITREE_A1.effort_limit,
    "r_shoulder_roll": ACTUATOR_ROBOSTRIDE01.effort_limit,
    "l_knee": ACTUATOR_UNITREE_A1_KNEE.effort_limit,  # kp*knee_gear_ratio^2
    "l_elbow": ACTUATOR_ROBOSTRIDE01_ELBOW.effort_limit,  # kp*elbow_gear_ratio^2
    "r_knee": ACTUATOR_UNITREE_A1_KNEE.effort_limit,  # kp*knee_gear_ratio^2
    "r_elbow": ACTUATOR_ROBOSTRIDE01_ELBOW.effort_limit,  # kp*elbow_gear_ratio^2
    "l_ankle": ACTUATOR_UNITREE_A1.effort_limit,
    "r_ankle": ACTUATOR_UNITREE_A1.effort_limit,
}

VELOCITY_LIMIT = {
    "l_hip_yaw": ACTUATOR_UNITREE_A1.velocity_limit,
    "l_shoulder_yaw": ACTUATOR_ROBOSTRIDE01.velocity_limit,
    "r_hip_yaw": ACTUATOR_UNITREE_A1.velocity_limit,
    "r_shoulder_yaw": ACTUATOR_ROBOSTRIDE01.velocity_limit,
    "l_hip_roll": ACTUATOR_UNITREE_A1.velocity_limit,
    "l_shoulder_pitch": ACTUATOR_ROBOSTRIDE01.velocity_limit,
    "r_hip_roll": ACTUATOR_UNITREE_A1.velocity_limit,
    "r_shoulder_pitch": ACTUATOR_ROBOSTRIDE01.velocity_limit,
    "l_hip_pitch": ACTUATOR_UNITREE_A1.velocity_limit,
    "l_shoulder_roll": ACTUATOR_ROBOSTRIDE01.velocity_limit,
    "r_hip_pitch": ACTUATOR_UNITREE_A1.velocity_limit,
    "r_shoulder_roll": ACTUATOR_ROBOSTRIDE01.velocity_limit,
    "l_knee": ACTUATOR_UNITREE_A1_KNEE.velocity_limit,  # kp*knee_gear_ratio^2
    "l_elbow": ACTUATOR_ROBOSTRIDE01_ELBOW.velocity_limit,  # kp*elbow_gear_ratio^2
    "r_knee": ACTUATOR_UNITREE_A1_KNEE.velocity_limit,  # kp*knee_gear_ratio^2
    "r_elbow": ACTUATOR_ROBOSTRIDE01_ELBOW.velocity_limit,  # kp*elbow_gear_ratio^2
    "l_ankle": ACTUATOR_UNITREE_A1.velocity_limit,
    "r_ankle": ACTUATOR_UNITREE_A1.velocity_limit,
}

ARMATURE = {
    "l_hip_yaw": ACTUATOR_UNITREE_A1.reflected_inertia,
    "l_shoulder_yaw": ACTUATOR_ROBOSTRIDE01.reflected_inertia,
    "r_hip_yaw": ACTUATOR_UNITREE_A1.reflected_inertia,
    "r_shoulder_yaw": ACTUATOR_ROBOSTRIDE01.reflected_inertia,
    "l_hip_roll": ACTUATOR_UNITREE_A1.reflected_inertia,
    "l_shoulder_pitch": ACTUATOR_ROBOSTRIDE01.reflected_inertia,
    "r_hip_roll": ACTUATOR_UNITREE_A1.reflected_inertia,
    "r_shoulder_pitch": ACTUATOR_ROBOSTRIDE01.reflected_inertia,
    "l_hip_pitch": ACTUATOR_UNITREE_A1.reflected_inertia,
    "l_shoulder_roll": ACTUATOR_ROBOSTRIDE01.reflected_inertia,
    "r_hip_pitch": ACTUATOR_UNITREE_A1.reflected_inertia,
    "r_shoulder_roll": ACTUATOR_ROBOSTRIDE01.reflected_inertia,
    "l_knee": ACTUATOR_UNITREE_A1_KNEE.reflected_inertia,  # kp*knee_gear_ratio^2
    "l_elbow": ACTUATOR_ROBOSTRIDE01_ELBOW.reflected_inertia,  # kp*elbow_gear_ratio^2
    "r_knee": ACTUATOR_UNITREE_A1_KNEE.reflected_inertia,  # kp*knee_gear_ratio^2
    "r_elbow": ACTUATOR_ROBOSTRIDE01_ELBOW.reflected_inertia,  # kp*elbow_gear_ratio^2
    "l_ankle": ACTUATOR_UNITREE_A1.reflected_inertia,
    "r_ankle": ACTUATOR_UNITREE_A1.reflected_inertia,
}

# 0.25 * effort / stiffness, in the same per-joint dict style
ACTION_SCALE = {
    name: 0.25 * EFFORT_LIMIT[name] / STIFFNESS[name]
    for name in JOINT_NAMES_EXPR
    if name in EFFORT_LIMIT and name in STIFFNESS and STIFFNESS[name] != 0
}

BAD_CONTACT_BODIES = [
    "torso",
    "r_thigh",
    "l_thigh",
    "r_calf",
    "l_calf",
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
        "actuated_joints": ["l_hip_yaw", "l_hip_roll", "l_hip_pitch", "l_knee", "l_ankle"],
        "links_in_chain": [
            "l_hip1",
            "l_hip_pitch",
            "l_thigh",
            "l_calf",
            "l_toe",
        ],
        "commanded_contact": True,
    },
    "r_foot": {
        "body_name": "r_toe",
        "actuated_joints": ["r_hip_yaw", "r_hip_roll", "r_hip_pitch", "r_knee", "r_ankle"],
        "links_in_chain": [
            "r_hip1",
            "r_hip_pitch",
            "r_thigh",
            "r_calf",
            "r_toe",
        ],
        "commanded_contact": True,
    },
    "l_wrist": {
        "body_name": "l_hand",
        "actuated_joints": ["l_shoulder_yaw", "l_shoulder_pitch", "l_shoulder_roll", "l_elbow"],
        "links_in_chain": [
            "l_shoulder1",
            "l_shoulder2",
            "l_upper_arm",
            "l_lower_arm",
            "l_hand",
        ],
        "commanded_contact": False,
    },
    "r_wrist": {
        "body_name": "r_hand",
        "actuated_joints": ["r_shoulder_yaw", "r_shoulder_pitch", "r_shoulder_roll", "r_elbow"],
        "links_in_chain": [
            "r_shoulder1",
            "r_shoulder2",
            "r_upper_arm",
            "r_lower_arm",
            "r_hand",
        ],
        "commanded_contact": False,
    },
}