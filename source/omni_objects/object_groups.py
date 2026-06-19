"""Single source of truth for the object groups the sim spawns.

Kept dependency-free (pure stdlib) so both the Isaac Lab spawner
(omni_objects.py) and the standalone scene generator
(generate_uolm_scene_xmls.py) can import it.

Each pattern is relative to SIM_ASSETS_PATH / ASSETS_DIR and is either a direct
"*.urdf" path or a folder glob (each matched subdir expected to hold
{name}/{name}.urdf).
"""

OBJECT_GROUP_PATTERNS = [
    "omomo_objects/*",
    "sugar_objects/*",
    "custom_objects/*",
]
