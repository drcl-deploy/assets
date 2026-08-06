# Python imports

Base imports do not require Isaac Lab:

```python
from assets.paths import asset_path
from assets.g1 import constants

model = asset_path("g1", "g1_bm.urdf")
```

Import simulator configuration explicitly:

```python
from assets.g1.isaaclab import G1_BM_CFG
from assets.hector_v2.feet.isaaclab import IMPLICIT_WO_COUPLING_CFG
```
