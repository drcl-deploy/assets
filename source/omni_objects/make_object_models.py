 #!/usr/bin/env python3
"""Auto-generate object model files (URDF + MuJoCo XMLs) from mesh + metadata.

Given an object directory containing:
  <name>.obj      -- visual/collision mesh
  metadata.json   -- {"inertial": {...}, "initial_pos": ..., "initial_quat": ..., "texture": ...}

The "inertial" block is the ONE mass/inertia authority (see resolve_inertial): body-level in
both formats, geoms carry no mass. `mass` is required; `com`/`inertia` override the
mesh-derived defaults field-by-field.

Generates (all inside the object directory):
  <name>.urdf              -- single-link URDF with auto-computed inertia
  <name>_cvx_hull.xml      -- MuJoCo includable body: single convex-hull collision
  <name>_cvx_dcmp.xml      -- MuJoCo includable body: CoACD decomposed collision
  collision/<name>_cvx_*.obj  -- convex decomposition parts

Usage:
    python make_object_models.py ../omomo_objects/smallbox
    python make_object_models.py ../omomo_objects/*/ --force
    python make_object_models.py ../custom_objects/tire --no-decompose
    python make_object_models.py --all                  # every object in OBJECT_GROUP_PATTERNS
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import trimesh

# ── Paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent       # .../source/omni_objects
ASSETS_DIR = SCRIPT_DIR.parent                     # .../source
WORKSPACE_ROOT = ASSETS_DIR.parent                 # .../assets


def _asset_abs(p: Path) -> str:
    """Absolute path for THIS machine. The generated URDF/XMLs bake absolute paths (training +
    sim2sim loaders need global paths and don't localize) — which is exactly why these files are
    git-IGNORED build products: each machine runs make_object_models.py once to (re)bake locally."""
    return str(p.resolve())

# ── Metadata ─────────────────────────────────────────────────────────────────

def load_metadata(obj_dir: Path) -> dict:
    meta_path = obj_dir / "metadata.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"Missing metadata.json in {obj_dir}")
    meta = json.loads(meta_path.read_text())
    if "mass" in meta:
        raise ValueError(
            f"metadata.json in {obj_dir} has a top-level 'mass' — it moved under "
            'the inertial block: {"inertial": {"mass": ...}}')
    if "mass" not in meta.get("inertial", {}):
        raise ValueError(f"metadata.json in {obj_dir} has no 'inertial.mass' field")
    return meta


def resolve_obj(path: Path) -> Path | None:
    """Accept an .obj file or an object dir holding <name>/<name>.obj.

    Returns None for primitive-geometry objects (no mesh file).
    """
    if path.is_file() and path.suffix.lower() == ".obj":
        return path
    if path.is_dir():
        cand = path / f"{path.name}.obj"
        if cand.is_file():
            return cand
    return None


# ── Inertia computation ─────────────────────────────────────────────────────
#
# One object -> ONE inertial, computed once and written verbatim into the URDF and every
# MJCF variant. Both formats carry it at BODY level (URDF <inertial>, MJCF <inertial>), geoms
# carry no mass — so hull and dcmp agree by construction and mjlab's per-world variant merge
# sees the same inertial representation on every object (entity/variants.py rejects a mix of
# fullinertia / diagonal / mesh-derived across variants).
#
# Convention, identical in both formats: `com` [m] is the COM in the MESH frame (before
# initial_pos/quat); the tensor is [kg m^2] about the COM in MESH AXES (not principal) — hence
# URDF rpy is always "0 0 0" and MJCF needs no inertial quat.

_INERTIA_KEYS = ("ixx", "iyy", "izz", "ixy", "ixz", "iyz")


def compute_inertia_primitive(mass: float, collider: dict) -> tuple[list[float], dict]:
    """Analytical (com, inertia) for primitive geometries (sphere, box, cylinder).

    The primitive geom sits at the body origin, so the COM is the origin.
    """
    com = [0.0, 0.0, 0.0]
    geom = collider["geometry"]
    if geom == "sphere":
        r = collider["radius"]
        I = 2.0 / 5.0 * mass * r ** 2
        return com, dict(ixx=I, iyy=I, izz=I, ixy=0.0, ixz=0.0, iyz=0.0)
    elif geom == "box":
        x, y, z = collider["x"], collider["y"], collider["z"]
        return com, dict(
            ixx=mass / 12.0 * (y**2 + z**2),
            iyy=mass / 12.0 * (x**2 + z**2),
            izz=mass / 12.0 * (x**2 + y**2),
            ixy=0.0, ixz=0.0, iyz=0.0)
    elif geom == "cylinder":
        r, h = collider["radius"], collider["height"]
        Iax = 0.5 * mass * r ** 2
        Itr = mass / 12.0 * (3 * r**2 + h**2)
        return com, dict(ixx=Itr, iyy=Itr, izz=Iax, ixy=0.0, ixz=0.0, iyz=0.0)
    else:
        raise ValueError(f"Unknown primitive geometry: {geom}")


def compute_inertia_mesh(obj_path: Path, mass: float) -> tuple[list[float], dict]:
    """Compute (com, inertia tensor about the com) assuming homogeneous density.

    Uses trimesh: sets density = mass / volume, reads center_mass + moment_inertia.
    Falls back to the convex hull if the mesh isn't watertight (true for every object
    shipped here — the metadata override exists for the cases where that is too crude).
    """
    mesh = trimesh.load(obj_path, force="mesh")
    if not mesh.is_watertight or mesh.volume <= 0:
        mesh = mesh.convex_hull
    vol = mesh.volume
    if vol <= 0:
        raise ValueError(f"Could not compute volume for {obj_path}")
    mesh.density = mass / vol
    I = mesh.moment_inertia  # 3x3 about CoM
    return ([float(c) for c in mesh.center_mass],
            dict(ixx=I[0, 0], iyy=I[1, 1], izz=I[2, 2],
                 ixy=I[0, 1], ixz=I[0, 2], iyz=I[1, 2]))


def _validate_inertia(name: str, inertia: dict) -> None:
    """Reject a tensor MuJoCo would refuse: non-positive-definite, or principal moments
    violating the triangle inequality (mjcf: A0+A1 >= A2, unless compiler balanceinertia)."""
    M = np.array([[inertia["ixx"], inertia["ixy"], inertia["ixz"]],
                  [inertia["ixy"], inertia["iyy"], inertia["iyz"]],
                  [inertia["ixz"], inertia["iyz"], inertia["izz"]]], dtype=np.float64)
    w = np.sort(np.linalg.eigvalsh(M))
    if w[0] <= 0:
        raise ValueError(f"{name}: inertia is not positive definite "
                         f"(principal moments {np.round(w, 9).tolist()})")
    if w[0] + w[1] < w[2] * (1 - 1e-9):
        raise ValueError(f"{name}: principal moments {np.round(w, 9).tolist()} violate the "
                         "triangle inequality — no rigid body has this tensor")


def resolve_inertial(name: str, metadata: dict, computed: tuple[list[float], dict]) -> dict:
    """Merge the metadata `inertial` block over the geometry-derived default, per field.

    metadata.json:
        "inertial": {
          "mass": 3.46,                 # required — the ONE mass authority
          "com": [0.0, 0.0, 0.075],     # optional -> mesh/primitive COM
          "inertia": {"ixx": .., "iyy": .., "izz": ..,   # optional -> computed tensor;
                      "ixy": .., "ixz": .., "iyz": ..}   # off-diagonals default to 0
        }

    Named keys, never a 6-list: the peculiar MJCF `fullinertia` order lives in exactly one
    place (`_mjcf_inertial`) and cannot be silently transposed against URDF's own order.
    """
    block = metadata["inertial"]
    com_c, I_c = computed
    com = [float(c) for c in block.get("com", com_c)]
    if len(com) != 3:
        raise ValueError(f"{name}: inertial.com must be 3 numbers, got {com}")
    over = block.get("inertia")
    if over is None:
        inertia = dict(I_c)
    else:
        unknown = set(over) - set(_INERTIA_KEYS)
        if unknown:
            raise ValueError(f"{name}: unknown inertial.inertia keys {sorted(unknown)} "
                             f"(expected a subset of {list(_INERTIA_KEYS)})")
        inertia = {k: float(over.get(k, 0.0)) for k in _INERTIA_KEYS}
    _validate_inertia(name, inertia)
    return dict(mass=float(block["mass"]), com=com, inertia=inertia,
                src=("metadata" if "com" in block else "computed",
                     "metadata" if over is not None else "computed"))


def _fmt(x: float) -> str:
    return f"{x:.6g}"


def _urdf_inertial(inr: dict) -> str:
    """URDF <inertial>: <origin> is the COM frame, rpy always 0 (tensor is in mesh axes)."""
    inertia = inr["inertia"]
    return (f'<mass value="{_fmt(inr["mass"])}"/>\n'
            f'      <origin xyz="{" ".join(_fmt(c) for c in inr["com"])}" rpy="0 0 0"/>\n'
            f'      <inertia ' + " ".join(f'{k}="{_fmt(inertia[k])}"' for k in
                                          ("ixx", "ixy", "ixz", "iyy", "iyz", "izz")) + "/>")


def _mjcf_inertial(inr: dict) -> str:
    """MJCF <inertial>. `fullinertia` order is M(1,1) M(2,2) M(3,3) M(1,2) M(1,3) M(2,3) —
    https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-inertial"""
    inertia = inr["inertia"]
    return (f'<inertial pos="{" ".join(_fmt(c) for c in inr["com"])}" '
            f'mass="{_fmt(inr["mass"])}" '
            f'fullinertia="{" ".join(_fmt(inertia[k]) for k in _INERTIA_KEYS)}"/>')


# ── URDF generation ─────────────────────────────────────────────────────────

URDF_TEMPLATE = """\
<?xml version="1.0"?>
<robot name="{name}">

  <link name="base_link">

    <inertial>
      {inertial}
    </inertial>

    <visual>
      <geometry>
        {geom_tag}
      </geometry>
    </visual>

    <collision>
      <geometry>
        {geom_tag}
      </geometry>
      <surface>
        <friction>
          <ode>
            <mu>{friction}</mu>
            <mu2>{friction}</mu2>
          </ode>
        </friction>
        <contact>
          <ode>
            <kp>1000000.0</kp>
            <kd>1.0</kd>
            <max_vel>100.0</max_vel>
            <min_depth>0.001</min_depth>
          </ode>
        </contact>
      </surface>
    </collision>

  </link>
</robot>
"""


def _urdf_geom_tag(name: str, collider: dict | None) -> str:
    """Return the URDF <geometry> inner tag for mesh or primitive."""
    if collider is None:
        return f'<mesh filename="{name}.obj"/>'
    geom = collider["geometry"]
    if geom == "sphere":
        return f'<sphere radius="{collider["radius"]}"/>'
    elif geom == "box":
        return f'<box size="{collider["x"]} {collider["y"]} {collider["z"]}"/>'
    elif geom == "cylinder":
        return f'<cylinder radius="{collider["radius"]}" length="{collider["height"]}"/>'
    raise ValueError(f"Unknown geometry: {geom}")


def write_urdf(obj_dir: Path, name: str, inertial: dict,
               friction: float, collider: dict | None = None) -> Path:
    geom_tag = _urdf_geom_tag(name, collider)
    out = obj_dir / f"{name}.urdf"
    out.write_text(URDF_TEMPLATE.format(name=name, friction=friction, geom_tag=geom_tag,
                                        inertial=_urdf_inertial(inertial)))
    return out


# ── MuJoCo XML: convex hull (single-geom body) ─────────────────────────────

CVX_HULL_TEMPLATE = """\
<mujoco model="{name}_cvx_hull">
  <asset>
    <mesh name="{name}" file="{mesh_file}"/>
    <texture name="{name}_texture" type="2d" file="{texture_file}"/>
    <material name="{name}_material" texture="{name}_texture" specular="0.25" shininess="0.6" reflectance="0.1"/>
  </asset>
  <worldbody>
    <body name="{name}" pos="{pos}" quat="{quat}">
      <freejoint/>
      {inertial}
      <geom type="mesh" mesh="{name}" friction="{friction} {friction} 0.0001" material="{name}_material"/>
    </body>
  </worldbody>
</mujoco>
"""


def write_cvx_hull_xml(obj_dir: Path, name: str, metadata: dict, inertial: dict,
                       friction: float) -> Path:
    mesh_file = _asset_abs(obj_dir / f"{name}.obj")
    texture_file = _asset_abs(WORKSPACE_ROOT / metadata["texture"])
    xml = CVX_HULL_TEMPLATE.format(
        name=name, mesh_file=mesh_file, texture_file=texture_file,
        inertial=_mjcf_inertial(inertial), friction=friction,
        pos=metadata["initial_pos"], quat=metadata["initial_quat"],
    )
    out = obj_dir / f"{name}_cvx_hull.xml"
    out.write_text(xml)
    return out


# ── MuJoCo XML: primitive geometry (sphere/box/cylinder) ─────────────────────

PRIMITIVE_XML_TEMPLATE = """\
<mujoco model="{name}_{variant}">
  <asset>
    <texture name="{name}_texture" type="2d" file="{texture_file}"/>
    <material name="{name}_material" texture="{name}_texture" specular="0.25" shininess="0.6" reflectance="0.1"/>
  </asset>
  <worldbody>
    <body name="{name}" pos="{pos}" quat="{quat}">
      <freejoint/>
      {inertial}
      <geom {geom_attrs} friction="{friction} {friction} 0.0001" material="{name}_material"/>
    </body>
  </worldbody>
</mujoco>
"""


def _mjcf_geom_attrs(collider: dict) -> str:
    """Return MuJoCo geom type + size attributes for a primitive."""
    geom = collider["geometry"]
    if geom == "sphere":
        return f'type="sphere" size="{collider["radius"]}"'
    elif geom == "box":
        hx = collider["x"] / 2
        hy = collider["y"] / 2
        hz = collider["z"] / 2
        return f'type="box" size="{hx} {hy} {hz}"'
    elif geom == "cylinder":
        return f'type="cylinder" size="{collider["radius"]} {collider["height"] / 2}"'
    raise ValueError(f"Unknown geometry: {geom}")


def write_primitive_xmls(obj_dir: Path, name: str, metadata: dict, inertial: dict,
                         collider: dict, friction: float) -> tuple[Path, Path]:
    """Write both _cvx_hull.xml and _cvx_dcmp.xml for a primitive (identical content)."""
    texture_file = _asset_abs(WORKSPACE_ROOT / metadata["texture"])
    geom_attrs = _mjcf_geom_attrs(collider)

    paths = []
    for variant in ("cvx_hull", "cvx_dcmp"):
        xml = PRIMITIVE_XML_TEMPLATE.format(
            name=name, variant=variant, geom_attrs=geom_attrs,
            texture_file=texture_file, inertial=_mjcf_inertial(inertial), friction=friction,
            pos=metadata["initial_pos"], quat=metadata["initial_quat"],
        )
        out = obj_dir / f"{name}_{variant}.xml"
        out.write_text(xml)
        paths.append(out)
    return paths[0], paths[1]


# ── MuJoCo XML: convex decomposition (multi-geom body) ─────────────────────

CVX_DCMP_TEMPLATE = """\
<mujoco model="{name}_cvx_dcmp">
  <asset>
    <mesh name="{name}_visual" file="{mesh_file}"/>
{part_assets}
    <texture name="{name}_texture" type="2d" file="{texture_file}"/>
    <material name="{name}_material" texture="{name}_texture" specular="0.25" shininess="0.6" reflectance="0.1"/>
  </asset>
  <worldbody>
    <body name="{name}" pos="{pos}" quat="{quat}">
      <freejoint/>
      {inertial}
      <geom name="{name}_visual" type="mesh" mesh="{name}_visual" contype="0" conaffinity="0" material="{name}_material"/>
{part_geoms}
    </body>
  </worldbody>
</mujoco>
"""


def decompose_mesh(obj_path: Path, threshold: float, max_hulls: int,
                   preprocess_resolution: int, seed: int) -> list[trimesh.Trimesh]:
    import coacd
    mesh = trimesh.load(obj_path, force="mesh")
    cmesh = coacd.Mesh(np.asarray(mesh.vertices, np.float64),
                       np.asarray(mesh.faces, np.int32))
    parts = coacd.run_coacd(
        cmesh, threshold=threshold, max_convex_hull=max_hulls,
        preprocess_mode="auto", preprocess_resolution=preprocess_resolution,
        merge=True, seed=seed,
    )
    return [trimesh.Trimesh(vertices=v, faces=f, process=False) for v, f in parts]


def write_cvx_dcmp_xml(obj_dir: Path, name: str, metadata: dict, inertial: dict,
                       parts: list[trimesh.Trimesh] | None, friction: float,
                       subdir: str = "convex_decomp_meshes") -> Path:
    """Emit the decomposed-collision XML. `parts` = fresh CoACD meshes → (re)export them;
    `parts is None` → REUSE the committed part .objs on disk (no CoACD needed). Part meshes are
    tracked geometry; only this XML (with abs paths) is a git-ignored, per-machine build product.

    Part geoms carry NO mass: the body-level <inertial> is the single mass authority, so the
    hull and dcmp variants of an object are dynamically identical (MuJoCo ignores geom mass
    when a body has an explicit inertial)."""
    coll_dir = obj_dir / subdir

    if parts is None:  # reuse committed parts — coacd-free regen
        part_paths = sorted(coll_dir.glob(f"{name}_cvx_*.obj"))
    else:              # fresh decomposition — (re)export the part meshes
        coll_dir.mkdir(exist_ok=True)
        for old in coll_dir.glob(f"{name}_cvx_*.obj"):
            old.unlink()
        part_paths = [coll_dir / f"{name}_cvx_{i:03d}.obj" for i in range(len(parts))]
        for part, pp in zip(parts, part_paths):
            part.export(pp)

    part_assets, part_geoms = [], []
    for i, part_path in enumerate(part_paths):
        mname = f"{name}_cvx_{i:03d}"
        part_assets.append(
            f'    <mesh name="{mname}" file="{_asset_abs(part_path)}"/>')
        part_geoms.append(
            f'      <geom type="mesh" mesh="{mname}" '
            f'friction="{friction} {friction} 0.0001" group="3"/>')

    mesh_file = _asset_abs(obj_dir / f"{name}.obj")
    texture_file = _asset_abs(WORKSPACE_ROOT / metadata["texture"])

    xml = CVX_DCMP_TEMPLATE.format(
        name=name, mesh_file=mesh_file, texture_file=texture_file,
        inertial=_mjcf_inertial(inertial),
        part_assets="\n".join(part_assets), part_geoms="\n".join(part_geoms),
        pos=metadata["initial_pos"], quat=metadata["initial_quat"],
    )
    out = obj_dir / f"{name}_cvx_dcmp.xml"
    out.write_text(xml)
    return out


# ── Object discovery (shared with scene generator) ──────────────────────────

from object_groups import OBJECT_GROUP_PATTERNS


def _has_object_source(obj_dir: Path) -> bool:
    """True if dir has a .obj mesh or a metadata with simple_collider."""
    name = obj_dir.name
    if (obj_dir / f"{name}.obj").is_file():
        return True
    meta_path = obj_dir / "metadata.json"
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text())
        if "simple_collider" in meta:
            return True
    return False


def discover_objects(filter_name: str | None = None) -> list[tuple[str, Path]]:
    """Returns list of (name, object_dir) for objects with mesh or primitive collider."""
    objects: list[tuple[str, Path]] = []
    seen: set[str] = set()

    for pattern in OBJECT_GROUP_PATTERNS:
        if pattern.endswith(".urdf"):
            obj_dir = (ASSETS_DIR / pattern).parent
            name = obj_dir.name
            if name not in seen and _has_object_source(obj_dir):
                seen.add(name)
                objects.append((name, obj_dir))
            continue

        for match in sorted(ASSETS_DIR.glob(pattern)):
            if not match.is_dir() or match.name.startswith("__"):
                continue
            name = match.name
            if name not in seen and _has_object_source(match):
                seen.add(name)
                objects.append((name, match))

    if filter_name:
        objects = [(n, d) for n, d in objects if n == filter_name]
    return objects


# ── Process one object ───────────────────────────────────────────────────────

def _print_inertial(inr: dict, source: str) -> None:
    """One line per object showing which fields are hand-pinned vs geometry-derived."""
    com_src, inertia_src = inr["src"]
    inertia = inr["inertia"]
    print(f"  [inrt] mass={_fmt(inr['mass'])}  "
          f"com=({' '.join(_fmt(c) for c in inr['com'])}) <{com_src}>  "
          f"inertia=({' '.join(_fmt(inertia[k]) for k in ('ixx', 'iyy', 'izz'))}) <{inertia_src}>  [{source}]")


def process(obj_dir: Path, *, force: bool, do_decompose: bool,
            threshold: float, max_hulls: int, preprocess_resolution: int,
            seed: int, quiet: bool):
    name = obj_dir.name
    metadata = load_metadata(obj_dir)
    mass = metadata["inertial"]["mass"]
    friction = metadata.get("friction", 0.6)
    collider = metadata.get("simple_collider")
    obj_path = resolve_obj(obj_dir)

    if collider is not None:
        # ── Primitive geometry path ──
        inertial = resolve_inertial(name, metadata,
                                    compute_inertia_primitive(mass, collider))
        _print_inertial(inertial, collider["geometry"])

        urdf_path = write_urdf(obj_dir, name, inertial, friction, collider)
        print(f"  [urdf] {urdf_path.name}")

        hull_path, dcmp_path = write_primitive_xmls(obj_dir, name, metadata, inertial,
                                                    collider, friction)
        print(f"  [hull] {hull_path.name}")
        print(f"  [dcmp] {dcmp_path.name}  (primitive — no decomposition needed)")
        return

    # ── Mesh geometry path ──
    if obj_path is None:
        raise FileNotFoundError(f"No .obj mesh and no simple_collider in {obj_dir}")

    inertial = resolve_inertial(name, metadata, compute_inertia_mesh(obj_path, mass))
    _print_inertial(inertial, "mesh")

    urdf_path = write_urdf(obj_dir, name, inertial, friction)
    print(f"  [urdf] {urdf_path.name}")

    hull_path = write_cvx_hull_xml(obj_dir, name, metadata, inertial, friction)
    print(f"  [hull] {hull_path.name}")

    if do_decompose:
        # Part meshes are tracked geometry; the XML is a per-machine build product. On a fresh
        # clone (or coacd-less box) reuse the committed parts to re-emit the XML with local abs
        # paths — no coacd. Only a first-time decomposition or --force actually runs coacd.
        existing_parts = sorted((obj_dir / "convex_decomp_meshes").glob(f"{name}_cvx_*.obj"))
        if existing_parts and not force:
            out = write_cvx_dcmp_xml(obj_dir, name, metadata, inertial, None, friction)
            print(f"  [dcmp] {out.name}  ({len(existing_parts)} parts reused — no coacd)")
        else:
            try:
                import coacd  # noqa: F811
            except ImportError:
                print("  [skip] coacd not installed (and no committed parts) — pip install coacd")
                return
            if quiet:
                coacd.set_log_level("error")
            parts = decompose_mesh(obj_path, threshold, max_hulls,
                                   preprocess_resolution, seed)
            out = write_cvx_dcmp_xml(obj_dir, name, metadata, inertial, parts, friction)
            print(f"  [dcmp] {out.name}  ({len(parts)} convex parts)")
            if len(parts) > 64:
                print(f"         ! {len(parts)} parts is a lot — raise --threshold")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", type=Path,
                    help="object dir(s) or .obj file(s)")
    ap.add_argument("--all", action="store_true",
                    help="process every object in OBJECT_GROUP_PATTERNS")
    ap.add_argument("--object", default=None,
                    help="process a single object by name (with --all)")
    ap.add_argument("--force", action="store_true",
                    help="regenerate even if outputs exist")
    ap.add_argument("--no-decompose", action="store_true",
                    help="skip CoACD decomposition (only URDF + hull)")
    ap.add_argument("--threshold", type=float, default=0.05,
                    help="CoACD concavity threshold (0.02..0.1)")
    ap.add_argument("--max-hulls", type=int, default=32,
                    help="cap on convex parts (default 32, -1 = no cap)")
    ap.add_argument("--preprocess-resolution", type=int, default=50,
                    help="voxel resolution for watertight pre-remesh")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--quiet", action="store_true",
                    help="silence CoACD logging")
    args = ap.parse_args()

    if args.all:
        targets = [(name, obj_dir) for name, obj_dir
                    in discover_objects(args.object)]
        if not targets:
            print("No mesh objects found.")
            return
        for name, obj_dir in targets:
            print(f"\n[{name}]")
            try:
                process(obj_dir, force=args.force,
                        do_decompose=not args.no_decompose,
                        threshold=args.threshold, max_hulls=args.max_hulls,
                        preprocess_resolution=args.preprocess_resolution,
                        seed=args.seed, quiet=args.quiet)
            except Exception as e:
                print(f"  [fail] {e}")
        print(f"\nDone. {len(targets)} object(s) processed.")
    elif args.paths:
        for p in args.paths:
            obj_dir = p if p.is_dir() else p.parent
            print(f"\n[{obj_dir.name}]")
            try:
                process(obj_dir, force=args.force,
                        do_decompose=not args.no_decompose,
                        threshold=args.threshold, max_hulls=args.max_hulls,
                        preprocess_resolution=args.preprocess_resolution,
                        seed=args.seed, quiet=args.quiet)
            except Exception as e:
                print(f"  [fail] {e}")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
