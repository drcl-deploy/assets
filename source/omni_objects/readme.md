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

---

# Convex colliders (`make_convex_colliders.py`)

Standalone, independent of the scene generator. MuJoCo collides a `<geom type="mesh">` as a
single **convex hull** (no auto-decomposition, unlike IsaacLab/PhysX) → concave objects get
phantom contacts. This runs **CoACD** offline and writes a single-body **multi-geom** collider
that MuJoCo treats exactly. Wire it into scenes yourself when needed.

```bash
pip install coacd
# one object (dir or .obj):
python make_convex_colliders.py ../custom_objects/woodchair2
# batch + tighter fit:
python make_convex_colliders.py ../omomo_objects/*/ --threshold 0.03 --force
# interactive physics DROP TEST: BEFORE (single hull) | AFTER (decomposed), contacts on:
python make_convex_colliders.py ../custom_objects/woodchair2 --view
#   SPACE = pause/play,  BACKSPACE = re-drop at a new random orientation
```

Per object `<dir>/<name>.obj` it writes, **inside that folder**:

```
<dir>/collision/<name>_cvx_000.obj ...   # convex parts
<dir>/<name>_collision.xml               # one body + freejoint + N mesh geoms (loadable alone)
```

Mass is read from a sibling `<name>.urdf` (else 1.0) and split across parts by volume.
e.g. `woodchair2` → 28 parts, AABB matches source to ~7 mm.

| Flag | Default | Description |
|---|---|---|
| `--threshold` | `0.05` | CoACD concavity; lower = more parts = tighter (0.02..0.1) |
| `--max-hulls` | `-1` | cap on convex parts (-1 = none) |
| `--preprocess-resolution` | `50` | voxel res for the watertight pre-remesh |
| `--seed` | `0` | deterministic |
| `--force` | off | redo even if `<name>_collision.xml` exists |
| `--quiet` | off | silence CoACD's own logging |
| `--view` | off | interactive drop test (hull vs decomposed); SPACE=pause, BACKSPACE=re-drop |
