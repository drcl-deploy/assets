from dataclasses import dataclass
from ..actuator_params import *

NATURAL_FREQ = 10 * 2.0 * 3.1415926535  # 10Hz
DAMPING_RATIO = 2.0

STIFFNESS_02 = ARMATURE_ROBOSTRIDE02 * NATURAL_FREQ**2
STIFFNESS_03 = ARMATURE_ROBOSTRIDE03 * NATURAL_FREQ**2
STIFFNESS_04 = ARMATURE_ROBOSTRIDE04 * NATURAL_FREQ**2

DAMPING_02 = 2.0 * DAMPING_RATIO * ARMATURE_ROBOSTRIDE02 * NATURAL_FREQ
DAMPING_03 = 2.0 * DAMPING_RATIO * ARMATURE_ROBOSTRIDE03 * NATURAL_FREQ
DAMPING_04 = 2.0 * DAMPING_RATIO * ARMATURE_ROBOSTRIDE04 * NATURAL_FREQ

JOINT_NAMES_EXPR = [
    "left_shoulder_pitch_joint",
    "right_shoulder_pitch_joint",
    "waist_yaw_joint",
    "left_shoulder_roll_joint",
    "right_shoulder_roll_joint",
    "left_hip_pitch_joint",
    "right_hip_pitch_joint",
    "left_shoulder_yaw_joint",
    "right_shoulder_yaw_joint",
    "left_hip_roll_joint",
    "right_hip_roll_joint",
    "left_elbow_joint",
    "right_elbow_joint",
    "left_hip_yaw_joint",
    "right_hip_yaw_joint",
    "left_wrist_yaw_joint",
    "right_wrist_yaw_joint",
    "left_knee_joint",
    "right_knee_joint",
    "left_ankle_pitch_joint",
    "right_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_ankle_roll_joint",
]

DEFAULT_JOINT_POS = {
    "left_shoulder_pitch_joint": 0.0,
    "right_shoulder_pitch_joint": 0.0,
    "waist_yaw_joint": 0.0,
    "left_shoulder_roll_joint": 0.0,
    "right_shoulder_roll_joint": 0.0,
    "left_hip_pitch_joint": -0.5,
    "right_hip_pitch_joint": -0.5,
    "left_shoulder_yaw_joint": 0.0,
    "right_shoulder_yaw_joint": 0.0,
    "left_hip_roll_joint": 0.0,
    "right_hip_roll_joint": 0.0,
    "left_elbow_joint": 0.0,
    "right_elbow_joint": 0.0,
    "left_hip_yaw_joint": -0.3,
    "right_hip_yaw_joint": 0.3,
    "left_wrist_yaw_joint": 0.0,
    "right_wrist_yaw_joint": 0.0,
    "left_knee_joint": 1.0,
    "right_knee_joint": 1.0,
    "left_ankle_pitch_joint": -0.49,
    "right_ankle_pitch_joint": -0.49,
    "left_ankle_roll_joint": 0.0,
    "right_ankle_roll_joint": 0.0,
}

STIFFNESS = {
    "left_shoulder_pitch_joint": STIFFNESS_02,
    "right_shoulder_pitch_joint": STIFFNESS_02,
    "waist_yaw_joint": STIFFNESS_04,
    "left_shoulder_roll_joint": STIFFNESS_02,
    "right_shoulder_roll_joint": STIFFNESS_02,
    "left_hip_pitch_joint": STIFFNESS_03,
    "right_hip_pitch_joint": STIFFNESS_03,
    "left_shoulder_yaw_joint": STIFFNESS_02,
    "right_shoulder_yaw_joint": STIFFNESS_02,
    "left_hip_roll_joint": STIFFNESS_03,
    "right_hip_roll_joint": STIFFNESS_03,
    "left_elbow_joint": STIFFNESS_02,
    "right_elbow_joint": STIFFNESS_02,
    "left_hip_yaw_joint": STIFFNESS_03,
    "right_hip_yaw_joint": STIFFNESS_03,
    "left_wrist_yaw_joint": STIFFNESS_02,
    "right_wrist_yaw_joint": STIFFNESS_02,
    "left_knee_joint": STIFFNESS_04,
    "right_knee_joint": STIFFNESS_04,
    "left_ankle_pitch_joint": 2.0*STIFFNESS_03,
    "right_ankle_pitch_joint": 2.0*STIFFNESS_03,
    "left_ankle_roll_joint": 2.0*STIFFNESS_03,
    "right_ankle_roll_joint": 2.0*STIFFNESS_03,
}

DAMPING = {
    "left_shoulder_pitch_joint": DAMPING_02,
    "right_shoulder_pitch_joint": DAMPING_02,
    "waist_yaw_joint": DAMPING_04,
    "left_shoulder_roll_joint": DAMPING_02,
    "right_shoulder_roll_joint": DAMPING_02,
    "left_hip_pitch_joint": DAMPING_03,
    "right_hip_pitch_joint": DAMPING_03,
    "left_shoulder_yaw_joint": DAMPING_02,
    "right_shoulder_yaw_joint": DAMPING_02,
    "left_hip_roll_joint": DAMPING_03,
    "right_hip_roll_joint": DAMPING_03,
    "left_elbow_joint": DAMPING_02,
    "right_elbow_joint": DAMPING_02,
    "left_hip_yaw_joint": DAMPING_03,
    "right_hip_yaw_joint": DAMPING_03,
    "left_wrist_yaw_joint": DAMPING_02,
    "right_wrist_yaw_joint": DAMPING_02,
    "left_knee_joint": DAMPING_04,
    "right_knee_joint": DAMPING_04,
    "left_ankle_pitch_joint": 2.0*DAMPING_03,
    "right_ankle_pitch_joint": 2.0*DAMPING_03,
    "left_ankle_roll_joint": 2.0*DAMPING_03,
    "right_ankle_roll_joint": 2.0*DAMPING_03,
}

EFFORT_LIMIT = {
    "left_shoulder_pitch_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_shoulder_pitch_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "waist_yaw_joint": ACTUATOR_ROBOSTRIDE04.effort_limit,
    "left_shoulder_roll_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_shoulder_roll_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "left_hip_pitch_joint": ACTUATOR_ROBOSTRIDE03.effort_limit,
    "right_hip_pitch_joint": ACTUATOR_ROBOSTRIDE03.effort_limit,
    "left_shoulder_yaw_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_shoulder_yaw_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "left_hip_roll_joint": ACTUATOR_ROBOSTRIDE03.effort_limit,
    "right_hip_roll_joint": ACTUATOR_ROBOSTRIDE03.effort_limit,
    "left_elbow_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_elbow_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "left_hip_yaw_joint": ACTUATOR_ROBOSTRIDE03.effort_limit,
    "right_hip_yaw_joint": ACTUATOR_ROBOSTRIDE03.effort_limit,
    "left_wrist_yaw_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "right_wrist_yaw_joint": ACTUATOR_ROBOSTRIDE02.effort_limit,
    "left_knee_joint": ACTUATOR_ROBOSTRIDE04.effort_limit,
    "right_knee_joint": ACTUATOR_ROBOSTRIDE04.effort_limit,
    "left_ankle_pitch_joint": 2.0*ACTUATOR_ROBOSTRIDE03.effort_limit,
    "right_ankle_pitch_joint": 2.0*ACTUATOR_ROBOSTRIDE03.effort_limit,
    "left_ankle_roll_joint": 2.0*ACTUATOR_ROBOSTRIDE03.effort_limit,
    "right_ankle_roll_joint": 2.0*ACTUATOR_ROBOSTRIDE03.effort_limit,
}

VELOCITY_LIMIT = {
    "left_shoulder_pitch_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_shoulder_pitch_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "waist_yaw_joint": ACTUATOR_ROBOSTRIDE04.velocity_limit,
    "left_shoulder_roll_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_shoulder_roll_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "left_hip_pitch_joint": ACTUATOR_ROBOSTRIDE03.velocity_limit,
    "right_hip_pitch_joint": ACTUATOR_ROBOSTRIDE03.velocity_limit,
    "left_shoulder_yaw_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_shoulder_yaw_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "left_hip_roll_joint": ACTUATOR_ROBOSTRIDE03.velocity_limit,
    "right_hip_roll_joint": ACTUATOR_ROBOSTRIDE03.velocity_limit,
    "left_elbow_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_elbow_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "left_hip_yaw_joint": ACTUATOR_ROBOSTRIDE03.velocity_limit,
    "right_hip_yaw_joint": ACTUATOR_ROBOSTRIDE03.velocity_limit,
    "left_wrist_yaw_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "right_wrist_yaw_joint": ACTUATOR_ROBOSTRIDE02.velocity_limit,
    "left_knee_joint": ACTUATOR_ROBOSTRIDE04.velocity_limit,
    "right_knee_joint": ACTUATOR_ROBOSTRIDE04.velocity_limit,
    "left_ankle_pitch_joint": ACTUATOR_ROBOSTRIDE03.velocity_limit,
    "right_ankle_pitch_joint": ACTUATOR_ROBOSTRIDE03.velocity_limit,
    "left_ankle_roll_joint": ACTUATOR_ROBOSTRIDE03.velocity_limit,
    "right_ankle_roll_joint": ACTUATOR_ROBOSTRIDE03.velocity_limit,
}

ARMATURE = {
    "left_shoulder_pitch_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_shoulder_pitch_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "waist_yaw_joint": ACTUATOR_ROBOSTRIDE04.reflected_inertia,
    "left_shoulder_roll_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_shoulder_roll_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "left_hip_pitch_joint": ACTUATOR_ROBOSTRIDE03.reflected_inertia,
    "right_hip_pitch_joint": ACTUATOR_ROBOSTRIDE03.reflected_inertia,
    "left_shoulder_yaw_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_shoulder_yaw_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "left_hip_roll_joint": ACTUATOR_ROBOSTRIDE03.reflected_inertia,
    "right_hip_roll_joint": ACTUATOR_ROBOSTRIDE03.reflected_inertia,
    "left_elbow_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_elbow_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "left_hip_yaw_joint": ACTUATOR_ROBOSTRIDE03.reflected_inertia,
    "right_hip_yaw_joint": ACTUATOR_ROBOSTRIDE03.reflected_inertia,
    "left_wrist_yaw_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "right_wrist_yaw_joint": ACTUATOR_ROBOSTRIDE02.reflected_inertia,
    "left_knee_joint": ACTUATOR_ROBOSTRIDE04.reflected_inertia,
    "right_knee_joint": ACTUATOR_ROBOSTRIDE04.reflected_inertia,
    "left_ankle_pitch_joint": 2.0*ACTUATOR_ROBOSTRIDE03.reflected_inertia,
    "right_ankle_pitch_joint": 2.0*ACTUATOR_ROBOSTRIDE03.reflected_inertia,
    "left_ankle_roll_joint": 2.0*ACTUATOR_ROBOSTRIDE03.reflected_inertia,
    "right_ankle_roll_joint": 2.0*ACTUATOR_ROBOSTRIDE03.reflected_inertia,
}

# 0.25 * effort / stiffness, in the same per-joint dict style
ACTION_SCALE = {
    name: 0.25 * EFFORT_LIMIT[name] / STIFFNESS[name]
    for name in JOINT_NAMES_EXPR
    if name in EFFORT_LIMIT and name in STIFFNESS and STIFFNESS[name] != 0
}

BAD_CONTACT_BODIES = [
    "torso_link",
    "pelvis_link",
    "left_hip_pitch_link",
    "right_hip_pitch_link",
]

FOOT_CONTACT_BODIES = [
    "left_ankle_roll_link",
    "right_ankle_roll_link",
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

SAMPLING_RANGE = {
    "left_foot_pos": [[-0.0, 0.15, 0.01], [0.0, 0.15, 0.3]],  # Lower limit, upper limit
    "right_foot_pos": [[0.0, -0.15, 0.01], [0.0, -0.15, 0.01]],
}

SUPPORT_CIRCLE_RADIUS = 0.5
SUPPORT_ELLIPSE_LENGTH = 0.5

END_EFFECTORS = {
    "l_foot": {
        "body_name": "left_ankle_roll_link",
        "actuated_joints": [
                            "left_hip_yaw_joint", 
                            "left_hip_roll_joint", 
                            "left_hip_pitch_joint", 
                            "left_knee_joint", 
                            "left_ankle_pitch_joint", 
                            "left_ankle_roll_joint"],
        "links_in_chain": [
            "left_hip_pitch_link",
            "left_hip_roll_link",
            "left_hip_yaw_link",
            "left_knee_link",
            "left_ankle_pitch_link",
            "left_ankle_roll_link",
        ],
        "commanded_contact": True,
    },
    "r_foot": {
        "body_name": "right_ankle_roll_link",
        "actuated_joints": [
                            "right_hip_yaw_joint", 
                            "right_hip_roll_joint", 
                            "right_hip_pitch_joint", 
                            "right_knee_joint", 
                            "right_ankle_pitch_joint", 
                            "right_ankle_roll_joint"],
        "links_in_chain": [ 
            "right_hip_pitch_link",
            "right_hip_roll_link",
            "right_hip_yaw_link",
            "right_knee_link",
            "right_ankle_pitch_link",
            "right_ankle_roll_link",
        ],  
        "commanded_contact": True,
    },
    "l_wrist": {
        "body_name": "left_fist_link",
        "actuated_joints": [
                            "left_shoulder_pitch_joint",
                            "left_shoulder_roll_joint",
                            "left_shoulder_yaw_joint",
                            "left_elbow_joint",
                            "left_wrist_yaw_joint",
                            ],
        "links_in_chain": [
            "left_shoulder_pitch_link",
            "left_shoulder_roll_link",
            "left_shoulder_yaw_link",
            "left_elbow_link",
            "left_wrist_link",
            "left_fist_link",
        ],
        "commanded_contact": False,
    },
    "r_wrist": {
        "body_name": "right_fist_link",
        "actuated_joints": [
                            "right_shoulder_pitch_joint",
                            "right_shoulder_roll_joint",
                            "right_shoulder_yaw_joint",
                            "right_elbow_joint",
                            "right_wrist_yaw_joint",
                            ],
        "links_in_chain": [
            "right_shoulder_pitch_link",
            "right_shoulder_roll_link",
            "right_shoulder_yaw_link",
            "right_elbow_link",
            "right_wrist_link",
            "right_fist_link",
        ],
        "commanded_contact": False,
    },
}
