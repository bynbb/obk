from pathlib import Path
from typing import List, Tuple
from lxml import etree
from .preprocess import preprocess_text


def validate_all(prompts_dir: Path, schema_path: Path) -> Tuple[List[str], int, int]:
    """
    Validates all prompt files under prompts_dir using the given XSD schema.
    Returns a tuple: (list of error messages, count_passed, count_failed)
    """
    schema_doc = etree.parse(str(schema_path.resolve()))
    schema = etree.XMLSchema(schema_doc)

    errors: List[str] = []
    count_passed = 0
    count_failed = 0

    prompts_dir = prompts_dir.resolve()  # absolute path

    for file_path in prompts_dir.rglob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        processed, _ = preprocess_text(text)
        try:
            tree = etree.fromstring(processed.encode("utf-8"))
            schema.assertValid(tree)
            count_passed += 1
        except Exception as exc:
            errors.append(f"{file_path}: {exc}")
            count_failed += 1

    return errors, count_passed, count_failed
