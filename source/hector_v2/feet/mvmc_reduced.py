import isaaclab.sim as sim_utils
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg

# TODO (lkrajan): add shared paramters across models as dicts.
STIFFNESS = {
    "l_hip_yaw": 20.0,
    "l_shoulder_yaw": 10.0,
    "r_hip_yaw": 20.0,
    "r_shoulder_yaw": 10.0,
    "l_hip_roll": 20.0,
    "l_shoulder_pitch": 10.0,
    "r_hip_roll": 20.0,
    "r_shoulder_pitch": 10.0,
    "l_hip_pitch": 30.0,
    "l_shoulder_roll": 10.0,
    "r_hip_pitch": 30.0,
    "r_shoulder_roll": 10.0,
    "l_knee": 60.0,  # kp*knee_gear_ratio^2
    "l_elbow": 20.0,  # kp*elbow_gear_ratio^2
    "r_knee": 60.0,  # kp*knee_gear_ratio^2
    "r_elbow": 20.0,  # kp*elbow_gear_ratio^2
    "l_ankle": 15.0,
    "r_ankle": 15.0,
}
DAMPING = {
    "l_hip_yaw": 1.0,
    "l_shoulder_yaw": 0.5,
    "r_hip_yaw": 1.0,
    "r_shoulder_yaw": 0.5,
    "l_hip_roll": 1.0,
    "l_shoulder_pitch": 0.5,
    "r_hip_roll": 1.0,
    "r_shoulder_pitch": 0.5,
    "l_hip_pitch": 1.0,
    "l_shoulder_roll": 0.5,
    "r_hip_pitch": 1.0,
    "r_shoulder_roll": 0.5,
    "l_knee": 2.0,  # kd*knee_gear_ratio^2
    "l_elbow": 1.0,  # kd*elbow_gear_ratio^2
    "r_knee": 2.0,  # kd*knee_gear_ratio^2
    "r_elbow": 1.0,  # kd*elbow_gear_ratio^2
    "l_ankle": 0.5,
    "r_ankle": 0.5,
}
import os

ASSETS_DIR = os.environ.get("SIM_ASSETS_PATH")

MPCL = [
    [-0.523599, 0.523599],  # l_hip_yaw_joint
    [-1.309, 1.309],  # l_shoulder_yaw_joint
    [-0.523599, 0.523599],  # r_hip_yaw_joint
    [-1.309, 1.309],  # r_shoulder_yaw_joint
    [-0.349066, 0.7900000214576721],  # l_hip_roll_joint
    [-2.35619, 2.61799],  # l_shoulder_pitch_joint
    [-0.7900000214576721, 0.349066],  # r_hip_roll_joint
    [-2.35619, 2.61799],  # r_shoulder_pitch_joint
    [-0.3, 2.1],  # l_hip_pitch_joint
    [-1.5708, 0.0],  # l_shoulder_roll_joint
    [-0.3, 2.1],  # r_hip_pitch_joint
    [-0.0, 1.5708],  # r_shoulder_roll_joint
    [-2.0, 0.0],  # l_knee_joint, joint limits * knee_gear_ratio
    [-3.70969733, 3.70969733],  # l_elbow_joint
    [-2.0, 0.0],  # r_knee_joint, joint limits * knee_gear_ratio
    [-3.70969733, 3.70969733],  # r_elbow_joint
    [-1.57, 0.7900000214576721],  # l_ankle_joint
    [-1.57, 0.7900000214576721],  # r_ankle_joint
]

# model variants
WITHOUT_COUPLING_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=os.path.join(ASSETS_DIR, "hector_v2/feet/mvmc_reduced.urdf"),
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
        fix_base=True,
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
        # pos=(0.0, 0.0, 0.55), # when fix_root_link=False
        pos=(0.0, 0.0, 0.65),  # when fix_root_link=True
        joint_pos={
            "l_hip_yaw": 0.0,
            "l_shoulder_yaw": 0.0,
            "r_hip_yaw": 0.0,
            "r_shoulder_yaw": 0.0,
            "l_hip_roll": 0.0,
            "l_shoulder_pitch": 0.785,
            "r_hip_roll": 0.0,
            "r_shoulder_pitch": 0.785,
            "l_hip_pitch": 0.7848373651504517,
            "l_shoulder_roll": 0.0,
            "r_hip_pitch": 0.7848373651504517,
            "r_shoulder_roll": 0.0,
            "l_knee": -1.57,
            "l_elbow": -1.57,
            "r_knee": -1.57,
            "r_elbow": -1.57,
            "l_ankle": 0.7848373651504517,
            "r_ankle": 0.7848373651504517,
        },
        joint_vel={".*": 0.0},
    ),
    actuators={
        "limbs": ImplicitActuatorCfg(
            joint_names_expr=[
                "l_hip_yaw",
                "l_shoulder_yaw",
                "r_hip_yaw",
                "r_shoulder_yaw",
                "l_hip_roll",
                "l_shoulder_pitch",
                "r_hip_roll",
                "r_shoulder_pitch",
                "l_hip_pitch",
                "l_shoulder_roll",
                "r_hip_pitch",
                "r_shoulder_roll",
                "l_knee",
                "l_elbow",
                "r_knee",
                "r_elbow",
                "l_ankle",
                "r_ankle",
            ],
            effort_limit={
                "l_hip_yaw": 33.5,
                "l_shoulder_yaw": 17.0,
                "r_hip_yaw": 33.5,
                "r_shoulder_yaw": 17.0,
                "l_hip_roll": 33.5,
                "l_shoulder_pitch": 17.0,
                "r_hip_roll": 33.5,
                "r_shoulder_pitch": 17.0,
                "l_hip_pitch": 33.5,
                "l_shoulder_roll": 17.0,
                "r_hip_pitch": 33.5,
                "r_shoulder_roll": 17.0,
                "l_knee": 67.0,  # motor_tau_max*knee_gear_ratio
                "l_elbow": 24.089,  # motor_tau_max*elbow_gear_ratio
                "r_knee": 67.0,  # motor_tau_max*knee_gear_ratio
                "r_elbow": 24.089,  # motor_tau_max*elbow_gear_ratio
                "l_ankle": 33.5,
                "r_ankle": 33.5,
            },
            velocity_limit={
                "l_hip_yaw": 21.0,
                "l_shoulder_yaw": 32.0,
                "r_hip_yaw": 21.0,
                "r_shoulder_yaw": 32.0,
                "l_hip_roll": 21.0,
                "l_shoulder_pitch": 32.0,
                "r_hip_roll": 21.0,
                "r_shoulder_pitch": 32.0,
                "l_hip_pitch": 21.0,
                "l_shoulder_roll": 32.0,
                "r_hip_pitch": 21.0,
                "r_shoulder_roll": 32.0,
                "l_knee": 10.5,  # motor_speed_max/knee_gear_ratio
                "l_elbow": 22.582921665,  # motor_speed_max/elbow_gear_ratio
                "r_knee": 10.5,  # motor_speed_max/knee_gear_ratio
                "r_elbow": 22.582921665,  # motor_speed_max/elbow_gear_ratio
                "l_ankle": 21.0,
                "r_ankle": 21.0,
            },
            stiffness=STIFFNESS,
            damping=DAMPING,
        ),
    },
)
