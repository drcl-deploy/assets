# Object model pipeline

Two-script workflow for generating consistent object models usable in both IsaacLab and MuJoCo sim2sim.

> **Generated files are git-ignored, per-machine build products.** URDF + `_cvx_*.xml` + `scenes/`
> bake **absolute paths** (IsaacLab + MuJoCo sim2sim need global paths, don't localize) → regenerate
> locally after cloning (see below).
> **Tracked source of truth:** `<name>.obj`, `metadata.json`, textures, and the CoACD parts under
> `convex_decomp_meshes/*.obj` (frozen collision geometry). Robot models stay tracked too.

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
        +-- convex_decomp_meshes/<name>_cvx_*.obj  (convex parts — TRACKED, reused)
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

# Re-decompose from scratch (overwrites the tracked parts — re-freezes geometry):
python make_object_models.py ../omomo_objects/*/ --threshold 0.03 --force
```

**CoACD runs only when needed.** If the `convex_decomp_meshes/` parts already exist (they're tracked),
the script **reuses them** to re-emit the dcmp XML — no CoACD, no re-decomposition (it only *reads* the
parts for per-part mass fractions). CoACD runs *only* for a brand-new object (no parts yet) or `--force`.
So a fresh clone regenerates every URDF/XML **without CoACD installed** — only re-freezing geometry needs it.
(LFS caveat: `git lfs pull` the real parts before regen, else the reuse step chokes on pointer stubs.)

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
| `--force` | off | Re-run CoACD and **overwrite the tracked parts** (re-freeze geometry); else parts are reused |
| `--no-decompose` | off | Skip CoACD decomposition (only URDF + hull) |
| `--threshold` | `0.05` | CoACD concavity threshold (0.02..0.1) |
| `--max-hulls` | `32` | Cap on convex parts (-1 = no cap) |
| `--preprocess-resolution` | `50` | Voxel resolution for watertight pre-remesh |
| `--seed` | `0` | CoACD RNG seed |
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
3. Run `make_object_models.py` — a new object has no parts yet, so this **first run needs CoACD**.
   **Commit** the resulting `convex_decomp_meshes/*.obj` (the frozen geometry); the URDF/XMLs stay ignored.
4. Run `generate_uolm_scene_xmls.py` for scenes.

## Interactive drop test (`view_drop_test.py`)

Side-by-side physics comparison: LEFT = convex hull, RIGHT = CoACD decomposed.
Requires both `_cvx_hull.xml` and `_cvx_dcmp.xml` to exist (run `make_object_models.py` first).

```bash
python view_drop_test.py ../omomo_objects/trashcan
python view_drop_test.py ../custom_objects/woodchair2
#   SPACE = pause/play,  BACKSPACE = re-drop at new random orientation
```
