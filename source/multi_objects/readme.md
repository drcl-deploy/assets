# Multi-Object MuJoCo Scene Generator

Generates MuJoCo MJCF scene XMLs that compose a Unitree robot with a single dynamic object from the assets repo.

## Quick Start

```bash
# Generate scenes for all objects (default: G1 / 29dof)
python generate_mujoco_scenes.py

# Single object
python generate_mujoco_scenes.py --object trashcan

# Custom spawn position
python generate_mujoco_scenes.py --object trashcan --object-pos "0.5 0 0.5"

# Different robot / scene variant
python generate_mujoco_scenes.py --robot g1 --robot-scene scene_29dof.xml
```

Generated scenes land in `scenes/`:

```
scenes/
  scene_g1_29dof_basketball.xml
  scene_g1_29dof_trashcan.xml
  scene_g1_29dof_woodchair.xml
  ...
  meshes -> <robot_meshes_dir>   # symlink, created automatically
```

## Usage with unitree_mujoco

Point `config.yaml` at a generated scene:

```yaml
robot_scene: "/HDD/drcl_projects/assets/source/multi_objects/scenes/scene_g1_29dof_trashcan.xml"
```

No changes to `unitree_mujoco` needed -- `main.cc` already supports absolute `robot_scene` paths.

## How It Works

- **No asset duplication.** Scene XMLs reference meshes via absolute paths (`<mesh file="/HDD/.../trashcan.obj"/>`).
- **Symlink for robot meshes.** MuJoCo resolves `meshdir` relative to the top-level file, not the included file. The generator creates `scenes/meshes -> <robot_meshes_dir>` so the robot `<include>` resolves correctly.
- **Auto-computed inertia.** Mass is set on `<geom>` with no `<inertial>` element. MuJoCo derives CoM, principal axes, and inertia tensor from mesh geometry. This sidesteps bad URDF inertia values (e.g. negative diaginertia in `monitor`, `largebox`).

## CLI Reference

| Flag | Default | Description |
|---|---|---|
| `--robot` | `g1` | Robot name |
| `--robot-scene` | `scene_29dof.xml` | Base robot scene file |
| `--object` | *(all)* | Generate for a single object only |
| `--object-pos` | `1.0 0.0 0.3` | Object spawn position `x y z` |
| `--out-dir` | `scenes/` | Output directory |
