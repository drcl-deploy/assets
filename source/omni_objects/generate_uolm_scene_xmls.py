#!/usr/bin/env python3
"""Generate UOLM scene XMLs: robot + object via <include>.

Each scene XML includes the robot model and one object model (hull or
decomposed).  Swap collision model by commenting/uncommenting the object
<include> line.

Usage:
    python generate_uolm_scene_xmls.py --robot-xml /path/to/g1_29dof.xml
    python generate_uolm_scene_xmls.py --robot-xml /path/to/g1_29dof.xml --object trashcan
    python generate_uolm_scene_xmls.py --robot-xml /path/to/g1_29dof.xml --model dcmp
"""

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = SCRIPT_DIR.parent
DEFAULT_OUT_DIR = SCRIPT_DIR / "scenes"

# ── Object discovery ─────────────────────────────────────────────────────────

from object_groups import OBJECT_GROUP_PATTERNS


def discover_objects(filter_name: str | None = None,
                     model: str = "hull") -> list[tuple[str, Path, Path]]:
    """Returns list of (name, object_xml_path, object_dir).

    Looks for <name>_cvx_{model}.xml in each object directory.
    """
    suffix = f"_cvx_{model}.xml"
    objects: list[tuple[str, Path, Path]] = []
    seen: set[str] = set()

    for pattern in OBJECT_GROUP_PATTERNS:
        if pattern.endswith(".urdf"):
            obj_dir = (ASSETS_DIR / pattern).parent
            name = obj_dir.name
            xml_path = obj_dir / f"{name}{suffix}"
            if name not in seen and xml_path.is_file():
                seen.add(name)
                objects.append((name, xml_path, obj_dir))
            continue

        for match in sorted(ASSETS_DIR.glob(pattern)):
            if not match.is_dir() or match.name.startswith("__"):
                continue
            name = match.name
            xml_path = match / f"{name}{suffix}"
            if name not in seen and xml_path.is_file():
                seen.add(name)
                objects.append((name, xml_path, match))

    if filter_name:
        objects = [(n, x, d) for n, x, d in objects if n == filter_name]
    return objects


# ── Scene template ───────────────────────────────────────────────────────────

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
  </asset>

  <worldbody>
    <light pos="2 2 4" dir="-0.5 -0.5 -1" directional="true" diffuse="0.6 0.6 0.6" specular="0.2 0.2 0.2"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
  </worldbody>

  <!-- Object model (swap hull/dcmp by commenting) -->
  <include file="{object_xml_abs}"/>
{alt_include}
</mujoco>
"""


def generate_scene(robot_xml_abs: str, object_name: str,
                   object_xml_abs: str, alt_xml_abs: str | None) -> str:
    model_name = f"{Path(robot_xml_abs).stem} + {object_name}"
    alt_include = ""
    if alt_xml_abs:
        alt_include = f'  <!-- <include file="{alt_xml_abs}"/> -->'
    return SCENE_TEMPLATE.format(
        model_name=model_name,
        robot_xml_abs=robot_xml_abs,
        object_xml_abs=object_xml_abs,
        alt_include=alt_include,
    )


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--robot-xml", default=None,
                        help="Absolute path to robot MuJoCo XML")
    parser.add_argument("--object", default=None,
                        help="Generate for a single object only")
    parser.add_argument("--model", choices=["hull", "dcmp"], default="hull",
                        help="Object collision model (default: hull)")
    parser.add_argument("--out-dir", default=None,
                        help=f"Output directory (default: {DEFAULT_OUT_DIR})")
    args = parser.parse_args()

    robot_xml = args.robot_xml
    if not robot_xml:
        robot_xml = input("Absolute path to robot XML: ").strip()
    robot_xml_path = Path(robot_xml).resolve()
    if not robot_xml_path.is_file():
        print(f"ERROR: {robot_xml_path} not found.")
        return
    robot_xml_abs = str(robot_xml_path)

    out_dir = Path(args.out_dir) if args.out_dir else DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # Symlink robot meshdir (MuJoCo resolves meshdir relative to top-level file)
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

    objects = discover_objects(args.object, args.model)
    if not objects:
        print(f"No objects found{f' matching {args.object!r}' if args.object else ''}.")
        print("  Did you run make_object_models.py first?")
        return

    robot_stem = robot_xml_path.stem
    alt_model = "dcmp" if args.model == "hull" else "hull"

    for name, obj_xml, obj_dir in objects:
        # check for alternative model XML
        alt_xml = obj_dir / f"{name}_cvx_{alt_model}.xml"
        alt_abs = str(alt_xml.resolve()) if alt_xml.is_file() else None

        scene_xml = generate_scene(robot_xml_abs, name,
                                   str(obj_xml.resolve()), alt_abs)
        out_path = out_dir / f"{robot_stem}_{name}.xml"
        out_path.write_text(scene_xml)
        print(f"  Generated: {out_path}")

    print(f"\nDone. {len(objects)} scene(s) in {out_dir}/")
    print(f"\nTo use in config.yaml:")
    print(f'  robot_scene: "{out_dir}/{robot_stem}_{objects[0][0]}.xml"')


if __name__ == "__main__":
    main()
