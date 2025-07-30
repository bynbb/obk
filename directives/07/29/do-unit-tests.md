## Unified Prompt-Driven Unit Tests Task

**Objective:**
Sequentially implement and test features in `obk` by reproducing behaviors from the reference article described below. Each step builds on the previous, and all deliverables are part of a single, unified change set.

---

### 1. Repository Analysis

1.1. Analyze the `obk` repository to understand its structure and current capabilities.

---

### 2. Reference Article & Feature Extraction

2.1. Review the article *\articles\bullet-proof-pytest-setup.md - Bulletproof Pytest Setup*.
2.2. Identify which functionalities, patterns, or CLI behaviors need to be reproduced in `obk`. (List them explicitly if possible, e.g. command help, entry point, run-from-anywhere, etc.)

---

### 3. Manual Testing & Iteration

3.1. Review the article *one-line-manual-tests.md* for best practices on manual test writing.
3.2. In the `20250729T185556-0400` prompt, within the `<gsl-tdd>` section, write a set of single-line manual tests that fully validate the features being implemented. Each test must be wrapped in a `<gsl-test>` element.

* Cover all necessary behaviors and edge cases for the required scope.
* 3.3. Use these manual tests to guide your development—iterating on implementation until all pass and the build meets requirements.

---

### 4. Modification Scope Constraint

**4.1. File Modification Policy:**
The agent **MUST NOT** make changes to any files except for those that are recognized as part of a standard Python project. Permitted file types and paths include:

* All files with the explicit Python extension:

  * `*.py`
* Python project configuration and metadata files:

  * `pyproject.toml`
  * `setup.py`
  * `setup.cfg`
  * `requirements.txt`
  * `MANIFEST.in`
* Test configuration and runner files:

  * `pytest.ini`
  * `tox.ini`
  * `.coveragerc`
* Standard documentation and ignore files:

  * `README.md`
  * `.gitignore`
  * `.gitattributes`
* Project-level scripts related to building, installing, or testing:

  * Any files within a `/scripts/` directory, with extensions listed above (e.g., `/scripts/*.py`).

**4.2. Prohibited Modifications:**
The agent MUST NOT create, modify, or delete any files or file types not explicitly listed above.

* Examples of prohibited files:

  * Arbitrary `*.txt` files except for `requirements.txt`
  * Binary files (e.g., `*.exe`, `*.dll`)
  * Non-Python source files (e.g., `*.js`, `*.ts`, `*.java`, etc.)
  * User or OS-specific files (e.g., `.DS_Store`, `Thumbs.db`)
  * Any unlisted files or directories

**4.3. Extension for Project-Specific Files:**
If the project relies on additional, non-standard files that are required for its correct operation, such files must be explicitly listed and justified in the relevant prompt or specification section.

**4.4. Frozen Modification Rule with Single Additive Exception**

The restrictions in Section 4.2 are **frozen** and MUST NOT be relaxed or altered in any future prompt, specification, or agent directive—**except** for the following exception:

* The agent MAY add content to the file named `20250729T185556-0400.md`, as required for prompt-driven or traceability-related development.

  * **The agent MUST NOT** modify or delete existing content in `20250729T185556-0400.md`—only appending or inserting new content is allowed.
  * All additions to `20250729T185556-0400.md` must comply with project conventions and traceability requirements.

---

**Instructions:**

* Complete each step before proceeding to the next.
* Treat all outputs (implementation and tests) as part of a single, cohesive change set.

---

### Standardized Placeholders

* `obk`: The repository under development
* *\articles\bullet-proof-pytest-setup.md - Bulletproof Pytest Setup*: Article outlining the behaviors/features to reproduce
* `one-line-manual-tests.md`: Article guiding manual test design (optional, but recommended for process discipline)
* `20250729T185556-0400`: Prompt file where tests will be written
