import isaaclab.sim as sim_utils
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg
from .constants import *

##
# Configuration
##

import os

ASSETS_DIR = os.environ.get("SIM_ASSETS_PATH")

# implicit actuator
MOTION_1_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=os.path.join(ASSETS_DIR, "motion_1/m1A_1v5_23dof_FixArm.urdf"),
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
        merge_fixed_joints=False,
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        # pos=(0.0, 0.0, 0.8), # when fix_root_link=False
        pos=(0.0, 0.0, 1.0),  # when fix_root_link=True
        joint_pos=DEFAULT_JOINT_POS,
        joint_vel={".*": 0.0},
    ),
    actuators={
        "limbs": ImplicitActuatorCfg(
            joint_names_expr=JOINT_NAME_EXPR,
            effort_limit_sim=EFFORT_LIMIT,
            velocity_limit_sim=VELOCITY_LIMIT,
            stiffness=STIFFNESS,
            damping=DAMPING,
            armature=ARMATURE,
        ),
    },
)

MOTION_1_SC_CFG = MOTION_1_CFG.copy()
# update the path to urdf file
MOTION_1_SC_CFG.spawn.asset_path = os.path.join(
    ASSETS_DIR, "motion_1/mvsc.urdf"
)   