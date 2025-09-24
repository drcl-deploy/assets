# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration for Hightorque robots.

The following configurations are available:

* :obj:`Pai_MINIMAL_CFG`: Pai biped robot with minimal collision bodies

Reference: https://github.com/hightorquerobotics/hightorque_ros
"""

import os
import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg
from .constants import *

ASSETS_DIR = os.environ.get("SIM_ASSETS_PATH")

PAI_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=os.path.join(ASSETS_DIR, "mini_pi/pi_12dof_release_v1.urdf"),
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
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=4,
            solver_velocity_iteration_count=1,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.3453),  
        joint_pos=DEFAULT_JOINT_POS,
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.90,
    actuators={
        "limbs": ImplicitActuatorCfg(
            joint_names_expr=JOINT_NAME_EXPR,
            effort_limit=EFFORT_LIMIT,
            velocity_limit=VELOCITY_LIMIT,
            stiffness=STIFFNESS,
            damping=DAMPING,
            armature=ARMATURE,
        ),
    },
)
