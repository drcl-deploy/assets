from assets.paths import PACKAGE_ROOT, asset_path, generated_path


def test_tracked_asset_path():
    assert asset_path("g1", "g1_bm.xml").is_file()
    assert asset_path("g1", "g1_bm.xml").is_relative_to(PACKAGE_ROOT)


def test_generated_path_is_outside_package():
    assert not generated_path().is_relative_to(PACKAGE_ROOT)
