"""Generate the canonical Repose cube map used by the sim2sim cube asset."""

from pathlib import Path

from PIL import Image


# Keep this in the canonical FACE_COLORS order from src/vibe/assets/repose.py:
# +X, -X, +Y, -Y, +Z, -Z.  MuJoCo's cube-map axes are R/L = +/-X,
# U/D = +/-Y, F/B = +/-Z, so metadata.json maps these tiles to RLUDFB.
FACE_RGB = (
    (230, 51, 51),   # +X red
    (242, 115, 26),  # -X orange
    (51, 230, 51),   # +Y green
    (230, 230, 51),  # -Y yellow
    (51, 51, 230),   # +Z blue
    (204, 51, 166),  # -Z purplish pink
)
FACE_SIZE = 64


def main() -> None:
    image = Image.new("RGB", (FACE_SIZE * len(FACE_RGB), FACE_SIZE))
    for index, rgb in enumerate(FACE_RGB):
        tile = Image.new("RGB", (FACE_SIZE, FACE_SIZE), rgb)
        image.paste(tile, (index * FACE_SIZE, 0))
    image.save(Path(__file__).with_name("repose_cube.png"), optimize=True)


if __name__ == "__main__":
    main()
