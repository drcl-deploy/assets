import isaaclab.sim as sim_utils
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg


##
# Configuration
##
JOINT_NAME_EXPR = [
    "left_hip_yaw_joint",
    "right_hip_yaw_joint",
    "left_hip_roll_joint",
    "right_hip_roll_joint",
    "left_hip_pitch_joint",
    "right_hip_pitch_joint",
    "left_knee_joint",
    "right_knee_joint",
    "left_calf_joint",
    "right_calf_joint",
    "left_ankle_joint",
    "right_ankle_joint",
]

DEFAULT_JOINT_POS = {
    "left_hip_yaw_joint": 0.0,  # 0
    "right_hip_yaw_joint": 0.0,  # 6
    "left_hip_roll_joint": 0.0,  # 1
    "right_hip_roll_joint": 0.0,  # 7
    "left_hip_pitch_joint": -0.4,  # 2
    "right_hip_pitch_joint": -0.4,  # 8
    "left_knee_joint": 0.5,  # 3
    "right_knee_joint": 0.5,  # 14
    "left_calf_joint": 0.1,  # 4
    "right_calf_joint": 0.1,  # 9
    "left_ankle_joint": -0.3,  # 5
    "right_ankle_joint": -0.3,  # 10
}

STIFFNESS = {
    "left_hip_yaw_joint": 10.0,
    "right_hip_yaw_joint": 10.0,
    "left_hip_roll_joint": 10.0,
    "right_hip_roll_joint": 10.0,
    "left_hip_pitch_joint": 10.0,
    "right_hip_pitch_joint": 10.0,
    "left_knee_joint": 10.0,
    "right_knee_joint": 10.0,
    "left_calf_joint": 10.0,
    "right_calf_joint": 10.0,
    "left_ankle_joint": 10.0,
    "right_ankle_joint": 10.0,
}

DAMPING = {
    "left_hip_yaw_joint": 1.0,
    "right_hip_yaw_joint": 1.0,
    "left_hip_roll_joint": 1.0,
    "right_hip_roll_joint": 1.0,
    "left_hip_pitch_joint": 1.0,
    "right_hip_pitch_joint": 1.0,
    "left_knee_joint": 1.0,
    "right_knee_joint": 1.0,
    "left_calf_joint": 1.0,
    "right_calf_joint": 1.0,
    "left_ankle_joint": 1.0,
    "right_ankle_joint": 1.0,
}

EFFORT_LIMIT = {
    "left_hip_yaw_joint": 17.0,
    "right_hip_yaw_joint": 17.0,
    "left_hip_roll_joint": 17.0,
    "right_hip_roll_joint": 17.0,
    "left_hip_pitch_joint": 17.0,
    "right_hip_pitch_joint": 17.0,
    "left_knee_joint": 17.0,
    "right_knee_joint": 17.0,
    "left_calf_joint": 17.0,
    "right_calf_joint": 17.0,
    "left_ankle_joint": 17.0,
    "right_ankle_joint": 17.0,
}

VELOCITY_LIMIT = {
    "left_hip_yaw_joint": 22.0,
    "right_hip_yaw_joint": 22.0,
    "left_hip_roll_joint": 22.0,
    "right_hip_roll_joint": 22.0,
    "left_hip_pitch_joint": 22.0,
    "right_hip_pitch_joint": 22.0,
    "left_knee_joint": 22.0,
    "right_knee_joint": 22.0,
    "left_calf_joint": 22.0,
    "right_calf_joint": 22.0,
    "left_ankle_joint": 22.0,
    "right_ankle_joint": 22.0,
}

import os

ASSETS_DIR = os.environ.get("SIM_ASSETS_PATH")

MPCL = [
    [-1.57, 1.57],  # l_hip_yaw_joint
    [-1.57, 1.57],  # r_hip_yaw_joint
    [-1.0, 1.0],  # l_hip_roll_joint
    [-1.0, 1.0],  # r_hip_roll_joint
    [-1.0, 2.57],  # l_hip_pitch_joint
    [-1.0, 2.57],  # r_hip_pitch_joint
    [0.1, 1.57],  # l_knee_joint
    [0.1, 1.57],  # r_knee_joint
    [-1.57, 1.57],  # l_calf_joint
    [-1.57, 1.57],  # r_calf_joint
    [-2.0, 2.0],  # l_ankle_joint
    [-2.0, 2.0],  # r_ankle_joint
]

# implicit actuator
HECTOR_MINI_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=os.path.join(ASSETS_DIR, "hector_mini/hector_mini_body.urdf"),
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
            joint_names_expr=JOINT_NAME_EXPR,
            effort_limit=EFFORT_LIMIT,
            velocity_limit=VELOCITY_LIMIT,
            stiffness=STIFFNESS,
            damping=DAMPING,
        ),
    },
)
