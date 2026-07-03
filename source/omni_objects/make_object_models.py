 #!/usr/bin/env python3
"""Auto-generate object model files (URDF + MuJoCo XMLs) from mesh + metadata.

Given an object directory containing:
  <name>.obj      -- visual/collision mesh
  metadata.json   -- {"mass": ..., "initial_pos": ..., "initial_quat": ..., "texture": ...}

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
    if "mass" not in meta:
        raise ValueError(f"metadata.json in {obj_dir} has no 'mass' field")
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

def compute_inertia_primitive(mass: float, collider: dict) -> dict:
    """Analytical inertia for primitive geometries (sphere, box, cylinder)."""
    geom = collider["geometry"]
    if geom == "sphere":
        r = collider["radius"]
        I = 2.0 / 5.0 * mass * r ** 2
        return dict(ixx=I, ixy=0.0, ixz=0.0, iyy=I, iyz=0.0, izz=I)
    elif geom == "box":
        x, y, z = collider["x"], collider["y"], collider["z"]
        return dict(
            ixx=mass / 12.0 * (y**2 + z**2), ixy=0.0, ixz=0.0,
            iyy=mass / 12.0 * (x**2 + z**2), iyz=0.0,
            izz=mass / 12.0 * (x**2 + y**2))
    elif geom == "cylinder":
        r, h = collider["radius"], collider["height"]
        Iax = 0.5 * mass * r ** 2
        Itr = mass / 12.0 * (3 * r**2 + h**2)
        return dict(ixx=Itr, ixy=0.0, ixz=0.0, iyy=Itr, iyz=0.0, izz=Iax)
    else:
        raise ValueError(f"Unknown primitive geometry: {geom}")


def compute_inertia_mesh(obj_path: Path, mass: float) -> dict:
    """Compute inertia tensor assuming homogeneous density.

    Uses trimesh: sets density = mass / volume, reads moment_inertia.
    Falls back to convex hull volume if the mesh isn't watertight.
    """
    mesh = trimesh.load(obj_path, force="mesh")
    if not mesh.is_watertight or mesh.volume <= 0:
        mesh = mesh.convex_hull
    vol = mesh.volume
    if vol <= 0:
        raise ValueError(f"Could not compute volume for {obj_path}")
    mesh.density = mass / vol
    I = mesh.moment_inertia  # 3x3 about CoM
    return dict(ixx=I[0, 0], ixy=I[0, 1], ixz=I[0, 2],
                iyy=I[1, 1], iyz=I[1, 2], izz=I[2, 2])


# ── URDF generation ─────────────────────────────────────────────────────────

URDF_TEMPLATE = """\
<?xml version="1.0"?>
<robot name="{name}">

  <link name="base_link">

    <inertial>
      <mass value="{mass:.5f}"/>
      <inertia ixx="{ixx:.6f}" ixy="{ixy:.6f}" ixz="{ixz:.6f}" iyy="{iyy:.6f}" iyz="{iyz:.6f}" izz="{izz:.6f}"/>
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


def write_urdf(obj_dir: Path, name: str, mass: float, inertia: dict,
               friction: float, collider: dict | None = None) -> Path:
    geom_tag = _urdf_geom_tag(name, collider)
    out = obj_dir / f"{name}.urdf"
    out.write_text(URDF_TEMPLATE.format(name=name, mass=mass, friction=friction,
                                        geom_tag=geom_tag, **inertia))
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
      <geom type="mesh" mesh="{name}" mass="{mass}" friction="{friction} {friction} 0.0001" material="{name}_material"/>
    </body>
  </worldbody>
</mujoco>
"""


def write_cvx_hull_xml(obj_dir: Path, name: str, metadata: dict,
                       friction: float) -> Path:
    mesh_file = _asset_abs(obj_dir / f"{name}.obj")
    texture_file = _asset_abs(WORKSPACE_ROOT / metadata["texture"])
    xml = CVX_HULL_TEMPLATE.format(
        name=name, mesh_file=mesh_file, texture_file=texture_file,
        mass=metadata["mass"], friction=friction,
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
      <geom {geom_attrs} mass="{mass}" friction="{friction} {friction} 0.0001" material="{name}_material"/>
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


def write_primitive_xmls(obj_dir: Path, name: str, metadata: dict,
                         collider: dict, friction: float) -> tuple[Path, Path]:
    """Write both _cvx_hull.xml and _cvx_dcmp.xml for a primitive (identical content)."""
    texture_file = _asset_abs(WORKSPACE_ROOT / metadata["texture"])
    geom_attrs = _mjcf_geom_attrs(collider)

    paths = []
    for variant in ("cvx_hull", "cvx_dcmp"):
        xml = PRIMITIVE_XML_TEMPLATE.format(
            name=name, variant=variant, geom_attrs=geom_attrs,
            texture_file=texture_file, mass=metadata["mass"], friction=friction,
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


def write_cvx_dcmp_xml(obj_dir: Path, name: str, metadata: dict,
                       parts: list[trimesh.Trimesh] | None, friction: float,
                       subdir: str = "convex_decomp_meshes") -> Path:
    """Emit the decomposed-collision XML. `parts` = fresh CoACD meshes → (re)export them;
    `parts is None` → REUSE the committed part .objs on disk (no CoACD needed). Part meshes are
    tracked geometry; only this XML (with abs paths) is a git-ignored, per-machine build product."""
    coll_dir = obj_dir / subdir

    if parts is None:  # reuse committed parts — coacd-free regen
        part_paths = sorted(coll_dir.glob(f"{name}_cvx_*.obj"))
        meshes = [trimesh.load(p, force="mesh") for p in part_paths]
    else:              # fresh decomposition — (re)export the part meshes
        coll_dir.mkdir(exist_ok=True)
        for old in coll_dir.glob(f"{name}_cvx_*.obj"):
            old.unlink()
        part_paths = [coll_dir / f"{name}_cvx_{i:03d}.obj" for i in range(len(parts))]
        for part, pp in zip(parts, part_paths):
            part.export(pp)
        meshes = parts

    total_mass = metadata["mass"]
    vols = np.array([max(m.volume, 1e-9) for m in meshes], dtype=np.float64)
    mass_frac = vols / vols.sum()

    part_assets, part_geoms = [], []
    for i, (part_path, m_vol) in enumerate(zip(part_paths, mass_frac)):
        mname = f"{name}_cvx_{i:03d}"
        part_assets.append(
            f'    <mesh name="{mname}" file="{_asset_abs(part_path)}"/>')
        m = total_mass * m_vol
        part_geoms.append(
            f'      <geom type="mesh" mesh="{mname}" mass="{m:.6g}" '
            f'friction="{friction} {friction} 0.0001" group="3"/>')

    mesh_file = _asset_abs(obj_dir / f"{name}.obj")
    texture_file = _asset_abs(WORKSPACE_ROOT / metadata["texture"])

    xml = CVX_DCMP_TEMPLATE.format(
        name=name, mesh_file=mesh_file, texture_file=texture_file,
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

def process(obj_dir: Path, *, force: bool, do_decompose: bool,
            threshold: float, max_hulls: int, preprocess_resolution: int,
            seed: int, quiet: bool):
    name = obj_dir.name
    metadata = load_metadata(obj_dir)
    mass = metadata["mass"]
    friction = metadata.get("friction", 0.6)
    collider = metadata.get("simple_collider")
    obj_path = resolve_obj(obj_dir)

    if collider is not None:
        # ── Primitive geometry path ──
        inertia = compute_inertia_primitive(mass, collider)
        urdf_path = write_urdf(obj_dir, name, mass, inertia, friction, collider)
        print(f"  [urdf] {urdf_path.name}  (mass={mass}, {collider['geometry']})")

        hull_path, dcmp_path = write_primitive_xmls(obj_dir, name, metadata,
                                                     collider, friction)
        print(f"  [hull] {hull_path.name}")
        print(f"  [dcmp] {dcmp_path.name}  (primitive — no decomposition needed)")
        return

    # ── Mesh geometry path ──
    if obj_path is None:
        raise FileNotFoundError(f"No .obj mesh and no simple_collider in {obj_dir}")

    inertia = compute_inertia_mesh(obj_path, mass)
    urdf_path = write_urdf(obj_dir, name, mass, inertia, friction)
    print(f"  [urdf] {urdf_path.name}  (mass={mass}, "
          f"Ixx={inertia['ixx']:.6f} Iyy={inertia['iyy']:.6f} Izz={inertia['izz']:.6f})")

    hull_path = write_cvx_hull_xml(obj_dir, name, metadata, friction)
    print(f"  [hull] {hull_path.name}")

    if do_decompose:
        # Part meshes are tracked geometry; the XML is a per-machine build product. On a fresh
        # clone (or coacd-less box) reuse the committed parts to re-emit the XML with local abs
        # paths — no coacd. Only a first-time decomposition or --force actually runs coacd.
        existing_parts = sorted((obj_dir / "convex_decomp_meshes").glob(f"{name}_cvx_*.obj"))
        if existing_parts and not force:
            out = write_cvx_dcmp_xml(obj_dir, name, metadata, None, friction)
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
            out = write_cvx_dcmp_xml(obj_dir, name, metadata, parts, friction)
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
