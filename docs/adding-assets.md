# Add an asset

1. Add the model below `src/assets/<entity>/`.
2. Keep mesh references relative within tracked robot models.
3. Add object metadata and source meshes to an object group.
4. Run `assets generate`.
5. Verify XML/URDF references and record upstream provenance.

Generated URDF/XML files stay untracked. Commit reusable convex decomposition
parts when adding a new object.
