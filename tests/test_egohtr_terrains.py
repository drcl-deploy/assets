"""Shipped terrain descriptors resolve to the exact packaged collision meshes."""

import hashlib
import json

from assets import asset_path


def test_egohtr_descriptors_and_hashes():
    expected = {
        "rocky-path_s7_bzb_01__40-50s": 360,
        "cliff-jump_s4_bzb_01__28-38s": 192,
    }
    for family, count in expected.items():
        root = asset_path("terrain", "egohtr", family)
        descriptor = root / "tile.json"
        tile = json.loads(descriptor.read_text())
        provenance = json.loads((root / "provenance.json").read_text())
        assert tile["family"] == family
        assert tile["level"] == 0.0
        assert len(tile["meshes"]) == count
        assert provenance["license"] == "CC-BY-4.0"
        assert hashlib.sha256(descriptor.read_bytes()).hexdigest() == provenance["tile_sha256"]
        for mesh in tile["meshes"]:
            path = (root / mesh["file"]).resolve()
            assert path.is_relative_to(root.resolve())
            assert hashlib.sha256(path.read_bytes()).hexdigest() == mesh["sha256"]
            assert mesh["scale"] == [provenance["scene_scale"]] * 3
