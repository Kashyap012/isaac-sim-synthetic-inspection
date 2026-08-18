"""Convert COCO bounding-box annotations into normalized YOLO labels."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def _normalize_box(box: list[float], width: int, height: int) -> tuple[float, float, float, float]:
    if width <= 0 or height <= 0:
        raise ValueError("image dimensions must be positive")
    x, y, box_width, box_height = box
    x1 = max(0.0, min(float(width), x))
    y1 = max(0.0, min(float(height), y))
    x2 = max(0.0, min(float(width), x + box_width))
    y2 = max(0.0, min(float(height), y + box_height))
    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"invalid bounding box after clipping: {box}")
    return (
        ((x1 + x2) / 2.0) / width,
        ((y1 + y2) / 2.0) / height,
        (x2 - x1) / width,
        (y2 - y1) / height,
    )


def convert_coco_to_yolo(
    coco_path: Path,
    output_dir: Path,
    category_map: dict[int, int],
) -> dict[str, int]:
    """Convert a COCO JSON file and return basic conversion statistics."""
    data = json.loads(coco_path.read_text(encoding="utf-8"))
    images = {int(item["id"]): item for item in data.get("images", [])}
    labels: dict[int, list[str]] = defaultdict(list)
    skipped = 0

    for annotation in data.get("annotations", []):
        image_id = int(annotation["image_id"])
        category_id = int(annotation["category_id"])
        if image_id not in images or category_id not in category_map:
            skipped += 1
            continue
        image = images[image_id]
        try:
            cx, cy, width, height = _normalize_box(
                list(annotation["bbox"]), int(image["width"]), int(image["height"])
            )
        except (KeyError, TypeError, ValueError):
            skipped += 1
            continue
        labels[image_id].append(
            f"{category_map[category_id]} {cx:.6f} {cy:.6f} {width:.6f} {height:.6f}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    for image_id, image in images.items():
        label_path = output_dir / f"{Path(image['file_name']).stem}.txt"
        label_path.write_text("\n".join(labels.get(image_id, [])), encoding="utf-8")

    return {
        "images": len(images),
        "annotations_written": sum(len(items) for items in labels.values()),
        "annotations_skipped": skipped,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coco", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--category-map", type=Path, required=True)
    args = parser.parse_args()
    mapping = {int(key): int(value) for key, value in json.loads(args.category_map.read_text()).items()}
    print(json.dumps(convert_coco_to_yolo(args.coco, args.output, mapping), indent=2))


if __name__ == "__main__":
    main()
