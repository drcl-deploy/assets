BAD_CONTACT_BODIES = [
    "trunk",
]

ROOT_LINK_NAME = "trunk"

END_EFFECTORS = {
    "fl_foot": {
        "body_name": "FL_foot",
        "actuated_joints": ["FL_hip_joint", 
                            "FL_thigh_joint", 
                            "FL_calf_joint"
                            ],
        "links_in_chain": [
            "FL_hip",
            "FL_thigh",
            "FL_calf",
            "FL_foot",
        ],
        "commanded_contact": True,
    },
    "fr_foot": {
        "body_name": "FR_foot",
        "actuated_joints": ["FR_hip_joint", 
                            "FR_thigh_joint", 
                            "FR_calf_joint"
                            ],
        "links_in_chain": [
            "FR_hip",
            "FR_thigh",
            "FR_calf",
            "FR_foot",
        ],
        "commanded_contact": True,
    },
    "rl_foot": {
        "body_name": "RL_foot",
        "actuated_joints": ["RL_hip_joint", 
                            "RL_thigh_joint", 
                            "RL_calf_joint"
                            ],
        "links_in_chain": [
            "RL_hip",
            "RL_thigh",
            "RL_calf",
            "RL_foot",
        ],
        "commanded_contact": True,
    },
    "rr_foot": {
        "body_name": "RR_foot",
        "actuated_joints": ["RR_hip_joint", 
                            "RR_thigh_joint", 
                            "RR_calf_joint"
                            ],
        "links_in_chain": [
            "RR_hip",
            "RR_thigh",
            "RR_calf",
            "RR_foot",
        ],
        "commanded_contact": True,
    },
}