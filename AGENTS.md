# Repository Guidelines for Automated Agents

This repository uses prompts to document and trace development tasks. Prompts are considered frozen by default. Automated updates to a prompt are permitted only when its ID is listed under **Prompts to Update** below. When source code changes occur—whether through Codex-driven edits or user-submitted pull requests—agents should update only the prompts specified.

## Prompts to Update

- <gsl-prompt-id>N/A</gsl-prompt-id>

Agents MUST automatically add any prompt files whose ID includes today's date
(formatted as `YYYYMMDD`) to the list above. This ensures newly generated
prompts from the current day are always updated without manual intervention.

## Workflow for Agents

1. Apply code changes and update the listed prompts when needed.
2. Run `python scripts/get_prompt_id.py -t UTC` to verify the prompt ID tool works and to normalize timestamps across environments.
3. Commit the changes and open a pull request describing the modifications.

## Commit Tracking

Agents MUST track which commits have been documented in the prompt with ID
<gsl-prompt-id>N/A</gsl-prompt-id>. After updating the prompt to describe a commit, append
that commit hash to the **Documented Commits** list below. To discover
undocumented commits, compare the hashes in this list with `git log --pretty=%H`.
Only commits not present in the list require prompt updates. In addition,
agents **MUST** limit their search to commits whose commit date matches the
current day. The search should be performed using UTC to avoid timezone
discrepancies when the agent runs from different regions. This prevents
documenting stale changes when the agent runs on a later date.

When scanning for same-day prompt files, list those prompt IDs alongside the
commit hashes they document. This keeps a direct record of which prompt was
updated for each commit.

### Branch Management

This repository supports a stacked branching workflow. When creating a new
branch that depends on another, make at least one commit on the new branch
before opening the next branch in the stack. This preserves the intended branch
order in tools that visualize history. Apart from this, no additional rules on
branch naming or stacking are enforced here.

## Documented Commits

- ipsum lorem
- 4ba222d7359c3ca373253bef5445def90f75ed4b
- 00caa51c44fd72f5dead2da8c316d725a8fdc85f
- f35652058bed6794dd00d6432f2ae81a6980ff07
- ea1a04aef0e11407db1d94d0f1692ea0bfa2848b
- bea7eeef689a3ac7863217007d71fc0fb4a230c4
