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
    },
    "l_wrist": {
        "body_name": "left_palm_link",
        "actuated_joints": [
                            "left_shoulder_pitch_joint",
                            "left_shoulder_roll_joint",
                            "left_shoulder_yaw_joint",
                            "left_elbow_pitch_joint",
                            "left_elbow_roll_joint",
                            ],
        "links_in_chain": [
            "left_shoulder_pitch_link",
            "left_shoulder_roll_link",
            "left_shoulder_yaw_link",
            "left_elbow_pitch_link",
            "left_elbow_roll_link",
            "left_palm_link",
        ],
    },
    "r_wrist": {
        "body_name": "right_palm_link",
        "actuated_joints": [
                            "right_shoulder_pitch_joint",
                            "right_shoulder_roll_joint",
                            "right_shoulder_yaw_joint",
                            "right_elbow_pitch_joint",
                            "right_elbow_roll_joint",
                            ],
        "links_in_chain": [
            "right_shoulder_pitch_link",
            "right_shoulder_roll_link",
            "right_shoulder_yaw_link",
            "right_elbow_pitch_link",   
            "right_elbow_roll_link",
            "right_palm_link",
        ],
    },
}
