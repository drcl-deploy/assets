import copy
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
    "l_hip_yaw": 20.0,
    "l_shoulder_yaw": 10.0,
    "r_hip_yaw": 20.0,
    "r_shoulder_yaw": 10.0,
    "l_hip_roll": 20.0,
    "l_shoulder_pitch": 10.0,
    "r_hip_roll": 20.0,
    "r_shoulder_pitch": 10.0,
    "l_hip_pitch": 30.0,
    "l_shoulder_roll": 10.0,
    "r_hip_pitch": 30.0,
    "r_shoulder_roll": 10.0,
    "l_knee": 60.0,  # kp*knee_gear_ratio^2
    "l_elbow": 20.0,  # kp*elbow_gear_ratio^2
    "r_knee": 60.0,  # kp*knee_gear_ratio^2
    "r_elbow": 20.0,  # kp*elbow_gear_ratio^2
    "l_ankle": 15.0,
    "r_ankle": 15.0,
}

DAMPING = {
    "l_hip_yaw": 1.0,
    "l_shoulder_yaw": 0.5,
    "r_hip_yaw": 1.0,
    "r_shoulder_yaw": 0.5,
    "l_hip_roll": 1.0,
    "l_shoulder_pitch": 0.5,
    "r_hip_roll": 1.0,
    "r_shoulder_pitch": 0.5,
    "l_hip_pitch": 1.0,
    "l_shoulder_roll": 0.5,
    "r_hip_pitch": 1.0,
    "r_shoulder_roll": 0.5,
    "l_knee": 2.0,  # kd*knee_gear_ratio^2
    "l_elbow": 1.0,  # kd*elbow_gear_ratio^2
    "r_knee": 2.0,  # kd*knee_gear_ratio^2
    "r_elbow": 1.0,  # kd*elbow_gear_ratio^2
    "l_ankle": 0.5,
    "r_ankle": 0.5,
}

EFFORT_LIMIT = {
    "l_hip_yaw": 33.5,
    "l_shoulder_yaw": 17.0,
    "r_hip_yaw": 33.5,
    "r_shoulder_yaw": 17.0,
    "l_hip_roll": 33.5,
    "l_shoulder_pitch": 17.0,
    "r_hip_roll": 33.5,
    "r_shoulder_pitch": 17.0,
    "l_hip_pitch": 33.5,
    "l_shoulder_roll": 17.0,
    "r_hip_pitch": 33.5,
    "r_shoulder_roll": 17.0,
    "l_knee": 67.0,  # motor_tau_max*knee_gear_ratio
    "l_elbow": 24.089,  # motor_tau_max*elbow_gear_ratio
    "r_knee": 67.0,  # motor_tau_max*knee_gear_ratio
    "r_elbow": 24.089,  # motor_tau_max*elbow_gear_ratio
    "l_ankle": 33.5,
    "r_ankle": 33.5,
}

VELOCITY_LIMIT = {
    "l_hip_yaw": 21.0,
    "l_shoulder_yaw": 32.0,
    "r_hip_yaw": 21.0,
    "r_shoulder_yaw": 32.0,
    "l_hip_roll": 21.0,
    "l_shoulder_pitch": 32.0,
    "r_hip_roll": 21.0,
    "r_shoulder_pitch": 32.0,
    "l_hip_pitch": 21.0,
    "l_shoulder_roll": 32.0,
    "r_hip_pitch": 21.0,
    "r_shoulder_roll": 32.0,
    "l_knee": 10.5,  # motor_speed_max/knee_gear_ratio
    "l_elbow": 22.582921665,  # motor_speed_max/elbow_gear_ratio
    "r_knee": 10.5,  # motor_speed_max/knee_gear_ratio
    "r_elbow": 22.582921665,  # motor_speed_max/elbow_gear_ratio
    "l_ankle": 21.0,
    "r_ankle": 21.0,
}

ARMATURE = {
    "l_hip_yaw": 0.01,
    "l_shoulder_yaw": 0.00414,
    "r_hip_yaw": 0.01,
    "r_shoulder_yaw": 0.00414,
    "l_hip_roll": 0.01,
    "l_shoulder_pitch": 0.00414,
    "r_hip_roll": 0.01,
    "r_shoulder_pitch": 0.00414,
    "l_hip_pitch": 0.01,
    "l_shoulder_roll": 0.00414,
    "r_hip_pitch": 0.01,
    "r_shoulder_roll": 0.00414,
    "l_knee": 0.04,  # motor_speed_max/knee_gear_ratio
    "l_elbow": 0.0093,  # motor_speed_max/elbow_gear_ratio
    "r_knee": 0.04,  # motor_speed_max/knee_gear_ratio
    "r_elbow": 0.0093,  # motor_speed_max/elbow_gear_ratio
    "l_ankle": 0.01,
    "r_ankle": 0.01,
}

MPCL = [
    [-0.523599, 0.523599],  # l_hip_yaw_joint
    [-1.309, 1.309],  # l_shoulder_yaw_joint
    [-0.523599, 0.523599],  # r_hip_yaw_joint
    [-1.309, 1.309],  # r_shoulder_yaw_joint
    [-0.349066, 0.7900000214576721],  # l_hip_roll_joint
    [-2.35619, 2.61799],  # l_shoulder_pitch_joint
    [-0.7900000214576721, 0.349066],  # r_hip_roll_joint
    [-2.35619, 2.61799],  # r_shoulder_pitch_joint
    [-0.3, 2.1],  # l_hip_pitch_joint
    [-1.5708, 0.0],  # l_shoulder_roll_joint
    [-0.3, 2.1],  # r_hip_pitch_joint
    [-0.0, 1.5708],  # r_shoulder_roll_joint
    [-2.0, 0.0],  # l_knee_joint, joint limits * knee_gear_ratio
    [-3.70969733, 3.70969733],  # l_elbow_joint
    [-2.0, 0.0],  # r_knee_joint, joint limits * knee_gear_ratio
    [-3.70969733, 3.70969733],  # r_elbow_joint
    [-1.57, 0.7900000214576721],  # l_ankle_joint
    [-1.57, 0.7900000214576721],  # r_ankle_joint
]

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
            "r_hip1",
            "l_hip_pitch",
            "l_thigh",
            "l_calf",
            "l_toe",
        ],
    },
    "r_foot": {
        "body_name": "r_toe",
        "actuated_joints": ["r_hip_yaw", "r_hip_roll", "r_hip_pitch", "r_knee", "r_ankle"],
        "links_in_chain": [
            "r_hip1",
            "l_hip1",
            "r_hip_pitch",
            "r_thigh",
            "r_calf",
            "r_toe",
        ],
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
    },
}