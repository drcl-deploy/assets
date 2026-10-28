# EgoHTR terrain crops

Fixed convex terrain for the paired ORCS G1 references in
[`l-k-r/retargeted_motions`](https://huggingface.co/datasets/l-k-r/retargeted_motions),
under `data/unitree_g1/egohtr/<clip>/sample1/`.

| Clip | Label | Convex pieces | Paired reviewed motion |
|---|---|---:|---|
| `rocky-path_s7_bzb_01__40-50s` | 03 | 360 | `0009_natural-step-v3` |
| `cliff-jump_s4_bzb_01__28-38s` | 05 | 192 | `0006_native-manifold` |

- `tile.json`: family, level, tile size, floor height, ordered meshes and scales.
- `meshes/*.obj`: precomputed collision pieces, named by SHA256.
- `provenance.json`: source crop, processing and exact descriptor hash.
- Mesh coordinates require the scale in `tile.json`; do not scale the robot too.
- These are the exact colliders used for the ORCS joint 03/05 policy. No generator,
  CoACD installation or dense scene scan is required to use them.

```python
from assets import asset_path

tile = asset_path("terrain", "egohtr", "cliff-jump_s4_bzb_01__28-38s", "tile.json")
```

## Attribution

Derived from [EgoHTR](https://huggingface.co/datasets/leggedrobotics/egohtr):
Alex Brandes and co-authors, ETH Zurich, *EgoHTR: Egocentric 4D Demonstrations of
Human Terrain Traversal* (2026), [paper](https://arxiv.org/abs/2607.13472).

These scene derivatives retain **CC-BY-4.0**, independently of the repository's
MIT code license. See [license terms](https://creativecommons.org/licenses/by/4.0/).
Modifications: scene cropping, convex decomposition and the per-crop scaling
recorded in each descriptor. Preserve this attribution when redistributing.
