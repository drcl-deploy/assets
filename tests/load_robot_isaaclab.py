"""
This script loads model simulates in isaaclab

"""

# TODO (lkrajan): currently simulates zero ctrl input, should add joint trajectory tracking
import argparse
import os

from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(description="This script loads model simulates in isaaclab")
parser.add_argument(
    "--robot", required=True, help="module path, e.g. assets.hector_v2.feet.isaaclab"
)
parser.add_argument("--cfg", required=True, help="config name, e.g. WITH_COUPLING_CFG")
parser.add_argument("--n_robots", type=int, default=25, help="number of robots to load")

# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import importlib

import isaaclab.sim as sim_utils
import torch
from isaaclab.assets import Articulation
from isaaclab.sim import SimulationContext


def main():
    """Main function."""

    # Load kit helper
    sim = SimulationContext(
        sim_utils.SimulationCfg(
            device="cuda",
            dt=1 / 120,
            render_interval=4,
            # dt=1/1000,
            # render_interval=10,
        )
    )
    # Set main camera
    sim.set_camera_view(eye=[3.5, 3.5, 3.5], target=[0.0, 0.0, 0.0])

    # Spawn things into stage
    # Ground-plane
    cfg = sim_utils.GroundPlaneCfg()
    cfg.func("/World/defaultGroundPlane", cfg)
    # Lights
    cfg = sim_utils.DomeLightCfg(intensity=2000.0, color=(0.75, 0.75, 0.75))
    cfg.func("/World/Light", cfg)
    N_ROBOTS = args_cli.n_robots
    # split N_ROBOTS into a rectangle closest to a square
    n_cols = int(N_ROBOTS**0.5)
    n_rows = int(N_ROBOTS / n_cols)

    origins = torch.tensor(
        [[i - n_cols / 2, j - n_rows / 2, 0.0] for i in range(n_cols) for j in range(n_rows)],
        device=sim.device,
    )

    # load a goalpost

    # load N_ROBOTS and append to robots
    try:
        robot_module = importlib.import_module(args_cli.robot)
        robot_cfg = getattr(robot_module, args_cli.cfg)
    except (ImportError, AttributeError) as e:
        print(f"[ERROR]: robot cfg not found: {e}")
        exit(1)

    robots = []
    for i in range(N_ROBOTS):
        robot = Articulation(robot_cfg.replace(prim_path=f"/World/robot_{i}"))
        robots.append(robot)

    # Play the simulator
    sim.reset()

    # Now we are ready!
    print("[INFO]: Setup complete...")
    os.system("clear")

    # print robot information of the first instance
    robot = robots[0]
    print("Robot 0")

    # print bodies and masses
    print("robot bodies")
    total_mass = 0.0
    for i, (body, mass) in enumerate(zip(robot.body_names, robot.data.default_mass.flatten())):
        print(f"\tbody {i}: {body} with mass: {mass}")
        total_mass += mass
    print(f"Total mass: {total_mass}")

    # print joints
    joint_ids, joint_names = robot.find_joints(".*")

    print("robot joints")
    for i, (
        joint_id,
        joint_name,
        joint_friction,
        joint_limits,
    ) in enumerate(
        zip(
            joint_ids,
            robot.joint_names,
            robot.data.joint_friction[0],
            robot.data.default_joint_limits[0],
        )
    ):
        print(
            "\tjnt",
            joint_id,
            joint_name,
            torch.round(joint_friction, decimals=2).tolist(),
            torch.round(joint_limits, decimals=2).tolist(),
        )

    for actuator in robot.actuators:
        print("actuator group: ", actuator)
        actuator = robot.actuators[actuator]
        i = 0
        for ajn, akp, akd in zip(
            actuator.joint_names,
            actuator.stiffness.flatten(),
            actuator.damping.flatten(),
        ):
            print(
                "\tact",
                i,
                ajn,
                torch.round(akp, decimals=2).tolist(),
                torch.round(akd, decimals=2).tolist(),
                # ROBOT_MPCL[i],
            )
            i += 1

    sim_dt = sim.get_physics_dt()
    sim_time = 0.0
    count = 0
    count_per_dof = 100

    joint_positions = []
    joint_velocities = []
    while simulation_app.is_running():
        # reset
        if count % count_per_dof == 0:
            sim_time = 0.0
            count = 0
            for index, robot in enumerate(robots):
                # reset dof state
                joint_pos, joint_vel = (
                    robot.data.default_joint_pos,
                    robot.data.default_joint_vel,
                )
                robot.write_joint_state_to_sim(joint_pos, joint_vel)
                root_state = robot.data.default_root_state.clone()
                root_state[:, :3] += origins[index]
                robot.write_root_state_to_sim(root_state)
                robot.reset()
                robot.write_data_to_sim()
            # reset
            print(">>>>>>>> Reset!")

        joint_positions.append(robot.data.joint_pos.clone())
        joint_velocities.append(robot.data.joint_vel.clone())
        # step the simulation
        sim.step()
        # update sim-time
        sim_time += sim_dt
        count += 1

        # update buffers
        for index, robot in enumerate(robots):
            robot.update(sim_dt)

    # make buffers into tensors
    joint_positions = torch.stack(joint_positions)
    joint_velocities = torch.stack(joint_velocities)

    # reshape the tensors
    joint_positions = joint_positions.permute(0, 2, 1).squeeze()
    joint_velocities = joint_velocities.permute(0, 2, 1).squeeze()

    # move it to cpu and make it numpy
    joint_positions = joint_positions.cpu().numpy()
    joint_velocities = joint_velocities.cpu().numpy()

    # make a plot 2x5
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(
        4,
        # 5,
        int(joint_positions.shape[1] / 2),
        figsize=(40, 10),
    )
    fig.suptitle("jpos, jvel and mcom")

    joint_limits = robot.data.default_joint_limits[0].cpu().numpy()

    for i in range(int(joint_positions.shape[1] / 2)):
        axs[0, i].plot(joint_positions[:, 2 * i], label="joint position")
        axs[1, i].plot(joint_positions[:, 2 * i + 1], label="joint position")

        axs[0, i].axhline(y=joint_limits[2 * i, 0], color="b", linestyle="--")
        axs[0, i].axhline(y=joint_limits[2 * i, 1], color="b", linestyle="--")
        axs[1, i].axhline(y=joint_limits[2 * i + 1, 0], color="b", linestyle="--")
        axs[1, i].axhline(y=joint_limits[2 * i + 1, 1], color="b", linestyle="--")

        axs[2, i].plot(joint_velocities[:, 2 * i], label="joint velocity")
        axs[3, i].plot(joint_velocities[:, 2 * i + 1], label="joint velocity")

    for ax in axs.flat:
        ax.set(xlabel="time", ylabel="value")
        ax.grid()
        ax.legend()

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    # run the main function
    main()
    simulation_app.close()
