import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg
from isaaclab.sim.spawners.materials import PreviewSurfaceCfg, RigidBodyMaterialCfg
import os

ASSETS_DIR = os.environ.get("SIM_ASSETS_PATH")
BALL_RADIUS = 0.16 #0.1213  # meters (standard basketball size5 radius)

# BASKETBALL_CFG = RigidObjectCfg(
#     prim_path="{ENV_REGEX_NS}/basketball",
#     spawn=sim_utils.SphereCfg(
#         radius=BALL_RADIUS,  # meters
#         # visual_material=PreviewSurfaceCfg(
#         #     # Cardboard-like color #C19A6C → sRGB ~ (193,154,108)/255
#         #     diffuse_color=(193 / 255.0, 154 / 255.0, 108 / 255.0),
#         #     metallic=0.25,
#         #     roughness=0.6,
#         # ),
#         visual_material_path = "/HDD/drcl_projects/assets/source/basketball/basketball.png",
#         physics_material=RigidBodyMaterialCfg(
#             static_friction=0.3, dynamic_friction=0.3
#         ),
#         rigid_props=sim_utils.RigidBodyPropertiesCfg(),
#         mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
#         collision_props=sim_utils.CollisionPropertiesCfg(),
#         activate_contact_sensors=False,
#     ),
#     init_state=RigidObjectCfg.InitialStateCfg(
#         pos=(0.0, 0.0, 0.1213), lin_vel=(0.0, 0.0, 0.0)
#     ),
# )


# using ursdf for texture 
BASKETBALL_CFG = RigidObjectCfg(
    prim_path="{ENV_REGEX_NS}/basketball",
    spawn=sim_utils.UrdfFileCfg(
        fix_base=False,
        replace_cylinders_with_capsules=True,
        asset_path=os.path.join(ASSETS_DIR, "basketball/basketball.urdf"),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(
                stiffness=0, damping=0
            )
        ),
    ),
    init_state=RigidObjectCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.1213), lin_vel=(0.0, 0.0, 0.0)
    ),
)
