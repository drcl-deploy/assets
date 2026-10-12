"""Generate the frozen Repose scene with native, independently colored faces."""

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from assets.paths import PACKAGE_ROOT


# Canonical +/-X, +/-Y, +/-Z palette from vibe.assets.repose.
FACE_COLORS = (
    (0.9, 0.2, 0.2, 1.0), (0.95, 0.45, 0.1, 1.0),
    (0.2, 0.9, 0.2, 1.0), (0.9, 0.9, 0.2, 1.0),
    (0.2, 0.2, 0.9, 1.0), (0.8, 0.2, 0.65, 1.0),
)


def numbers(values):
    return " ".join(str(value) for value in values)


def generate(robot_xml: Path, output: Path) -> Path:
    """Compose the simulator robot with public Repose's primitive cube contract."""
    robot_xml = robot_xml.resolve(strict=True)
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    metadata = json.loads((PACKAGE_ROOT / "custom_objects/cube/metadata.json").read_text())
    collider = metadata["simple_collider"]
    extents = [collider[axis] / 2 for axis in ("x", "y", "z")]
    if collider["geometry"] != "box" or len(set(extents)) != 1:
        raise ValueError("Repose requires a cube collider")
    half = extents[0]
    mass = metadata["inertial"]["mass"]

    # Use an absolute mesh directory in the generated copy. Source XML stays
    # untouched; visual groups follow the public robot convention (2/3).
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    robot = ET.parse(robot_xml, parser=parser)
    compiler = robot.getroot().find("compiler")
    compiler.set("meshdir", str((robot_xml.parent / compiler.get("meshdir", ".")).resolve()))
    for geom in robot.getroot().iter("geom"):
        if geom.get("group") == "1":
            geom.set("group", "2")
        elif geom.get("group", "0") == "0":
            geom.set("group", "3")
    robot_path = output / "g1_repose_robot.xml"
    robot.write(robot_path, encoding="unicode")

    scene = ET.Element("mujoco", model="g1_repose")
    ET.SubElement(scene, "include", file=str(robot_path))
    # Repose's task overrides on mjlab 1.4.0's MuJoCo defaults.
    ET.SubElement(scene, "option", timestep="0.005", integrator="implicitfast",
                  iterations="10", ls_iterations="20", tolerance="1e-8",
                  ls_tolerance="0.01", solver="Newton", cone="pyramidal")
    world = ET.SubElement(scene, "worldbody")
    ET.SubElement(world, "light", pos="0 0 3", dir="0 0 -1", directional="true")
    ET.SubElement(world, "geom", name="floor", type="plane", size="0 0 0.05",
                  rgba="0.30 0.30 0.32 1")
    body = ET.SubElement(world, "body", name="cube", pos=metadata["initial_pos"],
                         quat=metadata["initial_quat"])
    ET.SubElement(body, "freejoint", name="cube_joint")
    # Let MuJoCo derive the same exact inertia as the public MjSpec builder.
    ET.SubElement(body, "geom", name="cube_core", type="box", size=numbers(extents),
                  mass=str(mass), rgba="0.5 0.5 0.5 0", group="3",
                  contype="1", conaffinity="1")
    for index, rgba in enumerate(FACE_COLORS):
        axis, sign = index // 2, 1 if index % 2 == 0 else -1
        pos, size = [0.0] * 3, [half] * 3
        pos[axis], size[axis] = sign * half, 0.002
        ET.SubElement(body, "geom", name=f"cube_face_{index}", type="box",
                      pos=numbers(pos), size=numbers(size), rgba=numbers(rgba),
                      contype="0", conaffinity="0", mass="0")
    path = output / "g1_repose.xml"
    ET.indent(scene)
    ET.ElementTree(scene).write(path, encoding="unicode")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--robot-xml", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    print(generate(args.robot_xml, args.out_dir))


if __name__ == "__main__":
    main()
