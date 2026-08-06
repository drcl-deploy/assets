#!/usr/bin/env python3
"""Interactive drop test: hull vs decomposed collision side by side.

Single object or ALL objects at once.  Each object pair is laid out along
the Y axis; hull (left/−X) vs decomposed (right/+X).

Keys: SPACE = pause/play, BACKSPACE = re-drop (new random orientation).

Usage:
    python view_drop_test.py ../omomo_objects/trashcan
    python view_drop_test.py ../custom_objects/woodchair2
    python view_drop_test.py --all
"""

from __future__ import annotations

import argparse
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

from assets.paths import GENERATED_ROOT, PACKAGE_ROOT

from .object_groups import OBJECT_GROUP_PATTERNS

SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = PACKAGE_ROOT

# ── Scene assembly ───────────────────────────────────────────────────────────

DROP_SCENE = """\
<mujoco model="{name}">
  <compiler angle="radian"/>
  <option timestep="0.004"/>
  <visual>
    <global azimuth="-130" elevation="-20"/>
    <headlight diffuse="0.7 0.7 0.7"/>
    <map force="0.05"/>
  </visual>

  <asset>
{all_assets}
  </asset>

  <worldbody>
    <light pos="0 0 4" dir="0 0 -1" directional="true"/>
    <geom name="floor" type="plane" size="0 0 0.05" rgba="0.3 0.3 0.3 1" friction="1 0.1 0.01"/>
{all_bodies}
  </worldbody>
</mujoco>
"""


def _random_quat_wxyz() -> np.ndarray:
    """Uniform random orientation on SO(3) (Shoemake), wxyz."""
    u1, u2, u3 = np.random.random(3)
    return np.array(
        [
            np.sqrt(u1) * np.cos(2 * np.pi * u3),
            np.sqrt(1 - u1) * np.sin(2 * np.pi * u2),
            np.sqrt(1 - u1) * np.cos(2 * np.pi * u2),
            np.sqrt(u1) * np.sin(2 * np.pi * u3),
        ]
    )


def _extract_object_xml(
    xml_path: Path, old_name: str, new_name: str, x_offset: float, y_offset: float, height: float
) -> tuple[str, str]:
    """Parse an object XML, rename to avoid clashes, return (assets_str, bodies_str)."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    name_map: dict[str, str] = {}
    asset_el = root.find("asset")
    if asset_el is not None:
        for child in asset_el:
            old_aname = child.get("name")
            if old_aname:
                new_aname = old_aname.replace(old_name, new_name, 1)
                child.set("name", new_aname)
                name_map[old_aname] = new_aname
            if child.tag == "material" and child.get("texture"):
                tex = child.get("texture")
                if tex in name_map:
                    child.set("texture", name_map[tex])

    wb = root.find("worldbody")
    if wb is not None:
        for body in wb.findall("body"):
            body.set("name", new_name)
            body.set("pos", f"{x_offset} {y_offset} {height}")
            body.set("quat", "1 0 0 0")
            for geom in body.findall("geom"):
                for attr in ("mesh", "material", "name"):
                    val = geom.get(attr)
                    if val and val in name_map:
                        geom.set(attr, name_map[val])

    assets_str = (
        "\n".join("    " + ET.tostring(c, encoding="unicode") for c in asset_el)
        if asset_el is not None
        else ""
    )

    bodies_str = (
        "\n".join("    " + ET.tostring(b, encoding="unicode") for b in wb.findall("body"))
        if wb is not None
        else ""
    )

    return assets_str, bodies_str


# ── Object discovery ─────────────────────────────────────────────────────────


def discover_drop_objects() -> list[tuple[str, Path]]:
    """Find objects that have both _cvx_hull.xml and _cvx_dcmp.xml."""
    objects: list[tuple[str, Path]] = []
    seen: set[str] = set()

    for pattern in OBJECT_GROUP_PATTERNS:
        if pattern.endswith(".urdf"):
            source_dir = (ASSETS_DIR / pattern).parent
            name = source_dir.name
            obj_dir = GENERATED_ROOT / source_dir.relative_to(ASSETS_DIR)
        else:
            # expand glob
            for source_dir in sorted(ASSETS_DIR.glob(pattern)):
                if not source_dir.is_dir() or source_dir.name.startswith("__"):
                    continue
                name = source_dir.name
                obj_dir = GENERATED_ROOT / source_dir.relative_to(ASSETS_DIR)
                if name not in seen:
                    hull = obj_dir / f"{name}_cvx_hull.xml"
                    dcmp = obj_dir / f"{name}_cvx_dcmp.xml"
                    if hull.is_file() and dcmp.is_file():
                        seen.add(name)
                        objects.append((name, obj_dir))
                    elif hull.is_file():
                        print(f"  [skip] {name}: no _cvx_dcmp.xml")
            continue

        if name not in seen:
            hull = obj_dir / f"{name}_cvx_hull.xml"
            dcmp = obj_dir / f"{name}_cvx_dcmp.xml"
            if hull.is_file() and dcmp.is_file():
                seen.add(name)
                objects.append((name, obj_dir))

    return objects


# ── Run ──────────────────────────────────────────────────────────────────────


def run(obj_dirs: list[tuple[str, Path]]):
    import mujoco
    import mujoco.viewer
    import trimesh

    # compute per-object sizes and layout
    entries = []  # (name, obj_dir, dx, H, obj_extent)
    for name, obj_dir in obj_dirs:
        obj_path = obj_dir / f"{name}.obj"
        if obj_path.is_file():
            src = trimesh.load(obj_path, force="mesh")
            size = src.bounds[1] - src.bounds[0]
        else:
            size = np.array([0.3, 0.3, 0.3])
        extent = float(max(size))
        dx = float(size[0]) / 2 + extent * 0.6
        H = extent * 1.5 + 0.3
        entries.append((name, obj_dir, dx, H, extent))

    # use global max height so everything drops from the same level
    global_H = max(H for _, _, _, H, _ in entries)

    # NxN grid layout — each cell holds a hull/dcmp pair side by side on X
    import math

    n = len(entries)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    max_ext = max(ext for _, _, _, _, ext in entries)
    max_dx = max(dx for _, _, dx, _, _ in entries)
    cell_x = max_dx * 2 + max_ext * 1.0  # width per cell (hull + gap + dcmp)
    cell_y = max_ext * 2.5  # depth per cell

    # center the grid at origin
    x_origin = -cell_x * (cols - 1) / 2
    y_origin = -cell_y * (rows - 1) / 2

    all_assets, all_bodies = [], []
    body_info = []  # (body_name, x, y) for drop reset

    for i, (name, obj_dir, dx, _, extent) in enumerate(entries):
        col = i % cols
        row = i // cols
        cx = x_origin + col * cell_x  # cell center X
        cy = y_origin + row * cell_y  # cell center Y

        hull_xml = obj_dir / f"{name}_cvx_hull.xml"
        dcmp_xml = obj_dir / f"{name}_cvx_dcmp.xml"

        hull_name = f"{name}_HULL"
        dcmp_name = f"{name}_DCMP"

        hx, dx_pos = cx - dx, cx + dx  # hull left, dcmp right within cell

        ha, hb = _extract_object_xml(hull_xml, name, hull_name, hx, cy, global_H)
        da, db = _extract_object_xml(dcmp_xml, name, dcmp_name, dx_pos, cy, global_H)

        all_assets.extend([ha, da])
        all_bodies.extend([hb, db])
        body_info.append((hull_name, hx, cy))
        body_info.append((dcmp_name, dx_pos, cy))

    scene_label = "drop_test_all" if len(entries) > 1 else entries[0][0]
    scene_xml = DROP_SCENE.format(
        name=scene_label,
        all_assets="\n".join(all_assets),
        all_bodies="\n".join(all_bodies),
    )

    model = mujoco.MjModel.from_xml_string(scene_xml)
    data = mujoco.MjData(model)

    # map body names to freejoint qpos addresses
    qadr = {}
    for bname, x, y in body_info:
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, bname)
        if bid < 0:
            print(f"  warning: body '{bname}' not found")
            continue
        qadr[bname] = (int(model.jnt_qposadr[model.body_jntadr[bid]]), x, y)

    st_quat: dict[str, np.ndarray | None] = {"prev": None}

    def drop():
        quat = _random_quat_wxyz()
        while st_quat["prev"] is not None and np.allclose(quat, st_quat["prev"]):
            quat = _random_quat_wxyz()
        st_quat["prev"] = quat
        for q, x, y in qadr.values():
            pose = np.array([x, y, global_H, *quat])
            data.qpos[q : q + 7] = pose
            model.qpos0[q : q + 7] = pose
        data.qvel[:] = 0.0
        mujoco.mj_forward(model, data)
        print(f"  [drop] quat(wxyz)={np.round(quat, 3)}")

    KEY_SPACE, KEY_BACKSPACE = 32, 259
    st = {"paused": False, "redrop": True}

    def key_cb(key):
        if key == KEY_SPACE:
            st["paused"] = not st["paused"]
        elif key == KEY_BACKSPACE:
            st["redrop"] = True

    names = [n for n, _ in obj_dirs]
    print(f"[drop test] {len(names)} object(s): {', '.join(names)}")
    print("  each pair: LEFT=hull | RIGHT=decomposed")
    print("  SPACE=pause  BACKSPACE=re-drop  (close window to exit)")

    with mujoco.viewer.launch_passive(model, data, key_callback=key_cb) as viewer:
        viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = True
        viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = True
        viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONVEXHULL] = True
        while viewer.is_running():
            if st["redrop"]:
                drop()
                st["redrop"] = False
            elif not st["paused"]:
                mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(model.opt.timestep)


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "paths", nargs="*", type=Path, help="object dir(s) (e.g. ../omomo_objects/trashcan)"
    )
    ap.add_argument(
        "--all", action="store_true", help="drop all objects from OBJECT_GROUP_PATTERNS at once"
    )
    args = ap.parse_args()

    if args.all:
        obj_dirs = discover_drop_objects()
        if not obj_dirs:
            print("No objects with both _cvx_hull.xml and _cvx_dcmp.xml found.")
            return
    elif args.paths:
        obj_dirs = []
        for p in args.paths:
            d = p.resolve()
            if not d.is_dir():
                print(f"ERROR: {d} is not a directory")
                continue
            obj_dirs.append((d.name, d))
        if not obj_dirs:
            return
    else:
        ap.print_help()
        return

    run(obj_dirs)


if __name__ == "__main__":
    main()
