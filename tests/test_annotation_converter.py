import json
from pathlib import Path

from synthetic_inspection.annotation_converter import convert_coco_to_yolo


def test_conversion_clips_boxes_and_skips_unknown_categories(tmp_path: Path) -> None:
    source = tmp_path / "annotations.json"
    source.write_text(
        json.dumps(
            {
                "images": [{"id": 1, "file_name": "part.png", "width": 100, "height": 50}],
                "annotations": [
                    {"image_id": 1, "category_id": 7, "bbox": [-10, 5, 30, 20]},
                    {"image_id": 1, "category_id": 99, "bbox": [10, 10, 5, 5]},
                ],
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "labels"
    stats = convert_coco_to_yolo(source, output, {7: 0})
    assert stats == {"images": 1, "annotations_written": 1, "annotations_skipped": 1}
    assert (output / "part.txt").read_text() == "0 0.100000 0.300000 0.200000 0.400000"
