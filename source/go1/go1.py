from isaaclab_assets import UNITREE_GO1_CFG
from isaaclab.actuators import IdealPDActuatorCfg


GO1_ACTUATOR_CFG_IDEAL = IdealPDActuatorCfg(
    joint_names_expr=[".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"],
    
    # Joint-specific torque limits matching MuJoCo
    effort_limit={
        ".*_hip_joint": 23.7,     # Abduction joints
        ".*_thigh_joint": 23.7,   # Hip flexion joints
        ".*_calf_joint": 35.55,   # Knee joints (STRONGER)
    },
    
    velocity_limit=30.0,
    
    # Joint-specific gains (knees often need higher stiffness)
    stiffness={
        ".*_hip_joint": 40.0,
        ".*_thigh_joint": 40.0,
        ".*_calf_joint": 50.0,  # Stronger for load-bearing
    },
    damping={
        ".*_hip_joint": 1.0,
        ".*_thigh_joint": 1.0,
        ".*_calf_joint": 1.2,
    },
    
    armature=0.01,
    friction=0.2,
)

UNITREE_GO1_CFG = UNITREE_GO1_CFG.copy()

UNITREE_GO1_CFG.actuators={
        "base_legs": GO1_ACTUATOR_CFG_IDEAL,
    }