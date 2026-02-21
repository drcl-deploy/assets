"""
This script loads all omomo objects and simulates them in isaaclab in a grid layout.
"""

import os
import argparse
import math

from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(
    description="This script loads omomo objects and simulates them in isaaclab"
)
parser.add_argument(
    "--object",
    type=str,
    default=None,
    help="Specific object to load (e.g. 'CHAIR'). If not provided, loads all objects.",
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
import torch
import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObject
from isaaclab.sim import SimulationContext

sys.path.append("./")

from source.omomo_objects.omomo_objects import OBJECT_CONFIGS


def main():
    """Main function."""

    # Load kit helper
    sim = SimulationContext(
        sim_utils.SimulationCfg(
            device="cuda",
            dt=1 / 120,
            render_interval=4,
        )
    )
    # Set main camera
    sim.set_camera_view(eye=[5.0, 5.0, 5.0], target=[0.0, 0.0, 0.0])

    # Spawn things into stage
    # Ground-plane
    cfg = sim_utils.GroundPlaneCfg()
    cfg.func("/World/defaultGroundPlane", cfg)
    # Lights
    cfg = sim_utils.DomeLightCfg(intensity=2000.0, color=(0.75, 0.75, 0.75))
    cfg.func("/World/Light", cfg)

    # Get objects to load
    if args_cli.object:
        # Load specific object
        object_name = args_cli.object.upper()
        if object_name not in OBJECT_CONFIGS:
            print(f"[ERROR]: Object '{object_name}' not found in OBJECT_CONFIGS")
            print(f"Available objects: {list(OBJECT_CONFIGS.keys())}")
            exit(1)
        objects_to_load = {object_name: OBJECT_CONFIGS[object_name]}
    else:
        # Load all objects
        objects_to_load = OBJECT_CONFIGS

    n_objects = len(objects_to_load)
    print(f"[INFO]: Loading {n_objects} objects: {list(objects_to_load.keys())}")

    # Calculate grid layout (closest to square)
    n_cols = int(math.ceil(math.sqrt(n_objects)))
    n_rows = int(math.ceil(n_objects / n_cols))
    spacing = 1.5  # meters between objects

    # Create origins for grid placement
    origins = []
    for i in range(n_objects):
        row = i // n_cols
        col = i % n_cols
        x = (col - n_cols / 2) * spacing
        y = (row - n_rows / 2) * spacing
        origins.append([x, y, 0.5])  # Start slightly above ground

    origins = torch.tensor(origins, device=sim.device)

    # Load objects
    rigid_objects = []
    object_names = []
    
    for idx, (name, obj_cfg) in enumerate(objects_to_load.items()):
        try:
            obj = RigidObject(obj_cfg.replace(prim_path=f"/World/object_{idx}"))
            rigid_objects.append(obj)
            object_names.append(name)
            print(f"[INFO]: Loaded object {idx}: {name}")
        except Exception as e:
            print(f"[WARNING]: Failed to load {name}: {e}")

    if not rigid_objects:
        print("[ERROR]: No objects were loaded successfully")
        exit(1)

    # Play the simulator
    sim.reset()

    # Now we are ready!
    print("[INFO]: Setup complete...")
    os.system("clear")

    # Print object information
    print(f"\n{'='*60}")
    print(f"Loaded {len(rigid_objects)} objects:")
    print(f"{'='*60}")
    
    for idx, (obj, name) in enumerate(zip(rigid_objects, object_names)):
        print(f"\nObject {idx}: {name}")
        print(f"  Position: {origins[idx].tolist()}")
        print(f"  Bodies: {obj.body_names}")
        if hasattr(obj.data, 'default_mass'):
            total_mass = obj.data.default_mass.sum().item()
            print(f"  Total mass: {total_mass:.4f} kg")

    print(f"\n{'='*60}")
    print("Simulation running. Close the window to exit.")
    print(f"{'='*60}\n")

    sim_dt = sim.get_physics_dt()
    sim_time = 0.0
    count = 0
    reset_interval = 500  # Reset every N steps

    while simulation_app.is_running():
        # Reset periodically
        if count % reset_interval == 0:
            sim_time = 0.0
            for idx, obj in enumerate(rigid_objects):
                # Reset object state
                root_state = obj.data.default_root_state.clone()
                root_state[:, :3] += origins[idx]
                obj.write_root_state_to_sim(root_state)
                obj.reset()
            print(f"[INFO]: Reset at step {count}")

        # Step the simulation
        sim.step()

        # Update sim-time
        sim_time += sim_dt
        count += 1

        # Update object buffers
        for obj in rigid_objects:
            obj.update(sim_dt)


if __name__ == "__main__":
    # run the main function
    main()
    simulation_app.close()