import xml.etree.ElementTree as ET

from assets.omni_objects.make_object_models import main


def test_generate_primitive_object(tmp_path):
    result = main(
        [
            "--all",
            "--object",
            "cube",
            "--no-decompose",
            "--output-root",
            str(tmp_path),
        ]
    )

    assert result == 0
    output = tmp_path / "custom_objects" / "cube"
    assert (output / "cube.urdf").is_file()
    assert (output / "cube_cvx_hull.xml").is_file()
    assert (output / "cube_cvx_dcmp.xml").is_file()


def test_generate_flat_rgba_material(tmp_path):
    result = main(
        [
            "--all",
            "--object",
            "trashcan",
            "--no-decompose",
            "--output-root",
            str(tmp_path),
        ]
    )

    assert result == 0
    output = tmp_path / "omomo_objects" / "trashcan" / "trashcan_cvx_hull.xml"
    asset = ET.parse(output).getroot().find("asset")
    assert asset is not None
    assert asset.find("texture") is None
    material = asset.find("material")
    assert material is not None
    assert material.get("rgba") == "1 0.9569 0.9059 1"
