# assets

Simulation assets for Python training and ROS 2 sim-to-sim workflows.

## Install

```bash
git lfs pull
pip install -e .
assets generate
```

## Python

```python
from assets.paths import asset_path
from assets.g1.isaaclab import G1_BM_CFG

robot_xml = asset_path("g1", "g1_bm.xml")
```

Isaac Lab modules are optional and imported explicitly.

## Paths

```bash
assets path
assets generated-path
```

Use these paths from ROS 2 or sim-to-sim configuration.

## More

- [Python imports](docs/python.md)
- [Generating object models](docs/generation.md)
- [ROS 2 paths](docs/ros2.md)
- [Adding assets](docs/adding-assets.md)
- [Licensing and acknowledgements](docs/licensing.md)
