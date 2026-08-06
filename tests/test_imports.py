import subprocess
import sys


def test_base_imports_do_not_load_isaaclab():
    code = """
import sys
import assets
import assets.g1
import assets.g1.constants
import assets.hector_v1.constants
assert 'isaaclab' not in sys.modules
assert 'isaaclab_assets' not in sys.modules
"""
    subprocess.run([sys.executable, "-c", code], check=True)
