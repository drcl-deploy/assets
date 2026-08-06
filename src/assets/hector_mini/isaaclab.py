import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

from assets.paths import asset_path

from .constants import (
    ARMATURE,
    DAMPING,
    DEFAULT_JOINT_POS,
    EFFORT_LIMIT,
    JOINT_NAMES_EXPR,
    STIFFNESS,
    VELOCITY_LIMIT,
)

##
# Configuration
##

# implicit actuator
HECTOR_MINI_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=str(asset_path("hector_mini", "mvsc.urdf")),
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        fix_base=False,
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            drive_type="force",
            target_type="position",
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(
                stiffness=STIFFNESS,
                damping=DAMPING,
            ),
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.65),  # when fix_root_link=False
        # pos=(0.0, 0.0, 1.00), # when fix_root_link=True
        joint_pos=DEFAULT_JOINT_POS,
        joint_vel={".*": 0.0},
    ),
    actuators={
        "limbs": ImplicitActuatorCfg(
            joint_names_expr=JOINT_NAMES_EXPR,
            effort_limit_sim=EFFORT_LIMIT,
            velocity_limit_sim=VELOCITY_LIMIT,
            stiffness=STIFFNESS,
            damping=DAMPING,
            armature=ARMATURE,
        ),
    },
)

# simple collision
HECTOR_MINI_SC_CFG = HECTOR_MINI_CFG.copy()
# update the path to urdf file
HECTOR_MINI_SC_CFG.spawn.asset_path = str(asset_path("hector_mini", "hector_mini_mvsc.urdf"))
