#!/usr/bin/env python3
"""Generate UOLM scene XMLs (robot + dynamic object). See readme.md for details."""

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


# ── Paths (auto-detected from script location) ──────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent     # .../source/multi_objects
ASSETS_DIR = SCRIPT_DIR.parent                   # .../source
WORKSPACE_ROOT = ASSETS_DIR.parent               # .../assets
DEFAULT_OUT_DIR = SCRIPT_DIR / "scenes"


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_metadata(object_dir: Path) -> dict:
    meta_path = object_dir / "metadata.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"Missing metadata.json at {object_dir}")
    return json.loads(meta_path.read_text())


def parse_urdf(urdf_path: Path) -> dict:
    """Extract mass, geometry, and friction from a single-link URDF.

    Inertia is NOT extracted -- MuJoCo auto-computes it from geom shape + mass.
    """
    tree = ET.parse(urdf_path)
    link = tree.getroot().find("link")
    mass = float(link.find("inertial").find("mass").get("value"))

    # Geometry -- prefer collision, fall back to visual
    geom_el = None
    for tag in ("collision", "visual"):
        container = link.find(tag)
        if container is not None:
            geom_el = container.find("geometry")
            if geom_el is not None:
                break

    # Friction
    friction = 0.6
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

    return {"mass": mass, "geom": _parse_geometry(geom_el), "friction": friction}


def _parse_geometry(geom_el) -> dict:
    child = geom_el[0]
    tag = child.tag
    if tag == "mesh":
        return {"type": "mesh", "filename": child.get("filename")}
    elif tag == "sphere":
        return {"type": "sphere", "size": child.get("radius")}
    elif tag == "box":
        halfs = " ".join(str(float(v) / 2) for v in child.get("size").split())
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
        <headlight diffuse="0.6 0.6 0.6" ambient="0.6 0.6 0.6" specular="0.1 0.1 0.1"/>
        <rgba haze="0.85 0.87 0.9 1"/>
    <global azimuth="-130" elevation="-20"/>
        <map force="0.1" zfar="30"/>
        <quality shadowsize="4096"/>
  </visual>

  <asset>
        <texture type="skybox" builtin="flat" rgb1="0.8 0.85 0.9" rgb2="0.8 0.85 0.9" width="512" height="512"/>
        <texture type="2d" name="groundplane" builtin="checker" mark="edge"
            rgb1="0.05 0.05 0.05" rgb2="0.05 0.05 0.05"
            markrgb="1.0 1.0 1.0"
            width="512" height="512"/>
        <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="3 3" reflectance="0"/>

        <texture name="object_texture" type="2d" file="{object_texture_abs}"/>
        <material name="object_material" texture="object_texture" specular="0.25" shininess="0.6" reflectance="0.1"/>
{object_assets}
  </asset>

  <worldbody>
        <light pos="2 2 4" dir="-0.5 -0.5 -1" directional="true" diffuse="0.6 0.6 0.6" specular="0.2 0.2 0.2"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>

    <body name="{object_name}" pos="{object_pos}" quat="{object_quat}">
      <freejoint/>
{object_geom}
    </body>
  </worldbody>
</mujoco>
"""


def generate_scene(robot_xml_abs: str, object_name: str,
                   urdf_data: dict, object_dir: Path, metadata: dict) -> str:
    model_name = f"{Path(robot_xml_abs).stem} + {object_name}"

    geom = urdf_data["geom"]
    mass_attr = f'mass="{urdf_data["mass"]}"'
    friction_attr = f'friction="{urdf_data["friction"]} {urdf_data["friction"]} 0.0001"'
    material_attr = 'material="object_material"'
    object_assets = ""
    geom_line = ""

    if geom["type"] == "mesh":
        mesh_abs = str((object_dir / geom["filename"]).resolve())
        object_assets = f'    <mesh name="{object_name}" file="{mesh_abs}"/>'
        geom_line = f'      <geom type="mesh" mesh="{object_name}" {mass_attr} {friction_attr} {material_attr}/>'
    else:
        geom_line = f'      <geom type="{geom["type"]}" size="{geom["size"]}" {mass_attr} {friction_attr} {material_attr}/>'

    texture_abs = str((WORKSPACE_ROOT / metadata["texture"]).resolve())

    return SCENE_TEMPLATE.format(
        model_name=model_name,
        robot_xml_abs=robot_xml_abs,
        object_assets=object_assets,
        object_name=object_name,
        object_pos=metadata["initial_pos"],
        object_quat=metadata["initial_quat"],
        object_texture_abs=texture_abs,
        object_geom=geom_line,
    )


# ── Object discovery ─────────────────────────────────────────────────────────

def discover_objects(filter_name: str | None = None) -> list[tuple[str, Path, Path]]:
    """Returns list of (name, urdf_path, object_dir)."""
    objects = []

    bb_urdf = ASSETS_DIR / "basketball" / "basketball.urdf"
    if bb_urdf.exists():
        objects.append(("basketball", bb_urdf, ASSETS_DIR / "basketball"))

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
    parser.add_argument("--robot-xml", default=None,
                        help="Absolute path to robot MuJoCo XML (e.g. .../unitree_robots/g1/g1_29dof.xml)")
    parser.add_argument("--object", default=None, help="Generate for a single object only")
    parser.add_argument("--out-dir", default=None, help=f"Output directory (default: {DEFAULT_OUT_DIR})")
    args = parser.parse_args()

    robot_xml = args.robot_xml
    if not robot_xml:
        robot_xml = input("Absolute path to robot XML (e.g. .../unitree_robots/g1/g1_29dof.xml): ").strip()
    robot_xml_path = Path(robot_xml).resolve()
    if not robot_xml_path.is_file():
        print(f"ERROR: {robot_xml_path} not found.")
        return
    robot_xml_abs = str(robot_xml_path)

    out_dir = Path(args.out_dir) if args.out_dir else DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # Symlink robot meshdir -- MuJoCo resolves meshdir relative to the
    # top-level file, not the <include>'d file.
    robot_tree = ET.parse(robot_xml_path)
    robot_compiler = robot_tree.getroot().find("compiler")
    meshdir_rel = robot_compiler.get("meshdir", ".") if robot_compiler is not None else "."
    robot_meshdir_abs = (robot_xml_path.parent / meshdir_rel).resolve()

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

    robot_stem = robot_xml_path.stem

    for name, urdf_path, obj_dir in objects:
        urdf_data = parse_urdf(urdf_path)
        metadata = load_metadata(obj_dir)
        scene_xml = generate_scene(robot_xml_abs, name, urdf_data, obj_dir, metadata)

        out_path = out_dir / f"{robot_stem}_{name}.xml"
        out_path.write_text(scene_xml)
        print(f"  Generated: {out_path}")

    print(f"\nDone. {len(objects)} scene(s) in {out_dir}/")
    print(f"\nTo use in config.yaml:")
    print(f'  robot_scene: "{out_dir}/{robot_stem}_{objects[0][0]}.xml"')


if __name__ == "__main__":
    main()
