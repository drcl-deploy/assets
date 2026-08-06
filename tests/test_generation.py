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
