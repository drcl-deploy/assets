from isaaclab_assets import UNITREE_GO1_CFG
from isaaclab.actuators import IdealPDActuatorCfg
from .constants import STIFFNESS, DAMPING, EFFORT_LIMIT, ARMATURE


def create_actuator_stiffness():
    """Generate stiffness dict from constants"""
    stiffness = {}
    for joint_name, value in STIFFNESS.items():
        if "hip" in joint_name:
            stiffness.setdefault(".*_hip_joint", value)
        elif "thigh" in joint_name:
            stiffness.setdefault(".*_thigh_joint", value)
        elif "calf" in joint_name:
            stiffness.setdefault(".*_calf_joint", value)
    return stiffness


def create_actuator_damping():
    """Generate damping dict from constants"""
    damping = {}
    for joint_name, value in DAMPING.items():
        if "hip" in joint_name:
            damping.setdefault(".*_hip_joint", value)
        elif "thigh" in joint_name:
            damping.setdefault(".*_thigh_joint", value)
        elif "calf" in joint_name:
            damping.setdefault(".*_calf_joint", value)
    return damping

def create_effort_limit():
    effort_limit = {}
    for joint_name, value in EFFORT_LIMIT.items():
        if "hip" in joint_name:
            effort_limit.setdefault(".*_hip_joint", value)
        elif "thigh" in joint_name:
            effort_limit.setdefault(".*_thigh_joint", value)
        elif "calf" in joint_name:
            effort_limit.setdefault(".*_calf_joint", value)
    return effort_limit

GO1_ACTUATOR_CFG_IDEAL = IdealPDActuatorCfg(
    joint_names_expr=[".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"],
    
    velocity_limit=30.0,
    effort_limit=create_effort_limit(),
    stiffness=create_actuator_stiffness(),
    damping=create_actuator_damping(),
    armature=ARMATURE,
    friction=0.2,
)

UNITREE_GO1_CFG = UNITREE_GO1_CFG.copy()

UNITREE_GO1_CFG.actuators={
        "base_legs": GO1_ACTUATOR_CFG_IDEAL,
    }