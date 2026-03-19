import os
from pathlib import Path
import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg
from isaaclab.sim.spawners.materials import RigidBodyMaterialCfg


ASSETS_DIR = os.environ.get("SIM_ASSETS_PATH")

dir_path = Path(__file__).parent

def create_rigid_object_cfg(folder_name: str):
    """Create a RigidObjectCfg for a given folder."""
    print("asset_path: ", os.path.join(ASSETS_DIR, folder_name, folder_name + ".urdf")  )
    return sim_utils.UrdfFileCfg(
                                fix_base=False,
                                replace_cylinders_with_capsules=True,
                                asset_path=os.path.join(ASSETS_DIR,'omomo_objects', folder_name, folder_name + ".urdf"),
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
                                collider_type = "convex_decomposition"
                            )
# Build config dictionary
OBJECT_CONFIGS = {}
for folder in os.listdir(dir_path):
    folder_path = dir_path / folder
    if folder_path.is_dir() and not folder.startswith('__'):
        OBJECT_CONFIGS[folder.upper()] = create_rigid_object_cfg(folder)


# remove eveyrthing that has a box in the name

OMOMO_OBJECTS_CFG = RigidObjectCfg(
                                    prim_path="{ENV_REGEX_NS}/Object",
                                    spawn=sim_utils.MultiAssetSpawnerCfg(
                                                    assets_cfg=list(OBJECT_CONFIGS.values()),
                                                    random_choice=False,
                                                    semantic_tags=list( (("class", folder_name) for folder_name in OBJECT_CONFIGS.keys()) ),
                                                    activate_contact_sensors=True
                                                ),
                                    init_state=RigidObjectCfg.InitialStateCfg(
                                        pos=(0.0, 0.0, 0.1213), lin_vel=(0.0, 0.0, 0.0)
                                    ),
                                )

