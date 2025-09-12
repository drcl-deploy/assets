import isaaclab.sim as sim_utils
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg
from assets.hector_v1.actuators import (
    HectorV1ImplicitPDActuatorCfg,
    HectorV1IdealPDActuatorCfg,
)
from .constants import *

import os

ASSETS_DIR = os.environ.get("SIM_ASSETS_PATH")

# model variants

# implicit actuator
IMPLICIT_WO_COUPLING_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=os.path.join(ASSETS_DIR, "hector_v1/mvsc_reduced.urdf"),
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
        pos=(0.0, 0.0, 0.55),  # when fix_root_link=False
        joint_pos=DEFAULT_JOINT_POS,
        joint_vel={".*": 0.0},
    ),
    actuators={
        "legs": ImplicitActuatorCfg(
            joint_names_expr=JOINT_NAMES_EXPR,
            effort_limit=EFFORT_LIMIT,
            velocity_limit=VELOCITY_LIMIT,
            stiffness=STIFFNESS,
            damping=DAMPING,
        ),
    },
)

IMPLICIT_WO_COUPLING_SC_CFG = IMPLICIT_WO_COUPLING_CFG.copy()
# update the path to urdf file
IMPLICIT_WO_COUPLING_SC_CFG.spawn.asset_path = os.path.join(
    ASSETS_DIR, "hector_v1/mvsc_reduced2.urdf"
)

# implicit actuator with coupling 
IMPLICIT_W_COUPLING_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=os.path.join(ASSETS_DIR, "hector_v1/mvsc_reduced.urdf"),
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
        pos=(0.0, 0.0, 0.55),  # when fix_root_link=False
        joint_pos=DEFAULT_JOINT_POS,
        joint_vel={".*": 0.0},
    ),
    actuators={
        "legs": HectorV1ImplicitPDActuatorCfg(
            knee_gear_ratio=2.0,
            knee_indices=[6, 7],
            ankle_indices=[8, 9],
            joint_names_expr=JOINT_NAMES_EXPR,
            effort_limit=EFFORT_LIMIT,
            velocity_limit=VELOCITY_LIMIT,
            stiffness=STIFFNESS,
            damping=DAMPING,
        ),
    },
)

IMPLICIT_W_COUPLING_SC_CFG = IMPLICIT_W_COUPLING_CFG.copy()
# update the path to urdf file
IMPLICIT_W_COUPLING_SC_CFG.spawn.asset_path = os.path.join(
    ASSETS_DIR, "hector_v1/mvsc_reduced2.urdf"
)
