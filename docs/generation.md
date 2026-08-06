# Generate object models

Generate all per-machine URDF and MuJoCo files:

```bash
assets generate
```

Common options:

```bash
assets generate --object trashcan
assets generate --no-decompose
assets generate --force
assets generate --output-root /path/to/generated-assets
assets generate --in-place
```

Generated files contain absolute paths and are not tracked. Existing committed
convex parts are reused; `coacd` is needed only for a new decomposition or
`--force`.
