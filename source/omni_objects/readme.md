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
        +-- <name>.urdf                 (inertial from metadata / auto-computed)
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
the script **reuses them** to re-emit the dcmp XML — no CoACD, no re-decomposition, no mesh loading
(mass is body-level now, so the parts are referenced by path only). CoACD runs *only* for a
brand-new object (no parts yet) or `--force`.
So a fresh clone regenerates every URDF/XML **without CoACD installed** — only re-freezing geometry needs it.
(LFS caveat: `git lfs pull` the real parts before regen, else the reuse step chokes on pointer stubs.)

Each object directory needs:
- `<name>.obj` — visual/collision mesh
- `metadata.json` — with fields: `inertial`, `initial_pos`, `initial_quat`, `texture`

```json
{
  "initial_pos": "1.0 0.0 0.3",
  "initial_quat": "1 0 0 0",
  "texture": "source/textures/Wood/Bamboo_Planks/Bamboo_Planks_BaseColor.png",
  "inertial": {
    "mass": 0.8,
    "com": [0.0, 0.0, 0.075],
    "inertia": {"ixx": 0.159524, "iyy": 0.148608, "izz": 0.098411,
                "ixy": 0.000017, "ixz": 0.000100, "iyz": 0.024594}
  }
}
```

### The `inertial` block

The **single mass/inertia authority**: it is written body-level into the URDF *and* every MJCF
variant, and geoms carry no mass at all. So `_cvx_hull` and `_cvx_dcmp` of one object are
dynamically identical, and mjlab's per-world variant merge sees one inertial representation
(`fullinertia`) on every object — it rejects a mix of fullinertia / diagonal / mesh-derived
across variants.

| key | required | default |
|---|---|---|
| `mass` | **yes** | — |
| `com` | no | mesh COM (trimesh), or the origin for a `simple_collider` |
| `inertia` | no | mesh tensor at homogeneous density; off-diagonals default to `0` when the key is given |

Override is **per field**: give `com` alone to shift the COM and keep the computed tensor; give
`{ixx, iyy, izz}` alone for a diagonal tensor. `[inrt]` in the run log tags each field
`<metadata>` or `<computed>`, so a regen shows at a glance which objects are hand-pinned.

**Convention** (identical in both formats): `com` [m] is in the **mesh frame** (before
`initial_pos`/`initial_quat`); the tensor is [kg·m²] **about the COM**, in **mesh axes** — so URDF
`rpy` is always `0 0 0` and MJCF needs no inertial quat. A principal-axis tensor goes in as a
full tensor, never as axes + a rotation. Named keys, never a 6-list: URDF's order
(`ixx ixy ixz iyy iyz izz`) and MJCF `fullinertia`'s (`ixx iyy izz ixy ixz iyz`) differ, and each
lives in exactly one formatter. A tensor that is not positive definite, or whose principal
moments break the triangle inequality, is rejected here rather than at MuJoCo compile time.

**Defaults** come from mesh geometry at homogeneous density (trimesh). Every mesh shipped here is
non-watertight, so the default is computed on the **convex hull** — an overestimate of the spread
for open shapes (chairs, tables). That is what the override is for.

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
