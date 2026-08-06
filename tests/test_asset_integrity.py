import json
import xml.etree.ElementTree as ET
from pathlib import Path

from assets.paths import PACKAGE_ROOT


def test_python_sources_do_not_reference_legacy_environment_variable():
    for path in PACKAGE_ROOT.rglob("*.py"):
        assert "SIM_ASSETS_PATH" not in path.read_text()


def test_tracked_json_and_xml_parse():
    for path in PACKAGE_ROOT.rglob("*.json"):
        json.loads(path.read_text())
    for pattern in ("*.xml", "*.urdf"):
        for path in PACKAGE_ROOT.rglob(pattern):
            ET.parse(path)


def test_relative_xml_references_exist():
    missing = []
    for pattern in ("*.xml", "*.urdf"):
        for path in PACKAGE_ROOT.rglob(pattern):
            document = ET.parse(path).getroot()
            compiler = document.find("compiler")
            meshdir = compiler.get("meshdir") if compiler is not None else None
            texturedir = compiler.get("texturedir") if compiler is not None else None

            for element in document.iter():
                tag = element.tag.rsplit("}", 1)[-1]
                value = None
                base = path.parent
                if tag == "include":
                    value = element.get("file")
                elif tag == "mesh":
                    value = element.get("filename") or element.get("file")
                    if meshdir:
                        base /= meshdir
                elif tag in {"texture", "hfield"}:
                    value = element.get("file")
                    if texturedir:
                        base /= texturedir

                if not value or value.startswith(("package://", "model://", "http://", "https://")):
                    continue
                target = Path(value.removeprefix("file://"))
                if not target.is_absolute():
                    target = base / target
                if not target.exists():
                    missing.append((path, value))

    assert not missing
