"""
This script loads all omomo objects and simulates them in isaaclab in a grid layout.
"""

import os
import argparse

from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(
    description="This script loads omomo objects and simulates them in isaaclab"
)
parser.add_argument(
    "--num_objects",
    type=int,
    default=30,
    help="Number of object instances to spawn (default: 30)",
)
parser.add_argument(
    "--object_names",
    type=str,
    nargs="+",
    default=None,
    help="Subset of object folder names to retain (default: all). e.g. --object_names suitcase trashcan",
)

# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import sys
import isaaclab.sim as sim_utils
from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
from isaaclab.sim import SimulationContext
from isaaclab.utils import configclass

sys.path.append("./")

from source.multi_objects.multi_objects import MULTI_OBJECTS_CFG


def filter_objects(object_cfg, object_names):
    """Filter MultiAssetSpawnerCfg assets/semantic_tags to retain only `object_names`.

    Mirrors the filtering pattern used in omni_object_env_cfgs.py.
    """
    if object_names is None:
        return object_cfg

    all_objects = [tag[1].lower() for tag in object_cfg.spawn.semantic_tags]
    assets_cfg_filtered = []
    semantic_tags_filtered = []
    for i, name in enumerate(all_objects):
        if name in object_names:
            print(f"[INFO] retained object {name}")
            assets_cfg_filtered.append(object_cfg.spawn.assets_cfg[i])
            semantic_tags_filtered.append(object_cfg.spawn.semantic_tags[i])
        else:
            print(f"[INFO] removed object {name}")

    object_cfg.spawn.assets_cfg = assets_cfg_filtered
    object_cfg.spawn.semantic_tags = semantic_tags_filtered

    print("[INFO] finalized objects in scene:")
    for tag in object_cfg.spawn.semantic_tags:
        print(f" - {tag[1].lower()}")

    return object_cfg


@configclass
class OmomoObjectsSceneCfg(InteractiveSceneCfg):
    """Scene with one MultiAssetSpawner-driven object per env (round-robin)."""

    # the object cfg uses prim_path="{ENV_REGEX_NS}/Object" which is what
    # triggers MultiAssetSpawnerCfg's round-robin distribution across envs
    object = MULTI_OBJECTS_CFG


def main():
    """Main function."""

    sim = SimulationContext(
        sim_utils.SimulationCfg(
            device="cuda",
            dt=1 / 120,
            render_interval=4,
        )
    )
    sim.set_camera_view(eye=[10.0, 10.0, 8.0], target=[0.0, 0.0, 0.0])

    # Ground + lights at the world root (not scene entities)
    sim_utils.GroundPlaneCfg().func("/World/defaultGroundPlane", sim_utils.GroundPlaneCfg())
    sim_utils.DomeLightCfg(intensity=2000.0, color=(0.75, 0.75, 0.75)).func(
        "/World/Light", sim_utils.DomeLightCfg(intensity=2000.0, color=(0.75, 0.75, 0.75))
    )

    n_objects = args_cli.num_objects
    print(f"[INFO]: Spawning {n_objects} object instances via InteractiveScene")

    # InteractiveScene clones {ENV_REGEX_NS}/Object across num_envs in a single
    # spawn call, which is when MultiAssetSpawnerCfg(random_choice=False)
    # distributes assets round-robin (env_i -> asset[i % num_assets]).
    # NOTE: replicate_physics MUST be False — otherwise the cloner only spawns
    # into env_0 and physics-replicates the same prim to all other envs, so
    # MultiAssetSpawnerCfg sees a single prim_path and can't round-robin.
    scene_cfg = OmomoObjectsSceneCfg(
        num_envs=n_objects, env_spacing=1.5, replicate_physics=False
    )
    scene_cfg.object = filter_objects(scene_cfg.object, args_cli.object_names)
    scene = InteractiveScene(scene_cfg)

    sim.reset()
    print("[INFO]: Setup complete...")
    os.system("clear")

    obj = scene["object"]
    print(f"\n{'='*60}")
    print(f"Spawned {scene.num_envs} object instances")
    print(f"env_spacing: {scene_cfg.env_spacing}m")
    print(f"{'='*60}")
    print(f"Object body_names: {obj.body_names}")
    print(f"\n{'='*60}")
    print("Simulation running. Close the window to exit.")
    print(f"{'='*60}\n")

    sim_dt = sim.get_physics_dt()
    sim_time = 0.0
    count = 0
    reset_interval = 10000

    while simulation_app.is_running():
        if count % reset_interval == 0:
            sim_time = 0.0
            root_state = obj.data.default_root_state.clone()
            root_state[:, :3] += scene.env_origins
            obj.write_root_state_to_sim(root_state)
            scene.reset()
            print(f"[INFO]: Reset at step {count}")

        scene.write_data_to_sim()
        sim.step()
        sim_time += sim_dt
        count += 1
        scene.update(sim_dt)


if __name__ == "__main__":
    main()
    simulation_app.close()
