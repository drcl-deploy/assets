# UOLM scene generator

Generates MuJoCo scene XMLs: robot + single dynamic object (UniObject Loco Manipulation).

> **Note:** `scenes/` contains absolute paths and is **not portable** across machines.
> Do NOT copy scene XMLs between devices -- re-generate them locally with `generate_uolm_scene_xmls.py`.

## usage

```bash
# All objects (prompts for robot XML path):
python generate_uolm_scene_xmls.py

# Pass robot XML directly:
python generate_uolm_scene_xmls.py --robot-xml /path/to/unitree_robots/g1/g1_29dof.xml

# Single object:
python generate_uolm_scene_xmls.py --object trashcan
```

Output lands in `scenes/` (gitignored, generated per-machine):

```bash
# <robot>_<object>.xml
scenes/
  g1_29dof_trashcan.xml
  g1_29dof_woodchair.xml
  ...
  meshes -> <robot_meshes_dir>   # symlink, auto-created
```

## rationale

- **No asset duplication.** Meshes/textures referenced via absolute paths, auto-detected from script location.
- **Robot meshdir symlink.** MuJoCo resolves `meshdir` relative to the top-level file. The generator creates `scenes/meshes -> <robot_meshes_dir>` so `<include>` resolves correctly.
- **Auto-computed inertia.** Mass set on `<geom>`, no `<inertial>`. MuJoCo derives CoM and inertia from geometry.

## cli

| Flag | Default | Description |
|---|---|---|
| `--robot-xml` | *(prompt)* | Absolute path to robot MuJoCo XML |
| `--object` | *(all)* | Generate for a single object only |
| `--out-dir` | `scenes/` | Output directory |
