BAD_CONTACT_BODIES = [
    "torso_base",
]

FOOT_CONTACT_BODIES = [
    "left_toe_roll",
    "right_toe_roll",
]

ROOT_LINK_NAME = "torso_base"

END_EFFECTORS = {
    "l_foot": {
        "body_name": "left_leg_toe_roll",
        "actuated_joints": [
                            "left_leg_hip_roll",
                            "left_leg_hip_yaw",
                            "left_leg_hip_pitch",
                            "left_leg_knee",
                            "left_leg_toe_a",
                            "left_leg_toe_b",
                            ],
        "commanded_contact": True,
    },
    "r_foot": {
        "body_name": "right_leg_toe_roll",
        "actuated_joints": [
                            "right_leg_hip_roll",
                            "right_leg_hip_yaw",
                            "right_leg_hip_pitch",
                            "right_leg_knee",
                            "right_leg_toe_a",
                            "right_leg_toe_b",
                            ],
        "commanded_contact": True,
    },
    "l_wrist": {
        "body_name": "left_arm_wrist_yaw",
        "actuated_joints": [
                            "left_arm_shoulder_pitch",
                            "left_arm_shoulder_roll",
                            "left_arm_shoulder_yaw",
                            "left_arm_elbow",
                            "left_arm_wrist_roll",
                            "left_arm_wrist_pitch",
                            "left_arm_wrist_yaw",
                            ],
        "commanded_contact": False,
    },
    "r_wrist": {
        "body_name": "right_arm_wrist_yaw",
        "actuated_joints": [
                            "right_arm_shoulder_pitch",
                            "right_arm_shoulder_roll",
                            "right_arm_shoulder_yaw",
                            "right_arm_elbow",
                            "right_arm_wrist_roll",
                            "right_arm_wrist_pitch",
                            "right_arm_wrist_yaw",
                            ],
        "commanded_contact": False,
    },
}
