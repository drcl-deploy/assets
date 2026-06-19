#!/usr/bin/env python3
"""Offline convex decomposition (CoACD) -> per-object MuJoCo collider XML.

MuJoCo collides a `<geom type="mesh">` as a single CONVEX HULL (no auto-decomposition,
unlike IsaacLab/PhysX cooking). So concave objects (chairs, tires, trashcans) get phantom
contacts. This script runs CoACD on an object's visual mesh and writes a *single-body,
multi-geom* collider — one convex `<geom>` per decomposed part — that MuJoCo treats exactly.

Standalone: emits files INSIDE each object's own folder. Nothing else is touched; wire the
collider into scenes manually when you need it.

Per object `<dir>/<name>.obj` it writes:
    <dir>/collision/<name>_cvx_000.obj ...      # the convex parts
    <dir>/<name>_collision.xml                  # one body, freejoint, N mesh geoms (loadable alone)

Usage:
    python make_convex_colliders.py <obj_or_dir> [more ...] [--threshold 0.05] [--force]
    # examples:
    python make_convex_colliders.py ../custom_objects/woodchair2
    python make_convex_colliders.py ../omomo_objects/*/ --threshold 0.03 --force
"""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import trimesh
import coacd


# distinct colours so each convex part is visible when you load the XML in a viewer
_PALETTE = [
    "0.90 0.30 0.30 1", "0.30 0.70 0.90 1", "0.40 0.80 0.40 1", "0.95 0.75 0.25 1",
    "0.70 0.45 0.85 1", "0.95 0.55 0.25 1", "0.40 0.85 0.80 1", "0.85 0.50 0.65 1",
]


def resolve_obj(path: Path) -> Path:
    """Accept an .obj file or an object dir holding <name>/<name>.obj."""
    if path.is_file() and path.suffix.lower() == ".obj":
        return path
    if path.is_dir():
        cand = path / f"{path.name}.obj"
        if cand.is_file():
            return cand
    raise FileNotFoundError(f"No <name>.obj found for: {path}")


def read_urdf_mass(obj_dir: Path, name: str) -> float:
    """Total mass from a sibling single-link URDF, if present (else 1.0)."""
    urdf = obj_dir / f"{name}.urdf"
    if not urdf.is_file():
        return 1.0
    try:
        link = ET.parse(urdf).getroot().find("link")
        return float(link.find("inertial").find("mass").get("value"))
    except Exception:
        return 1.0


def decompose(obj_path: Path, threshold: float, max_hulls: int,
              preprocess_resolution: int, seed: int) -> list[trimesh.Trimesh]:
    mesh = trimesh.load(obj_path, force="mesh")
    cmesh = coacd.Mesh(np.asarray(mesh.vertices, np.float64), np.asarray(mesh.faces, np.int32))
    parts = coacd.run_coacd(
        cmesh,
        threshold=threshold,
        max_convex_hull=max_hulls,
        preprocess_mode="auto",          # voxel-remesh first -> robust on non-watertight scans
        preprocess_resolution=preprocess_resolution,
        merge=True,
        seed=seed,
    )
    return [trimesh.Trimesh(vertices=v, faces=f, process=False) for v, f in parts]


COLLIDER_TEMPLATE = """\
<mujoco model="{name}_collision">
  <asset>
{assets}
  </asset>
  <worldbody>
    <body name="{name}" pos="{pos}" quat="{quat}">
      <freejoint/>
{geoms}
    </body>
  </worldbody>
</mujoco>
"""


def write_collider(obj_dir: Path, name: str, parts: list[trimesh.Trimesh],
                   subdir: str, total_mass: float) -> Path:
    coll_dir = obj_dir / subdir
    coll_dir.mkdir(exist_ok=True)
    # clear stale parts for this object
    for old in coll_dir.glob(f"{name}_cvx_*.obj"):
        old.unlink()

    vols = np.array([max(p.volume, 1e-9) for p in parts], dtype=np.float64)
    mass_frac = vols / vols.sum()

    assets, geoms = [], []
    for i, part in enumerate(parts):
        part_path = coll_dir / f"{name}_cvx_{i:03d}.obj"
        part.export(part_path)
        mname = f"{name}_cvx_{i:03d}"
        assets.append(f'    <mesh name="{mname}" file="{part_path.resolve()}"/>')
        rgba = _PALETTE[i % len(_PALETTE)]
        m = total_mass * mass_frac[i]
        geoms.append(
            f'      <geom type="mesh" mesh="{mname}" mass="{m:.6g}" '
            f'friction="0.6 0.6 0.0001" rgba="{rgba}"/>'
        )

    # spawn pose from the object's metadata.json (defaults if absent)
    pos, quat = "0 0 0.5", "1 0 0 0"
    meta_path = obj_dir / "metadata.json"
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text())
        pos = meta.get("initial_pos", pos)
        quat = meta.get("initial_quat", quat)

    xml = COLLIDER_TEMPLATE.format(name=name, assets="\n".join(assets), geoms="\n".join(geoms),
                                   pos=pos, quat=quat)
    out = obj_dir / f"{name}_collision.xml"
    out.write_text(xml)
    return out


DROP_TEMPLATE = """\
<mujoco model="{name}_drop">
  <compiler angle="radian"/>
  <option timestep="0.004"/>
  <visual><global azimuth="-130" elevation="-20"/><headlight diffuse="0.7 0.7 0.7"/><map force="0.05"/></visual>
  <asset>
    <mesh name="{name}_orig" file="{orig_abs}"/>
{assets}
  </asset>
  <worldbody>
    <light pos="0 0 4" dir="0 0 -1" directional="true"/>
    <geom name="floor" type="plane" size="0 0 0.05" rgba="0.3 0.3 0.3 1" friction="1 0.1 0.01"/>
    <body name="BEFORE_hull" pos="{dx_neg} 0 {H}">
      <freejoint/>
      <geom type="mesh" mesh="{name}_orig" mass="{mass:.6g}" rgba="0.85 0.30 0.30 0.7" friction="1 0.1 0.01"/>
    </body>
    <body name="AFTER_{n}parts" pos="{dx_pos} 0 {H}">
      <freejoint/>
{geoms}
    </body>
  </worldbody>
</mujoco>
"""


def _random_quat_wxyz() -> np.ndarray:
    """Uniform random orientation on SO(3) (Shoemake), wxyz.

    Continuous (not 90°-snapped): the object lands on faces/edges/corners, so every drop
    looks genuinely different — including the near-cubic convex hull, which is visually
    invariant under axis-aligned rotations.
    """
    u1, u2, u3 = np.random.random(3)
    return np.array([
        np.sqrt(u1) * np.cos(2 * np.pi * u3),       # w
        np.sqrt(1 - u1) * np.sin(2 * np.pi * u2),   # x
        np.sqrt(1 - u1) * np.cos(2 * np.pi * u2),   # y
        np.sqrt(u1) * np.sin(2 * np.pi * u3),       # z
    ])


def view_comparison(obj_path: Path, name: str, coll_dir: Path):
    """Interactive physics drop test: BEFORE (single convex hull) | AFTER (decomposed parts).

    Both objects drop under gravity from a height at a random orientation onto the floor;
    contact points are drawn. The hull tumbles/rests differently than the decomposed body —
    that's the interaction difference the matrix cares about.
    Keys: SPACE = pause/play, BACKSPACE = re-drop (new random orientation).
    """
    import time
    import mujoco
    import mujoco.viewer

    src = trimesh.load(obj_path, force="mesh")
    size = src.bounds[1] - src.bounds[0]
    dx = float(size[0]) / 2 + float(max(size)) * 0.6   # half-spacing between the two
    H = float(max(size)) * 1.5 + 0.3                    # drop height

    parts = sorted(coll_dir.glob(f"{name}_cvx_*.obj"))
    if not parts:
        raise FileNotFoundError(f"no decomposed parts in {coll_dir} — run without --view first")
    total_mass = read_urdf_mass(obj_path.parent, name)
    pmeshes = [trimesh.load(p, force="mesh") for p in parts]
    vols = np.array([max(pm.volume, 1e-9) for pm in pmeshes])
    pmass = total_mass * vols / vols.sum()

    assets, geoms = [], []
    for i, p in enumerate(parts):
        mname = f"{name}_cvx_{i:03d}"
        assets.append(f'    <mesh name="{mname}" file="{p.resolve()}"/>')
        rgba = _PALETTE[i % len(_PALETTE)]
        geoms.append(f'      <geom type="mesh" mesh="{mname}" mass="{pmass[i]:.6g}" '
                     f'friction="1 0.1 0.01" rgba="{rgba}"/>')

    xml = DROP_TEMPLATE.format(
        name=name, orig_abs=obj_path.resolve(), assets="\n".join(assets), geoms="\n".join(geoms),
        dx_neg=-dx, dx_pos=dx, H=H, mass=total_mass, n=len(parts),
    )
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)

    # freejoint qpos addresses for the two bodies
    qadr = {}
    for bn, x in [("BEFORE_hull", -dx), (f"AFTER_{len(parts)}parts", dx)]:
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, bn)
        qadr[bn] = (int(model.jnt_qposadr[model.body_jntadr[bid]]), x)

    st_quat = {"prev": None}

    def drop():
        quat = _random_quat_wxyz()                       # new orientation every reset
        while st_quat["prev"] is not None and np.allclose(quat, st_quat["prev"]):
            quat = _random_quat_wxyz()                   # never repeat the previous one
        st_quat["prev"] = quat
        for q, x in qadr.values():
            pose = np.array([x, 0.0, H, *quat])
            data.qpos[q:q + 7] = pose
            # also point qpos0 here: the viewer's native Backspace does mj_resetData ->
            # qpos0; without this it would flush to identity and clobber our drop.
            model.qpos0[q:q + 7] = pose
        data.qvel[:] = 0.0
        mujoco.mj_forward(model, data)
        print(f"  [re-drop] quat(wxyz)={np.round(quat, 3)}")

    KEY_SPACE, KEY_BACKSPACE = 32, 259
    st = {"paused": False, "redrop": True}  # apply first drop in the loop

    def key_cb(key):
        # only SET FLAGS here — the native viewer also handles Backspace (resets to qpos0),
        # so we re-drop in the main loop afterwards to override it.
        if key == KEY_SPACE:
            st["paused"] = not st["paused"]
        elif key == KEY_BACKSPACE:
            st["redrop"] = True

    print(f"[drop] {name}: BEFORE (red hull) | AFTER ({len(parts)} parts)  | "
          f"SPACE=pause  BACKSPACE=re-drop  (close to continue)")
    with mujoco.viewer.launch_passive(model, data, key_callback=key_cb) as viewer:
        viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = True
        viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = True
        # render geoms AS their collider: BEFORE -> solid hull block, AFTER -> the convex parts.
        # without this the red mesh draws its true shape but still collides as a hull (misleading).
        viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONVEXHULL] = True
        while viewer.is_running():
            if st["redrop"]:
                drop()                      # runs after native reset -> our random pose wins
                st["redrop"] = False
            elif not st["paused"]:
                mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(model.opt.timestep)


def process(path: Path, threshold: float, max_hulls: int, preprocess_resolution: int,
            seed: int, subdir: str, force: bool, view: bool = False):
    obj_path = resolve_obj(path)
    obj_dir, name = obj_path.parent, obj_path.stem
    out_xml = obj_dir / f"{name}_collision.xml"

    if out_xml.exists() and not force:
        print(f"[skip] exists: {out_xml}  (--force to redo)")
    else:
        src = trimesh.load(obj_path, force="mesh")
        parts = decompose(obj_path, threshold, max_hulls, preprocess_resolution, seed)
        mass = read_urdf_mass(obj_dir, name)
        out = write_collider(obj_dir, name, parts, subdir, mass)

        # sanity: hull-volume coverage vs source convex hull
        part_vol = sum(p.volume for p in parts)
        try:
            cover = part_vol / max(src.convex_hull.volume, 1e-9)
        except Exception:
            cover = float("nan")
        print(f"[ok] {name}: {len(parts)} parts | mass={mass:.3g} | "
              f"vol/hull={cover:.2f} | -> {out.name}")
        if len(parts) > 64:
            print(f"     ! {len(parts)} parts is a lot — raise --threshold for cheaper collision.")

    if view:
        view_comparison(obj_path, name, obj_dir / subdir)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", type=Path, help="object .obj file(s) or object dir(s)")
    ap.add_argument("--threshold", type=float, default=0.05,
                    help="CoACD concavity threshold; lower = more parts = tighter (0.02..0.1)")
    ap.add_argument("--max-hulls", type=int, default=-1, help="cap on convex parts (-1 = no cap)")
    ap.add_argument("--preprocess-resolution", type=int, default=50,
                    help="voxel resolution for the watertight pre-remesh")
    ap.add_argument("--seed", type=int, default=0, help="deterministic seed")
    ap.add_argument("--subdir", default="collision", help="parts output subdir name")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="silence CoACD's own logging")
    ap.add_argument("--view", action="store_true",
                    help="after each object, open MuJoCo viewer: original hull | decomposed parts")
    args = ap.parse_args()

    coacd.set_log_level("error" if args.quiet else "warn")

    for p in args.paths:
        try:
            process(p, args.threshold, args.max_hulls, args.preprocess_resolution,
                    args.seed, args.subdir, args.force, args.view)
        except Exception as e:
            print(f"[fail] {p}: {e}")


if __name__ == "__main__":
    main()
