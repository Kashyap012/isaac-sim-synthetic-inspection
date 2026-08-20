# Dent defect material sample

This folder contains four maps for one dent material used in the thesis workflow:

- `dent_0_D.png` — albedo / diffuse
- `dent_0_N.png` — tangent-space normal
- `dent_0_R.png` — roughness
- `dent_0_M.png` — metallic

The `_D`, `_N`, and `_R` suffixes follow the naming convention expected by the included upstream NVIDIA defect extension. The metallic map is included for completeness but is not consumed by that upstream implementation without an additional code change.
