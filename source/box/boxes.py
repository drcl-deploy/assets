import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg
from isaaclab.sim.spawners.materials import PreviewSurfaceCfg, RigidBodyMaterialCfg
import os

ASSETS_DIR = os.environ.get("SIM_ASSETS_PATH")

CUBE_SIZE = 0.4  # meters (adjust as needed)
CUBE_HEIGHT = CUBE_SIZE  # for a cube
CARDBOARD_BOX_CFG = RigidObjectCfg(
    prim_path="{ENV_REGEX_NS}/Cube",
    spawn=sim_utils.CuboidCfg(
        size=(CUBE_SIZE, CUBE_SIZE, CUBE_HEIGHT),
        visual_material=PreviewSurfaceCfg(
            # Cardboard-like color #C19A6C → sRGB ~ (193,154,108)/255
            diffuse_color=(193/255.0, 154/255.0, 108/255.0),
            metallic=0.25,
            roughness=0.6,
        ),
        physics_material=RigidBodyMaterialCfg(static_friction=0.3, dynamic_friction=0.3),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(),
        mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
        collision_props=sim_utils.CollisionPropertiesCfg(),
        activate_contact_sensors=False,
    ),
    init_state=RigidObjectCfg.InitialStateCfg(
        pos=(0.0, 0.0, CUBE_HEIGHT / 2), lin_vel=(0.0, 0.0, 0.0)
    ),
)