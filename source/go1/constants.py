BAD_CONTACT_BODIES = [
    "trunk",
]

ROOT_LINK_NAME = "trunk"

JOINT_NAMES_EXPR = [
    'FR_hip',
    'FR_thigh',
    'FR_calf',
    'FL_hip',
    'FL_thigh',
    'FL_calf',
    'RR_hip',
    'RR_thigh',
    'RR_calf',
    'RL_hip',
    'RL_thigh',
    'RL_calf',
]

DEFAULT_JOINT_POS = {
    "FL_hip": 0.1,
    "FR_hip": -0.1,
    "RL_hip": 0.1,
    "RR_hip": -0.1,
    "FL_thigh": 0.8,
    "FR_thigh": 0.8,
    "RL_thigh": 1.0,
    "RR_thigh": 1.0,
    "FL_calf": -1.5,
    "FR_calf": -1.5,
    "RL_calf": -1.5,
    "RR_calf": -1.5,
}

STIFFNESS = {
    # Hip joints (abduction/adduction)
    "FL_hip": 20.0,
    "FR_hip": 20.0,
    "RL_hip": 20.0,
    "RR_hip": 20.0,
    
    # Thigh joints (hip flexion/extension)
    "FL_thigh": 20.0,
    "FR_thigh": 20.0,
    "RL_thigh": 20.0,
    "RR_thigh": 20.0,
    
    # Calf joints (knee)
    "FL_calf": 20.0,
    "FR_calf": 20.0,
    "RL_calf": 20.0,
    "RR_calf": 20.0,
}

DAMPING = {
    # Hip joints
    "FL_hip": 0.5,
    "FR_hip": 0.5,
    "RL_hip": 0.5,
    "RR_hip": 0.5,
    
    # Thigh joints
    "FL_thigh": 0.5,
    "FR_thigh": 0.5,
    "RL_thigh": 0.5,
    "RR_thigh": 0.5,
    
    # Calf joints
    "FL_calf": 0.5,
    "FR_calf": 0.5,
    "RL_calf": 0.5,
    "RR_calf": 0.5,
}


