#!/usr/bin/env python3
"""
update_agents_md.py

Update all <gsl-prompt-id> elements NOT inside code fences to a user-provided value.

- Prompts the user for the new prompt ID (does NOT generate or suggest one).
- Ignores code blocks fenced by single or triple backticks.
- Cross-platform, works on Windows, macOS, and Linux.
- Place this script in 'scripts/', run from project root or scripts directory.

Usage:
    python scripts/update_agents_md.py
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
AGENTS_MD_PATH = os.path.join(ROOT_DIR, 'AGENTS.md')

def split_fenced_blocks(text):
    """
    Splits the input text into blocks: [("outside", ...), ("code", ...), ...]
    Where "outside" is content not in a code fence, and "code" is content inside.
    """
    pattern = re.compile(
        r'(`{3,}|`)([\s\S]*?)(\1)',
        re.MULTILINE
    )
    last_idx = 0
    blocks = []
    for m in pattern.finditer(text):
        # Outside code fence
        if m.start() > last_idx:
            blocks.append(("outside", text[last_idx:m.start()]))
        # Inside code fence
        blocks.append(("code", m.group(0)))
        last_idx = m.end()
    # Any trailing text after the last code block
    if last_idx < len(text):
        blocks.append(("outside", text[last_idx:]))
    return blocks

def update_gsl_prompt_id_outside_code(text, new_id):
    """Replace all <gsl-prompt-id>...</gsl-prompt-id> tags with new_id, except inside code fences."""
    blocks = split_fenced_blocks(text)
    updated_blocks = []
    for typ, block in blocks:
        if typ == "outside":
            # Replace all <gsl-prompt-id>...</gsl-prompt-id>
            block = re.sub(
                r'<gsl-prompt-id>.*?</gsl-prompt-id>',
                f'<gsl-prompt-id>{new_id}</gsl-prompt-id>',
                block,
                flags=re.DOTALL
            )
        updated_blocks.append(block)
    return "".join(updated_blocks)

if __name__ == "__main__":
    while True:
        prompt_id = input("Enter the new <gsl-prompt-id>: ").strip()
        if prompt_id:
            break
        print("Prompt ID cannot be empty. Please enter a valid prompt ID.")

    with open(AGENTS_MD_PATH, encoding='utf-8') as f:
        content = f.read()
    new_content = update_gsl_prompt_id_outside_code(content, prompt_id)
    if new_content != content:
        with open(AGENTS_MD_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated all <gsl-prompt-id> elements outside code fences to: {prompt_id} in global `AGENTS.md` file.")
    else:
        print("No updates made. All prompt IDs already current.")
