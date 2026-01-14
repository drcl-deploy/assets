ARMATURE_5020 = 0.003609725
ARMATURE_7520_14 = 0.010177520
ARMATURE_7520_22 = 0.025101925
ARMATURE_4010 = 0.00425

NATURAL_FREQ = 10 * 2.0 * 3.1415926535  # 10Hz
DAMPING_RATIO = 2.0

STIFFNESS_5020 = ARMATURE_5020 * NATURAL_FREQ**2
STIFFNESS_7520_14 = ARMATURE_7520_14 * NATURAL_FREQ**2
STIFFNESS_7520_22 = ARMATURE_7520_22 * NATURAL_FREQ**2
STIFFNESS_4010 = ARMATURE_4010 * NATURAL_FREQ**2

DAMPING_5020 = 2.0 * DAMPING_RATIO * ARMATURE_5020 * NATURAL_FREQ
DAMPING_7520_14 = 2.0 * DAMPING_RATIO * ARMATURE_7520_14 * NATURAL_FREQ
DAMPING_7520_22 = 2.0 * DAMPING_RATIO * ARMATURE_7520_22 * NATURAL_FREQ
DAMPING_4010 = 2.0 * DAMPING_RATIO * ARMATURE_4010 * NATURAL_FREQ

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

JOINT_NAMES_EXPR = [
    "left_hip_pitch_joint",
    "left_hip_roll_joint",
    "left_hip_yaw_joint",
    "left_knee_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_hip_pitch_joint",
    "right_hip_roll_joint",
    "right_hip_yaw_joint",
    "right_knee_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",
    "waist_yaw_joint",
    "waist_roll_joint",
    "waist_pitch_joint",
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "left_wrist_pitch_joint",
    "left_wrist_yaw_joint",
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
    "right_wrist_pitch_joint",
    "right_wrist_yaw_joint",
]

DEFAULT_JOINT_POS = {
    "left_hip_yaw_joint": 0.0,
    "right_hip_yaw_joint": 0.0,
    "left_hip_roll_joint": 0.0,
    "right_hip_roll_joint": 0.0,
    "left_hip_pitch_joint": -0.312,
    "right_hip_pitch_joint": -0.312,
    "left_knee_joint": 0.669,
    "right_knee_joint": 0.669,
    "left_ankle_pitch_joint": -0.363,
    "right_ankle_pitch_joint": -0.363,
    "left_ankle_roll_joint": 0.0,
    "right_ankle_roll_joint": 0.0,
    "waist_roll_joint": 0.0,
    "waist_pitch_joint": 0.0,
    "waist_yaw_joint": 0.0,
    "left_shoulder_pitch_joint": 0.2,
    "right_shoulder_pitch_joint": 0.2,
    "left_shoulder_roll_joint": 0.2,
    "right_shoulder_roll_joint": -0.2,
    "left_shoulder_yaw_joint": 0.0,
    "right_shoulder_yaw_joint": 0.0,
    "left_elbow_joint": 0.6,
    "right_elbow_joint": 0.6,
    "left_wrist_roll_joint": 0.0,
    "right_wrist_roll_joint": 0.0,
    "left_wrist_pitch_joint": 0.0,
    "right_wrist_pitch_joint": 0.0,
    "left_wrist_yaw_joint": 0.0,
    "right_wrist_yaw_joint": 0.0,
}

STIFFNESS = {
    "left_hip_yaw_joint": STIFFNESS_7520_14,
    "right_hip_yaw_joint": STIFFNESS_7520_14,
    "left_hip_roll_joint": STIFFNESS_7520_22,
    "right_hip_roll_joint": STIFFNESS_7520_22,
    "left_hip_pitch_joint": STIFFNESS_7520_14,
    "right_hip_pitch_joint": STIFFNESS_7520_14,
    "left_knee_joint": STIFFNESS_7520_22,
    "right_knee_joint": STIFFNESS_7520_22,
    "left_ankle_pitch_joint": 2.0 * STIFFNESS_5020,
    "right_ankle_pitch_joint": 2.0 * STIFFNESS_5020,
    "left_ankle_roll_joint": 2.0 * STIFFNESS_5020,
    "right_ankle_roll_joint": 2.0 * STIFFNESS_5020,
    "waist_roll_joint": 2.0 * STIFFNESS_5020,
    "waist_pitch_joint": 2.0 * STIFFNESS_5020,
    "waist_yaw_joint": STIFFNESS_7520_14,
    "left_shoulder_pitch_joint": STIFFNESS_5020,
    "right_shoulder_pitch_joint": STIFFNESS_5020,
    "left_shoulder_roll_joint": STIFFNESS_5020,
    "right_shoulder_roll_joint": STIFFNESS_5020,
    "left_shoulder_yaw_joint": STIFFNESS_5020,
    "right_shoulder_yaw_joint": STIFFNESS_5020,
    "left_elbow_joint": STIFFNESS_5020,
    "right_elbow_joint": STIFFNESS_5020,
    "left_wrist_roll_joint": STIFFNESS_5020,
    "right_wrist_roll_joint": STIFFNESS_5020,
    "left_wrist_pitch_joint": STIFFNESS_4010,
    "right_wrist_pitch_joint": STIFFNESS_4010,
    "left_wrist_yaw_joint": STIFFNESS_4010,
    "right_wrist_yaw_joint": STIFFNESS_4010,
}

DAMPING = {
    "left_hip_yaw_joint": DAMPING_7520_14,
    "right_hip_yaw_joint": DAMPING_7520_14,
    "left_hip_roll_joint": DAMPING_7520_22,
    "right_hip_roll_joint": DAMPING_7520_22,
    "left_hip_pitch_joint": DAMPING_7520_14,
    "right_hip_pitch_joint": DAMPING_7520_14,
    "left_knee_joint": DAMPING_7520_22,
    "right_knee_joint": DAMPING_7520_22,
    "left_ankle_pitch_joint": 2.0 * DAMPING_5020,
    "right_ankle_pitch_joint": 2.0 * DAMPING_5020,
    "left_ankle_roll_joint": 2.0 * DAMPING_5020,
    "right_ankle_roll_joint": 2.0 * DAMPING_5020,
    "waist_roll_joint": 2.0 * DAMPING_5020,
    "waist_pitch_joint": 2.0 * DAMPING_5020,
    "waist_yaw_joint": DAMPING_7520_14,
    "left_shoulder_pitch_joint": DAMPING_5020,
    "right_shoulder_pitch_joint": DAMPING_5020,
    "left_shoulder_roll_joint": DAMPING_5020,
    "right_shoulder_roll_joint": DAMPING_5020,
    "left_shoulder_yaw_joint": DAMPING_5020,
    "right_shoulder_yaw_joint": DAMPING_5020,
    "left_elbow_joint": DAMPING_5020,
    "right_elbow_joint": DAMPING_5020,
    "left_wrist_roll_joint": DAMPING_5020,
    "right_wrist_roll_joint": DAMPING_5020,
    "left_wrist_pitch_joint": DAMPING_4010,
    "right_wrist_pitch_joint": DAMPING_4010,
    "left_wrist_yaw_joint": DAMPING_4010,
    "right_wrist_yaw_joint": DAMPING_4010,
}

EFFORT_LIMIT = {
    "left_hip_yaw_joint": 88.0,
    "right_hip_yaw_joint": 88.0,
    "left_hip_roll_joint": 139.0,
    "right_hip_roll_joint": 139.0,
    "left_hip_pitch_joint": 88.0,
    "right_hip_pitch_joint": 88.0,
    "left_knee_joint": 139.0,
    "right_knee_joint": 139.0,
    "left_ankle_pitch_joint": 50.0,
    "right_ankle_pitch_joint": 50.0,
    "left_ankle_roll_joint": 50.0,
    "right_ankle_roll_joint": 50.0,
    "waist_roll_joint": 50.0,
    "waist_pitch_joint": 50.0,
    "waist_yaw_joint": 88.0,
    "left_shoulder_pitch_joint": 25.0,
    "right_shoulder_pitch_joint": 25.0,
    "left_shoulder_roll_joint": 25.0,
    "right_shoulder_roll_joint": 25.0,
    "left_shoulder_yaw_joint": 25.0,
    "right_shoulder_yaw_joint": 25.0,
    "left_elbow_joint": 25.0,
    "right_elbow_joint": 25.0,
    "left_wrist_roll_joint": 25.0,
    "right_wrist_roll_joint": 25.0,
    "left_wrist_pitch_joint": 5.0,
    "right_wrist_pitch_joint": 5.0,
    "left_wrist_yaw_joint": 5.0,
    "right_wrist_yaw_joint": 5.0,
}

VELOCITY_LIMIT = {
    "left_hip_yaw_joint": 32.0,
    "right_hip_yaw_joint": 32.0,
    "left_hip_roll_joint": 20.0,
    "right_hip_roll_joint": 20.0,
    "left_hip_pitch_joint": 32.0,
    "right_hip_pitch_joint": 32.0,
    "left_knee_joint": 20.0,
    "right_knee_joint": 20.0,
    "left_ankle_pitch_joint": 37.0,
    "right_ankle_pitch_joint": 37.0,
    "left_ankle_roll_joint": 37.0,
    "right_ankle_roll_joint": 37.0,
    "waist_roll_joint": 37.0,
    "waist_pitch_joint": 37.0,
    "waist_yaw_joint": 32.0,
    "left_shoulder_pitch_joint": 37.0,
    "right_shoulder_pitch_joint": 37.0,
    "left_shoulder_roll_joint": 37.0,
    "right_shoulder_roll_joint": 37.0,
    "left_shoulder_yaw_joint": 37.0,
    "right_shoulder_yaw_joint": 37.0,
    "left_elbow_joint": 37.0,
    "right_elbow_joint": 37.0,
    "left_wrist_roll_joint": 37.0,
    "right_wrist_roll_joint": 37.0,
    "left_wrist_pitch_joint": 22.0,
    "right_wrist_pitch_joint": 22.0,
    "left_wrist_yaw_joint": 22.0,
    "right_wrist_yaw_joint": 22.0,
}

ARMATURE = {
    "left_hip_yaw_joint": ARMATURE_7520_14,
    "right_hip_yaw_joint": ARMATURE_7520_14,
    "left_hip_roll_joint": ARMATURE_7520_22,
    "right_hip_roll_joint": ARMATURE_7520_22,
    "left_hip_pitch_joint": ARMATURE_7520_14,
    "right_hip_pitch_joint": ARMATURE_7520_14,
    "left_knee_joint": ARMATURE_7520_22,
    "right_knee_joint": ARMATURE_7520_22,
    "left_ankle_pitch_joint": 2.0 * ARMATURE_5020,
    "right_ankle_pitch_joint": 2.0 * ARMATURE_5020,
    "left_ankle_roll_joint": 2.0 * ARMATURE_5020,
    "right_ankle_roll_joint": 2.0 * ARMATURE_5020,
    "waist_roll_joint": 2.0 * ARMATURE_5020,
    "waist_pitch_joint": 2.0 * ARMATURE_5020,
    "waist_yaw_joint": ARMATURE_7520_14,
    "left_shoulder_pitch_joint": ARMATURE_5020,
    "right_shoulder_pitch_joint": ARMATURE_5020,
    "left_shoulder_roll_joint": ARMATURE_5020,
    "right_shoulder_roll_joint": ARMATURE_5020,
    "left_shoulder_yaw_joint": ARMATURE_5020,
    "right_shoulder_yaw_joint": ARMATURE_5020,
    "left_elbow_joint": ARMATURE_5020,
    "right_elbow_joint": ARMATURE_5020,
    "left_wrist_roll_joint": ARMATURE_5020,
    "right_wrist_roll_joint": ARMATURE_5020,
    "left_wrist_pitch_joint": ARMATURE_4010,
    "right_wrist_pitch_joint": ARMATURE_4010,
    "left_wrist_yaw_joint": ARMATURE_4010,
    "right_wrist_yaw_joint": ARMATURE_4010,
}

END_EFFECTORS = {
    "l_foot": {
        "body_name": "left_ankle_roll_link",
        "actuated_joints": [
                            "left_hip_pitch_joint",
                            "left_hip_roll_joint",
                            "left_hip_yaw_joint",
                            "left_knee_joint",
                            "left_ankle_pitch_joint",
                            "left_ankle_roll_joint",
                            ],
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
                            "right_hip_pitch_joint",
                            "right_hip_roll_joint",
                            "right_hip_yaw_joint",
                            "right_knee_joint",
                            "right_ankle_pitch_joint",
                            "right_ankle_roll_joint",
                            ],
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
        "body_name": "left_wrist_yaw_link",
        "actuated_joints": [
                            "left_shoulder_pitch_joint",
                            "left_shoulder_roll_joint",
                            "left_shoulder_yaw_joint",
                            "left_elbow_joint",
                            "left_wrist_roll_joint",
                            "left_wrist_pitch_joint",
                            "left_wrist_yaw_joint",
                            ],
        "links_in_chain": [
            "left_shoulder_pitch_link",
            "left_shoulder_roll_link",
            "left_shoulder_yaw_link",
            "left_elbow_link",
            "left_wrist_roll_link",
            "left_wrist_pitch_link",
            "left_wrist_yaw_link",
        ],
        "commanded_contact": False,
    },
    "r_wrist": {
        "body_name": "right_wrist_yaw_link",
        "actuated_joints": [
                            "right_shoulder_pitch_joint",
                            "right_shoulder_roll_joint",
                            "right_shoulder_yaw_joint",
                            "right_elbow_joint",
                            "right_wrist_roll_joint",
                            "right_wrist_pitch_joint",
                            "right_wrist_yaw_joint",
                            ],
        "links_in_chain": [
            "right_shoulder_pitch_link",
            "right_shoulder_roll_link",
            "right_shoulder_yaw_link",
            "right_elbow_link",
            "right_wrist_roll_link",
            "right_wrist_pitch_link",
            "right_wrist_yaw_link",
        ],
        "commanded_contact": False,
    },

}
