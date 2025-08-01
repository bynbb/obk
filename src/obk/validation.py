from pathlib import Path
from typing import List

from lxml import etree

from .preprocess import preprocess_text


def validate_all(prompts_dir: Path, schema_path: Path) -> List[str]:
    schema_doc = etree.parse(str(schema_path))
    schema = etree.XMLSchema(schema_doc)
    errors: List[str] = []
    for file_path in prompts_dir.rglob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        processed, _ = preprocess_text(text)
        try:
            tree = etree.fromstring(processed.encode("utf-8"))
            schema.assertValid(tree)
        except Exception as exc:
            errors.append(f"{file_path}: {exc}")
    return errors
