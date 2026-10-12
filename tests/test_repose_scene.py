"""The release cube has one collider and massless, independently colored faces."""
import xml.etree.ElementTree as ET

import pytest

from assets.repose_scene import generate


def test_repose_generation_preserves_robot_and_cube_contract(tmp_path):
    mujoco = pytest.importorskip("mujoco")
    robot = tmp_path / "robot.xml"
    source = '<mujoco><compiler meshdir="meshes"/><worldbody/></mujoco>'
    robot.write_text(source)
    (tmp_path / "meshes").mkdir()
    scene = generate(robot, tmp_path / "output")
    first = scene.read_bytes()
    assert generate(robot, tmp_path / "output").read_bytes() == first
    assert robot.read_text() == source
    model = mujoco.MjModel.from_xml_path(str(scene))
    assert model.body("cube").mass == pytest.approx(0.62369)
    assert tuple(model.geom("cube_core").size) == pytest.approx((0.3048,) * 3)
    assert model.opt.timestep == 0.005
    assert model.opt.integrator == mujoco.mjtIntegrator.mjINT_IMPLICITFAST
    assert model.opt.iterations == 10
    assert model.opt.ls_iterations == 20
    assert model.geom("cube_core").contype == 1
    for index in range(6):
        face = model.geom(f"cube_face_{index}")
        assert face.contype == 0 and face.conaffinity == 0
    tree = ET.parse(scene)
    assert tree.find(".//texture") is None
