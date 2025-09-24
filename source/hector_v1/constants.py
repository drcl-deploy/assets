STIFFNESS = {
    "l_hip_yaw_joint": 20.0,
    "r_hip_yaw_joint": 20.0,
    "l_hip_roll_joint": 20.0,
    "r_hip_roll_joint": 20.0,
    # 'l_hip_yaw_joint': 40.0,
    # 'r_hip_yaw_joint': 40.0,
    # 'l_hip_roll_joint': 40.0,
    # 'r_hip_roll_joint': 40.0,
    "l_hip_pitch_joint": 30.0,
    "r_hip_pitch_joint": 30.0,
    "l_knee_joint": 60.0,  # kp*knee_gear_ratio^2
    "r_knee_joint": 60.0,  # kp*knee_gear_ratio^2
    "l_ankle_joint": 15.0,
    "r_ankle_joint": 15.0,
}

DAMPING = {
    "l_hip_yaw_joint": 1.0,
    "r_hip_yaw_joint": 1.0,
    "l_hip_roll_joint": 1.0,
    "r_hip_roll_joint": 1.0,
    "l_hip_pitch_joint": 1.0,
    "r_hip_pitch_joint": 1.0,
    "l_knee_joint": 2.0,  # kd*knee_gear_ratio^2
    "r_knee_joint": 2.0,  # kd*knee_gear_ratio^2
    "l_ankle_joint": 0.5,
    "r_ankle_joint": 0.5,
}


EFFORT_LIMIT = {
    "l_hip_yaw_joint": 33.5,
    "r_hip_yaw_joint": 33.5,
    "l_hip_roll_joint": 33.5,
    "r_hip_roll_joint": 33.5,
    "l_hip_pitch_joint": 33.5,
    "r_hip_pitch_joint": 33.5,
    "l_knee_joint": 67.0,  # motor_tau_max*knee_gear_ratio
    "r_knee_joint": 67.0,  # motor_tau_max*knee_gear_ratio
    "l_ankle_joint": 33.5,
    "r_ankle_joint": 33.5,
}


VELOCITY_LIMIT = {
    "l_hip_yaw_joint": 21.0,
    "r_hip_yaw_joint": 21.0,
    "l_hip_roll_joint": 21.0,
    "r_hip_roll_joint": 21.0,
    "l_hip_pitch_joint": 21.0,
    "r_hip_pitch_joint": 21.0,
    "l_knee_joint": 10.5,  # motor_speed_max/knee_gear_ratio
    "r_knee_joint": 10.5,  # motor_speed_max/knee_gear_ratio
    "l_ankle_joint": 21.0,
    "r_ankle_joint": 21.0,
}


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

ARMATURE = {
    "l_hip_yaw_joint": 0.01,
    "r_hip_yaw_joint": 0.01,
    "l_hip_roll_joint": 0.01,
    "r_hip_roll_joint": 0.01,
    "l_hip_pitch_joint": 0.01,
    "r_hip_pitch_joint": 0.01,
    "l_knee_joint": 0.04,  # motor_speed_max/knee_gear_ratio
    "r_knee_joint": 0.04,  # motor_speed_max/knee_gear_ratio
    "l_ankle_joint": 0.01,
    "r_ankle_joint": 0.01,
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
