BAD_CONTACT_BODIES = [
    "trunk",
]

ROOT_LINK_NAME = "trunk"

JOINT_NAMES_EXPR = [
    'FR_hip_joint',
    'FR_thigh_joint',
    'FR_calf_joint',
    'FL_hip_joint',
    'FL_thigh_joint',
    'FL_calf_joint',
    'RR_hip_joint',
    'RR_thigh_joint',
    'RR_calf_joint',
    'RL_hip_joint',
    'RL_thigh_joint',
    'RL_calf_joint',
    'FR_spring',
    'FL_spring',
    'RR_spring',
    'RL_spring',
]

DEFAULT_JOINT_POS = {
    "FL_hip_joint": 0.1,
    "FR_hip_joint": -0.1,
    "RL_hip_joint": 0.1,
    "RR_hip_joint": -0.1,
    "FL_thigh_joint": 0.785,
    "FR_thigh_joint": 0.785,
    "RL_thigh_joint": 0.785,
    "RR_thigh_joint": 0.785,
    "FL_calf_joint": -1.57,
    "FR_calf_joint": -1.57,
    "RL_calf_joint": -1.57,
    "RR_calf_joint": -1.57,
    "FR_spring": 0.0,
    "FL_spring": 0.0,
    "RR_spring": 0.0,
    "RL_spring": 0.0,
}

STIFFNESS = {
    # Hip joints (abduction/adduction)
    "FL_hip_joint": 40.0,
    "FR_hip_joint": 40.0,
    "RL_hip_joint": 40.0,
    "RR_hip_joint": 40.0,
    
    # Thigh joints (hip flexion/extension)
    "FL_thigh_joint": 40.0,
    "FR_thigh_joint": 40.0,
    "RL_thigh_joint": 40.0,
    "RR_thigh_joint": 40.0,
    
    # Calf joints (knee)
    "FL_calf_joint": 50.0,
    "FR_calf_joint": 50.0,
    "RL_calf_joint": 50.0,
    "RR_calf_joint": 50.0,

    # Spring joints
    "FR_spring": 200.0,
    "FL_spring": 200.0,
    "RR_spring": 200.0,
    "RL_spring": 200.0,
}

DAMPING = {
    # Hip joints
    "FL_hip_joint": 1.0,
    "FR_hip_joint": 1.0,
    "RL_hip_joint": 1.0,
    "RR_hip_joint": 1.0,
    
    # Thigh joints
    "FL_thigh_joint": 1.0,
    "FR_thigh_joint": 1.0,
    "RL_thigh_joint": 1.0,
    "RR_thigh_joint": 1.0,
    
    # Calf joints
    "FL_calf_joint": 1.2,
    "FR_calf_joint": 1.2,
    "RL_calf_joint": 1.2,
    "RR_calf_joint": 1.2,

    # Spring joints
    "FR_spring": 0.0,
    "FL_spring": 0.0,
    "RR_spring": 0.0,
    "RL_spring": 0.0,
}

EFFORT_LIMIT = {
    # Hip joints
    "FL_hip_joint": 23.7,
    "FR_hip_joint": 23.7,
    "RL_hip_joint": 23.7,
    "RR_hip_joint": 23.7,
    
    # Thigh joints
    "FL_thigh_joint": 23.7,
    "FR_thigh_joint": 23.7,
    "RL_thigh_joint": 23.7,
    "RR_thigh_joint": 23.7,
    
    # Calf joints
    "FL_calf_joint": 35.55,
    "FR_calf_joint": 35.55,
    "RL_calf_joint": 35.55,
    "RR_calf_joint": 35.55,

    # Spring joints
    "FR_spring": 100.0,
    "FL_spring": 100.0,
    "RR_spring": 100.0,
    "RL_spring": 100.0,
}

VELOCITY_LIMIT = {
    "FL_hip_joint": 30.0,
    "FR_hip_joint": 30.0,
    "RL_hip_joint": 30.0,
    "RR_hip_joint": 30.0,
    "FL_thigh_joint": 30.0,
    "FR_thigh_joint": 30.0,
    "RL_thigh_joint": 30.0,
    "RR_thigh_joint": 30.0,
    "FL_calf_joint": 30.0,
    "FR_calf_joint": 30.0,
    "RL_calf_joint": 30.0,
    "RR_calf_joint": 30.0,

    "FR_spring": 100.0,
    "FL_spring": 100.0,
    "RR_spring": 100.0,
    "RL_spring": 100.0,
}

ARMATURE = 0.0001