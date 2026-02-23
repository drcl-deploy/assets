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
    "--num_objects",
    type=int,
    default=30,
    help="Number of object instances to spawn (default: 30)",
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

from source.omomo_objects.omomo_objects import OMOMO_OBJECTS_CFG


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
    sim.set_camera_view(eye=[10.0, 10.0, 8.0], target=[0.0, 0.0, 0.0])

    # Spawn things into stage
    # Ground-plane
    cfg = sim_utils.GroundPlaneCfg()
    cfg.func("/World/defaultGroundPlane", cfg)
    # Lights
    cfg = sim_utils.DomeLightCfg(intensity=2000.0, color=(0.75, 0.75, 0.75))
    cfg.func("/World/Light", cfg)

    n_objects = args_cli.num_objects
    print(f"[INFO]: Spawning {n_objects} random object instances")

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

    # Spawn objects using MultiAssetSpawnerCfg (random selection)
    # Create multiple prim paths for each instance
    rigid_objects = []
    for idx in range(n_objects):
        obj_cfg = OMOMO_OBJECTS_CFG.replace(prim_path=f"/World/Object_{idx}")
        obj = RigidObject(obj_cfg)
        rigid_objects.append(obj)
        print(f"[INFO]: Spawned object instance {idx}")

    # Play the simulator
    sim.reset()

    # Now we are ready!
    print("[INFO]: Setup complete...")
    os.system("clear")

    # Print object information
    print(f"\n{'='*60}")
    print(f"Spawned {len(rigid_objects)} random object instances")
    print(f"Grid: {n_rows} rows x {n_cols} cols, spacing: {spacing}m")
    print(f"{'='*60}")

    for idx, obj in enumerate(rigid_objects):
        print(f"  Object {idx}: pos={origins[idx].tolist()}, bodies={obj.body_names}")

    print(f"\n{'='*60}")
    print("Simulation running. Close the window to exit.")
    print(f"{'='*60}\n")

    sim_dt = sim.get_physics_dt()
    sim_time = 0.0
    count = 0
    reset_interval = 100  # Reset every N steps

    while simulation_app.is_running():
        # Reset periodically
        if count % reset_interval == 0:
            sim_time = 0.0
            for idx, obj in enumerate(rigid_objects):
                # Reset object state
                root_state = obj.data.default_root_state.clone()
                root_state[:, :3] = origins[idx]
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