# Synthetic Data for Industrial Quality Inspection

> Public technical reconstruction of an approved master's thesis project. Proprietary source code, CAD assets, datasets, and trained weights are not included.

This case study documents an end-to-end workflow for generating synthetic defect images in NVIDIA Isaac Sim / Omniverse, converting annotations, training object detectors, and evaluating sim-to-real behavior on real inspection images.

![Workflow](docs/images/workflow.png)

## Problem

Industrial defect datasets are expensive and imbalanced: rare defects are difficult to capture, labeling is slow, and variations in material, lighting, viewpoint, and background create a substantial domain gap. The project addressed this with controllable synthetic-data generation and systematic model evaluation.

## Architecture

```mermaid
flowchart LR
    A[CAD / OpenUSD asset] --> B[Isaac Sim scene]
    B --> C[Defect texture generation]
    C --> D[Domain randomization]
    D --> E[RGB + annotations]
    E --> F[COCO to YOLO conversion]
    F --> G[YOLO / DETR training]
    G --> H[Real-image evaluation]
```

## Public implementation

The repository includes a dependency-light COCO-to-YOLO annotation converter that can be tested without Isaac Sim. It validates category mappings, clips boxes to image bounds, and writes normalized YOLO labels.

```bash
python -m synthetic_inspection.annotation_converter \
  --coco annotations.json \
  --output labels \
  --category-map category_map.json
```

## Domain-randomization design

The example configuration in [`configs/domain_randomization.yaml`](configs/domain_randomization.yaml) captures the project dimensions without exposing proprietary assets:

- lighting intensity, direction, and color temperature
- camera pose, focal length, and distance
- surface albedo, roughness, and normal-map variation
- defect position, scale, rotation, texture, and severity
- background and distractor variation

## Approved project evidence

### Synthetic samples

![Synthetic samples](docs/images/synthetic-samples.png)

### Real-image evaluation examples

![Real-image results](docs/images/real-image-results.png)

The thesis project trained and evaluated YOLO and DETR models and reported 94% accuracy on real-world inspection images. The public repository does not include the proprietary dataset, so this number is documented as a project result rather than claimed as reproducible from this repository alone.

## Limitations

- This release is a public reconstruction, not the internal production repository.
- CAD data, inspection images, trained weights, and company-specific pipeline code are excluded.
- Isaac Sim APIs evolve; integration code should be pinned to the chosen simulator release.
- The included tests validate annotation conversion only, not rendering or model training.

## Run the tests

```bash
python -m pytest
```

## License and attribution

Original public reconstruction code is MIT licensed. Thesis visuals are published with external approval. NVIDIA Isaac Sim and Omniverse remain subject to their respective NVIDIA licenses; no NVIDIA source code is redistributed here.
