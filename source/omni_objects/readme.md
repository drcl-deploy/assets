# Object model pipeline

Two-script workflow for generating consistent object models usable in both IsaacLab and MuJoCo sim2sim.

> **Note:** Generated files contain absolute paths and are **not portable** across machines.
> Re-generate locally after cloning.

## Workflow

```
metadata.json + .obj mesh
        |
        v
 make_object_models.py          # Step 1: per-object model files
        |
        +-- <name>.urdf                 (auto-computed inertia)
        +-- <name>_cvx_hull.xml         (MuJoCo body: single convex hull)
        +-- <name>_cvx_dcmp.xml         (MuJoCo body: CoACD decomposed)
        +-- collision/<name>_cvx_*.obj  (convex parts)
        |
        v
 generate_uolm_scene_xmls.py   # Step 2: robot + object scene
        |
        +-- scenes/<robot>_<object>.xml
```

## Step 1: generate object models

```bash
# All objects:
python make_object_models.py --all

# Single object:
python make_object_models.py ../custom_objects/tire

# Hull only (skip CoACD decomposition):
python make_object_models.py --all --no-decompose

# Tighter decomposition:
python make_object_models.py ../omomo_objects/*/ --threshold 0.03 --force
```

Each object directory needs:
- `<name>.obj` — visual/collision mesh
- `metadata.json` — with fields: `mass`, `initial_pos`, `initial_quat`, `texture`

```json
{
  "mass": 0.8,
  "initial_pos": "1.0 0.0 0.3",
  "initial_quat": "1 0 0 0",
  "texture": "source/textures/Wood/Bamboo_Planks/Bamboo_Planks_BaseColor.png"
}
```

**Inertia** is auto-computed from mesh geometry assuming homogeneous density (trimesh). Non-watertight meshes fall back to convex hull for volume estimation.

| Flag | Default | Description |
|---|---|---|
| `--all` | off | Process every object in `OBJECT_GROUP_PATTERNS` |
| `--object` | *(all)* | Process a single object by name (with `--all`) |
| `--force` | off | Regenerate even if outputs exist |
| `--no-decompose` | off | Skip CoACD decomposition (only URDF + hull) |
| `--threshold` | `0.05` | CoACD concavity threshold (0.02..0.1) |
| `--max-hulls` | `-1` | Cap on convex parts (-1 = none) |
| `--quiet` | off | Silence CoACD logging |

## Step 2: generate scene XMLs

```bash
# All objects:
python generate_uolm_scene_xmls.py --robot-xml /path/to/g1_29dof.xml

# Single object:
python generate_uolm_scene_xmls.py --robot-xml /path/to/g1_29dof.xml --object trashcan

# Use decomposed collision model:
python generate_uolm_scene_xmls.py --robot-xml /path/to/g1_29dof.xml --model dcmp
```

Scene XMLs use `<include>` for both robot and object — no inlined bodies. The generated file has both hull and dcmp includes (one commented out) for easy swapping during sim2sim.

| Flag | Default | Description |
|---|---|---|
| `--robot-xml` | *(prompt)* | Absolute path to robot MuJoCo XML |
| `--object` | *(all)* | Generate for a single object only |
| `--model` | `hull` | Object collision model: `hull` or `dcmp` |
| `--out-dir` | `scenes/` | Output directory |

## Adding a new object

1. Create `source/<group>/<name>/` with `<name>.obj` and `metadata.json`
2. Add the group pattern to `object_groups.py` (if new group)
3. Run `make_object_models.py` then `generate_uolm_scene_xmls.py`

## Interactive drop test (`view_drop_test.py`)

Side-by-side physics comparison: LEFT = convex hull, RIGHT = CoACD decomposed.
Requires both `_cvx_hull.xml` and `_cvx_dcmp.xml` to exist (run `make_object_models.py` first).

```bash
python view_drop_test.py ../omomo_objects/trashcan
python view_drop_test.py ../custom_objects/woodchair2
#   SPACE = pause/play,  BACKSPACE = re-drop at new random orientation
```
