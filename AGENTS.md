# Repository Guidelines for Automated Agents

This repository uses prompts to document and trace development tasks. Prompts are considered frozen by default. Automated updates to a prompt are permitted only when its ID is listed under **Prompts to Update** below. When source code changes occur—whether through Codex-driven edits or user-submitted pull requests—agents should update only the prompts specified.

## Prompts to Update

- <gsl-prompt-id>20250729T145215</gsl-prompt-id>

Agents MUST automatically add any prompt files whose ID includes today's date
(formatted as `YYYYMMDD`) to the list above. This ensures newly generated
prompts from the current day are always updated with minimal manual intervention.

## Workflow for Agents

1. Apply code changes and update the listed prompts when needed.
2. Run `python scripts/get_prompt_id.py -t UTC` to verify the prompt ID tool works and to normalize timestamps across environments.
3. Commit the changes and open a pull request describing the modifications.


### Branch Management

This repository supports a stacked branching workflow. When creating a new
branch that depends on another, make at least one commit on the new branch
before opening the next branch in the stack. This preserves the intended branch
order in tools that visualize history. Apart from this, no additional rules on
branch naming or stacking are enforced here.

