#!/usr/bin/env python3
"""Generate MuJoCo scene XMLs that compose a Unitree robot with a single dynamic object.

Each generated scene uses absolute paths so it can be loaded from anywhere — no
asset copying required.

Usage:
    # Generate scenes for all objects with the default robot (g1 / scene_29dof):
    python generate_mujoco_scenes.py

    # Specify robot and scene:
    python generate_mujoco_scenes.py --robot g1 --robot-scene scene_29dof.xml

    # Generate for a single object:
    python generate_mujoco_scenes.py --object trashcan

    # Custom output directory:
    python generate_mujoco_scenes.py --out-dir /tmp/scenes

Generated scenes can be used directly in unitree_mujoco's config.yaml:
    robot_scene: "/HDD/drcl_projects/assets/source/multi_objects/scenes/scene_g1_29dof_trashcan.xml"
"""

import argparse
import os
import glob
import xml.etree.ElementTree as ET
from pathlib import Path


# ── Paths ────────────────────────────────────────────────────────────────────

ASSETS_DIR = Path(os.environ.get("SIM_ASSETS_PATH", "/HDD/drcl_projects/assets/source"))
UNITREE_ROBOTS_DIR = Path("/home/lkrajan/ros2/unitree_ros2/unitree_mujoco/unitree_robots")
DEFAULT_OUT_DIR = ASSETS_DIR / "multi_objects" / "scenes"


# ── URDF parsing ─────────────────────────────────────────────────────────────

def parse_urdf(urdf_path: Path) -> dict:
    """Extract mass and geometry from a single-link URDF.

    Inertia is NOT extracted — MuJoCo auto-computes it from the geom shape
    and mass, which gives correct CoM position and principal axes.
    """
    tree = ET.parse(urdf_path)
    root = tree.getroot()
    link = root.find("link")
    inertial = link.find("inertial")

    mass = float(inertial.find("mass").get("value"))

    # Geometry — check collision first, fall back to visual
    geom_el = None
    for tag in ("collision", "visual"):
        container = link.find(tag)
        if container is not None:
            geom_el = container.find("geometry")
            if geom_el is not None:
                break

    geom_info = _parse_geometry(geom_el)

    # Friction from URDF (if present)
    friction = 0.6  # default
    collision = link.find("collision")
    if collision is not None:
        surface = collision.find("surface")
        if surface is not None:
            fric = surface.find("friction")
            if fric is not None:
                ode = fric.find("ode")
                if ode is not None:
                    mu = ode.find("mu")
                    if mu is not None:
                        friction = float(mu.text)

    return {
        "mass": mass,
        "geom": geom_info,
        "friction": friction,
    }


def _parse_geometry(geom_el) -> dict:
    """Parse URDF geometry element into MuJoCo-friendly dict."""
    child = geom_el[0]  # first child is the geometry type
    tag = child.tag

    if tag == "mesh":
        filename = child.get("filename")
        return {"type": "mesh", "filename": filename}
    elif tag == "sphere":
        return {"type": "sphere", "size": child.get("radius")}
    elif tag == "box":
        size = child.get("size")  # URDF: full extents "x y z"
        halfs = " ".join(str(float(v) / 2) for v in size.split())
        return {"type": "box", "size": halfs}
    elif tag == "cylinder":
        r = child.get("radius")
        h = float(child.get("length")) / 2
        return {"type": "cylinder", "size": f"{r} {h}"}
    else:
        raise ValueError(f"Unsupported geometry type: {tag}")


# ── Scene generation ─────────────────────────────────────────────────────────

SCENE_TEMPLATE = """\
<mujoco model="{model_name}">
  <include file="{robot_xml_abs}"/>

  <statistic center="0 0 0.5" extent="2.0"/>

  <visual>
    <headlight diffuse="0.6 0.6 0.6" ambient="0.3 0.3 0.3" specular="0 0 0"/>
    <rgba haze="0.15 0.25 0.35 1"/>
    <global azimuth="-130" elevation="-20"/>
  </visual>

  <asset>
    <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="3072"/>
    <texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3"
      markrgb="0.8 0.8 0.8" width="300" height="300"/>
    <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5" reflectance="0.2"/>
{object_assets}
  </asset>

  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>

    <body name="{object_name}" pos="{object_pos}">
      <freejoint/>
{object_geom}
    </body>
  </worldbody>
</mujoco>
"""


def generate_scene(
    robot: str,
    robot_scene_name: str,
    object_name: str,
    urdf_data: dict,
    object_dir: Path,
    object_pos: str = "1.0 0.0 0.3",
) -> str:
    """Generate a complete scene XML string."""
    # Resolve the robot XML that the original scene includes
    # Parse the original scene to find the <include file="..."/>
    original_scene = UNITREE_ROBOTS_DIR / robot / robot_scene_name
    orig_tree = ET.parse(original_scene)
    include_el = orig_tree.getroot().find("include")
    robot_xml_name = include_el.get("file")
    robot_xml_abs = str(UNITREE_ROBOTS_DIR / robot / robot_xml_name)

    # Derive scene variant name from robot_scene (e.g. "scene_29dof.xml" -> "29dof")
    scene_variant = robot_scene_name.replace("scene_", "").replace("scene", "").replace(".xml", "")
    if scene_variant:
        model_name = f"{robot}_{scene_variant} + {object_name}"
    else:
        model_name = f"{robot} + {object_name}"

    # Build object geometry and assets
    geom = urdf_data["geom"]
    object_assets = ""
    geom_line = ""
    mass = urdf_data["mass"]
    friction_attr = f'friction="{urdf_data["friction"]} {urdf_data["friction"]} 0.0001"'
    mass_attr = f'mass="{mass}"'

    if geom["type"] == "mesh":
        mesh_abs_path = str(object_dir / geom["filename"])
        object_assets = f'    <mesh name="{object_name}" file="{mesh_abs_path}"/>'
        geom_line = f'      <geom type="mesh" mesh="{object_name}" {mass_attr} {friction_attr}/>'
    elif geom["type"] == "sphere":
        geom_line = f'      <geom type="sphere" size="{geom["size"]}" {mass_attr} {friction_attr}/>'
    elif geom["type"] == "box":
        geom_line = f'      <geom type="box" size="{geom["size"]}" {mass_attr} {friction_attr}/>'
    elif geom["type"] == "cylinder":
        geom_line = f'      <geom type="cylinder" size="{geom["size"]}" {mass_attr} {friction_attr}/>'

    return SCENE_TEMPLATE.format(
        model_name=model_name,
        robot_xml_abs=robot_xml_abs,
        object_assets=object_assets,
        object_name=object_name,
        object_pos=object_pos,
        object_geom=geom_line,
    )


# ── Object discovery ─────────────────────────────────────────────────────────

def discover_objects(filter_name: str | None = None) -> list[tuple[str, Path, Path]]:
    """Discover available objects. Returns list of (name, urdf_path, object_dir)."""
    objects = []

    # Basketball (special case — sphere, no mesh)
    bb_urdf = ASSETS_DIR / "basketball" / "basketball.urdf"
    if bb_urdf.exists():
        objects.append(("basketball", bb_urdf, ASSETS_DIR / "basketball"))

    # Omomo objects
    omomo_dir = ASSETS_DIR / "omomo_objects"
    if omomo_dir.exists():
        for obj_dir in sorted(omomo_dir.iterdir()):
            if not obj_dir.is_dir() or obj_dir.name.startswith("__"):
                continue
            urdf = obj_dir / f"{obj_dir.name}.urdf"
            if urdf.exists():
                objects.append((obj_dir.name, urdf, obj_dir))

    if filter_name:
        objects = [(n, u, d) for n, u, d in objects if n == filter_name]

    return objects


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--robot", default="g1", help="Robot name (default: g1)")
    parser.add_argument("--robot-scene", default="scene_29dof.xml", help="Base robot scene file (default: scene_29dof.xml)")
    parser.add_argument("--object", default=None, help="Generate for a single object only")
    parser.add_argument("--object-pos", default="1.0 0.0 0.3", help="Object spawn position 'x y z' (default: '1.0 0.0 0.3')")
    parser.add_argument("--out-dir", default=None, help=f"Output directory (default: {DEFAULT_OUT_DIR})")
    args = parser.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # Create a symlink for the robot's meshdir so MuJoCo can resolve it
    # from the scene file's directory. MuJoCo resolves meshdir relative to
    # the top-level file, even inside <include>'d files.
    robot_xml_path = UNITREE_ROBOTS_DIR / args.robot / args.robot_scene
    orig_tree = ET.parse(robot_xml_path)
    include_el = orig_tree.getroot().find("include")
    robot_xml_name = include_el.get("file")
    robot_tree = ET.parse(UNITREE_ROBOTS_DIR / args.robot / robot_xml_name)
    robot_compiler = robot_tree.getroot().find("compiler")
    meshdir_rel = robot_compiler.get("meshdir", ".") if robot_compiler is not None else "."
    robot_meshdir_abs = (UNITREE_ROBOTS_DIR / args.robot / meshdir_rel).resolve()

    symlink_path = out_dir / meshdir_rel
    if symlink_path.is_symlink():
        if symlink_path.resolve() != robot_meshdir_abs:
            symlink_path.unlink()
            symlink_path.symlink_to(robot_meshdir_abs)
            print(f"  Updated symlink: {symlink_path} -> {robot_meshdir_abs}")
    elif not symlink_path.exists():
        symlink_path.symlink_to(robot_meshdir_abs)
        print(f"  Created symlink: {symlink_path} -> {robot_meshdir_abs}")

    objects = discover_objects(args.object)
    if not objects:
        print(f"No objects found{f' matching {args.object!r}' if args.object else ''}.")
        return

    scene_variant = args.robot_scene.replace("scene_", "").replace("scene", "").replace(".xml", "")

    for name, urdf_path, obj_dir in objects:
        urdf_data = parse_urdf(urdf_path)
        scene_xml = generate_scene(
            robot=args.robot,
            robot_scene_name=args.robot_scene,
            object_name=name,
            urdf_data=urdf_data,
            object_dir=obj_dir,
            object_pos=args.object_pos,
        )

        if scene_variant:
            out_name = f"scene_{args.robot}_{scene_variant}_{name}.xml"
        else:
            out_name = f"scene_{args.robot}_{name}.xml"
        out_path = out_dir / out_name
        out_path.write_text(scene_xml)
        print(f"  Generated: {out_path}")

    print(f"\nDone. {len(objects)} scene(s) in {out_dir}/")
    print(f"\nTo use, set in config.yaml:")
    print(f'  robot_scene: "{out_dir}/scene_{args.robot}_{scene_variant}_{objects[0][0]}.xml"')


if __name__ == "__main__":
    main()
