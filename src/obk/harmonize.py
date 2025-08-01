from typing import List, Tuple


def harmonize_text(text: str) -> Tuple[str, List[str]]:
    lines = text.splitlines()
    actions: List[str] = []
    i = 0
    in_code = False
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```") or line.lstrip().startswith("~~~"):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            i += 1
            continue
        stripped = line.lstrip()
        if stripped.startswith("<") and line != stripped:
            lines[i] = stripped
            actions.append(f"Removed indentation for XML element on line {i + 1}")
        i += 1
    result = "\n".join(lines)
    if text.endswith("\n"):
        result += "\n"
    return result, actions
