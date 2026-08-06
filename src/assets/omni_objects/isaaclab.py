"""
custom omni-object cfgs that can be used to spawn a variety of objects with a single spawner.

to reuse existing assets, we support flexible pattern-based asset resolution. See build_omni_object_cfg and resolve_assets for details.
"""

import glob
import os
from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg

from assets.paths import GENERATED_ROOT

from .object_groups import OBJECT_GROUP_PATTERNS

ASSETS_DIR = GENERATED_ROOT


def _make_urdf_cfg(urdf_path: str) -> sim_utils.UrdfFileCfg:
    """Create a UrdfFileCfg from an absolute URDF path."""
    return sim_utils.UrdfFileCfg(
        fix_base=False,
        replace_cylinders_with_capsules=True,
        asset_path=urdf_path,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(stiffness=0, damping=0)
        ),
        # collider_type="convex_hull",
        collider_type="convex_decomposition",
        # collision_from_visuals=True,
    )


def resolve_assets(patterns: list[str]) -> dict[str, sim_utils.UrdfFileCfg]:
    """Resolve a list of asset patterns into a name -> UrdfFileCfg dict.

    Each pattern is relative to the generated asset root and can be:
      - A direct URDF path:  "basketball/basketball.urdf"
      - A folder glob:       "omomo_objects/*"   (expands to all subdirs,
                              each expected to contain {name}/{name}.urdf)
      - A recursive glob:    "omomo_objects/**"  (same, recursive)

    Returns:
        dict mapping uppercase object names to their UrdfFileCfg.
    """
    configs: dict[str, sim_utils.UrdfFileCfg] = {}

    for pattern in patterns:
        full_pattern = os.path.join(ASSETS_DIR, pattern)

        # Direct .urdf path
        if pattern.endswith(".urdf"):
            if os.path.isfile(full_pattern):
                name = Path(full_pattern).stem.upper()
                configs[name] = _make_urdf_cfg(full_pattern)
            else:
                print(f"[omni_objects] WARNING: URDF not found: {full_pattern}")
            continue

        # Glob pattern — expand and look for subfolders with matching URDFs
        matched_paths = sorted(glob.glob(full_pattern))
        for match in matched_paths:
            if not os.path.isdir(match):
                continue
            folder_name = os.path.basename(match)
            if folder_name.startswith("__"):
                continue
            urdf_path = os.path.join(match, folder_name + ".urdf")
            if os.path.isfile(urdf_path):
                configs[folder_name.upper()] = _make_urdf_cfg(urdf_path)
            else:
                print(f"[omni_objects] WARNING: expected URDF not found: {urdf_path}")

    return configs


def build_omni_object_cfg(
    patterns: list[str],
    prim_path: str = "{ENV_REGEX_NS}/Object",
    random_choice: bool = False,
    init_pos: tuple = (0.0, 0.0, 0.1213),
    activate_contact_sensors: bool = True,
) -> RigidObjectCfg:
    """Build a RigidObjectCfg with MultiAssetSpawner from mixed asset patterns.

    Args:
        patterns: List of asset patterns (see resolve_assets for syntax).
        prim_path: USD prim path template.
        random_choice: Whether to randomly pick among assets per env.
        init_pos: Initial position (x, y, z).
        activate_contact_sensors: Enable contact sensors on spawned objects.

    Example:
        cfg = build_omni_object_cfg([
            "basketball/basketball.urdf",
            "omomo_objects/*",
        ])
    """
    configs = resolve_assets(patterns)

    if not configs:
        raise ValueError(
            f"No assets resolved from patterns: {patterns}. "
            "Run `assets generate` before building object configurations."
        )

    return RigidObjectCfg(
        prim_path=prim_path,
        spawn=sim_utils.MultiAssetSpawnerCfg(
            assets_cfg=list(configs.values()),
            random_choice=random_choice,
            semantic_tags=[("class", name) for name in configs.keys()],
            activate_contact_sensors=activate_contact_sensors,
        ),
        init_state=RigidObjectCfg.InitialStateCfg(pos=init_pos, lin_vel=(0.0, 0.0, 0.0)),
    )


# ── Pre-built configs ──────────────────────────────────────────────────────────

OMNI_OBJECTS_CFG = build_omni_object_cfg(OBJECT_GROUP_PATTERNS)
