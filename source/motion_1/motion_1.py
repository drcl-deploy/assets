import isaaclab.sim as sim_utils
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg


##
# Configuration
##
STIFFNESS = {
    "left_shoulder_pitch_joint": 40.0,
    "right_shoulder_pitch_joint": 40.0,
    "waist_yaw_joint": 120.0,
    "left_shoulder_roll_joint": 40.0,
    "right_shoulder_roll_joint": 40.0,
    "left_hip_pitch_joint": 120.0,
    "right_hip_pitch_joint": 120.0,
    "left_shoulder_yaw_joint": 40.0,
    "right_shoulder_yaw_joint": 40.0,
    "left_hip_roll_joint": 120.0,
    "right_hip_roll_joint": 120.0,
    "left_elbow_joint": 40.0,
    "right_elbow_joint": 40.0,
    "left_hip_yaw_joint": 120.0,
    "right_hip_yaw_joint": 120.0,
    "left_wrist_roll_joint": 40.0,
    "right_wrist_roll_joint": 40.0,
    "left_knee_joint": 160.0,
    "right_knee_joint": 160.0,
    "left_ankle_pitch_joint": 20.0,
    "right_ankle_pitch_joint": 20.0,
    "left_ankle_roll_joint": 20.0,
    "right_ankle_roll_joint": 20.0,
}
DAMPING = {
    "left_shoulder_pitch_joint": 5.0,
    "right_shoulder_pitch_joint": 5.0,
    "waist_yaw_joint": 5.0,
    "left_shoulder_roll_joint": 5.0,
    "right_shoulder_roll_joint": 5.0,
    "left_hip_pitch_joint": 5.0,
    "right_hip_pitch_joint": 5.0,
    "left_shoulder_yaw_joint": 5.0,
    "right_shoulder_yaw_joint": 5.0,
    "left_hip_roll_joint": 5.0,
    "right_hip_roll_joint": 5.0,
    "left_elbow_joint": 5.0,
    "right_elbow_joint": 5.0,
    "left_hip_yaw_joint": 5.0,
    "right_hip_yaw_joint": 5.0,
    "left_wrist_roll_joint": 5.0,
    "right_wrist_roll_joint": 5.0,
    "left_knee_joint": 5.0,
    "right_knee_joint": 5.0,
    "left_ankle_pitch_joint": 2.0,
    "right_ankle_pitch_joint": 2.0,
    "left_ankle_roll_joint": 2.0,
    "right_ankle_roll_joint": 2.0,
}

JOINT_NAME_EXPR = {
    "left_shoulder_pitch_joint",
    "right_shoulder_pitch_joint",
    "waist_yaw_joint",
    "left_shoulder_roll_joint",
    "right_shoulder_roll_joint",
    "left_hip_pitch_joint",
    "right_hip_pitch_joint",
    "left_shoulder_yaw_joint",
    "right_shoulder_yaw_joint",
    "left_hip_roll_joint",
    "right_hip_roll_joint",
    "left_elbow_joint",
    "right_elbow_joint",
    "left_hip_yaw_joint",
    "right_hip_yaw_joint",
    "left_wrist_roll_joint",
    "right_wrist_roll_joint",
    "left_knee_joint",
    "right_knee_joint",
    "left_ankle_pitch_joint",
    "right_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_ankle_roll_joint",
}

DEFAULT_JOINT_POS = {
    "left_shoulder_pitch_joint": 0.0,
    "right_shoulder_pitch_joint": 0.0,
    "waist_yaw_joint": 0.0,
    "left_shoulder_roll_joint": 0.0,
    "right_shoulder_roll_joint": 0.0,
    "left_hip_pitch_joint": -0.5,
    "right_hip_pitch_joint": -0.5,
    "left_shoulder_yaw_joint": 0.0,
    "right_shoulder_yaw_joint": 0.0,
    "left_hip_roll_joint": 0.0,
    "right_hip_roll_joint": 0.0,
    "left_elbow_joint": 0.0,
    "right_elbow_joint": 0.0,
    "left_hip_yaw_joint": -0.3,
    "right_hip_yaw_joint": 0.3,
    "left_wrist_roll_joint": 0.0,
    "right_wrist_roll_joint": 0.0,
    "left_knee_joint": 1.0,
    "right_knee_joint": 1.0,
    "left_ankle_pitch_joint": -0.49,
    "right_ankle_pitch_joint": -0.49,
    "left_ankle_roll_joint": 0.0,
    "right_ankle_roll_joint": 0.0,
}

EFFORT_LIMIT = {
    "left_shoulder_pitch_joint": 17.0,
    "right_shoulder_pitch_joint": 17.0,
    "waist_yaw_joint": 60.0,
    "left_shoulder_roll_joint": 17.0,
    "right_shoulder_roll_joint": 17.0,
    "left_hip_pitch_joint": 60.0,
    "right_hip_pitch_joint": 60.0,
    "left_shoulder_yaw_joint": 17.0,
    "right_shoulder_yaw_joint": 17.0,
    "left_hip_roll_joint": 60.0,
    "right_hip_roll_joint": 60.0,
    "left_elbow_joint": 17.0,
    "right_elbow_joint": 17.0,
    "left_hip_yaw_joint": 60.0,
    "right_hip_yaw_joint": 60.0,
    "left_wrist_roll_joint": 17.0,
    "right_wrist_roll_joint": 17.0,
    "left_knee_joint": 120.0,
    "right_knee_joint": 120.0,
    "left_ankle_pitch_joint": 34.0,
    "right_ankle_pitch_joint": 34.0,
    "left_ankle_roll_joint": 34.0,
    "right_ankle_roll_joint": 34.0,
}

VELOCITY_LIMIT = {
    "left_shoulder_pitch_joint": 32.9,
    "right_shoulder_pitch_joint": 32.9,
    "waist_yaw_joint": 20.4,
    "left_shoulder_roll_joint": 32.9,
    "right_shoulder_roll_joint": 32.9,
    "left_hip_pitch_joint": 20.4,
    "right_hip_pitch_joint": 20.4,
    "left_shoulder_yaw_joint": 32.9,
    "right_shoulder_yaw_joint": 32.9,
    "left_hip_roll_joint": 20.4,
    "right_hip_roll_joint": 20.4,
    "left_elbow_joint": 32.9,
    "right_elbow_joint": 32.9,
    "left_hip_yaw_joint": 20.4,
    "right_hip_yaw_joint": 20.4,
    "left_wrist_roll_joint": 32.9,
    "right_wrist_roll_joint": 32.9,
    "left_knee_joint": 20.9,
    "right_knee_joint": 20.9,
    "left_ankle_pitch_joint": 32.9,
    "right_ankle_pitch_joint": 32.9,
    "left_ankle_roll_joint": 32.9,
    "right_ankle_roll_joint": 32.9,
}

import os

ASSETS_DIR = os.environ.get("SIM_ASSETS_PATH")

MPCL = [
    [-3.1, 3.1],  # left_shoulder_pitch_joint
    [-3.1, 3.1],  # right_shoulder_pitch_joint
    [-0.175, 3.0],  # left_shoulder_roll_joint
    [-3.0, -0.175],  # right_shoulder_roll_joint
    [-1.047, 1.047],  # left_hip_pitch_joint
    [-1.047, 1.047],  # right_hip_pitch_joint
    [-3.1, 3.1],  # left_shoulder_yaw_joint
    [-3.1, 3.1],  # right_shoulder_yaw_joint
    [-0.145, 1.047],  # left_hip_roll_joint
    [-1.047, 0.145],  # right_hip_roll_joint
    [-1.6, 1.6],  # left_elbow_joint
    [-1.6, 1.6],  # right_elbow_joint
    [-1.6, 1.6],  # left_hip_yaw_joint
    [-1.6, 1.6],  # right_hip_yaw_joint
    [-0.15, 1.72],  # left_knee_joint
    [-0.15, 1.72],  # right_knee_joint
    [-0.5, 0.5],  # left_ankle_pitch_joint
    [-0.5, 0.5],  # right_ankle_pitch_joint
    [-0.26, 0.26],  # left_ankle_roll_joint
    [-0.26, 0.26],  # right_ankle_roll_joint
    [-1.57, 1.57],  # waist_joint
    [-3.1, 3.1],  # left_wrist_joint
    [-3.1, 3.1],  # right_wrist_joint
]

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
        ),
    },
)
