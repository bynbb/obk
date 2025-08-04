# Grit Structured Language (GSL): Overview and Reference

* * *

## Introduction

The **Grit Structured Language (GSL)** provides a rigorous, flexible foundation for structured collaboration in development projects.  
GSL defines a set of XML-based elements, embedded in Markdown, that capture requirements, context, workflows, and validation logic—creating a “shared language” for teams, tools, and agents.

GSL enforces clarity, process, and validation _when you want it_, and stays out of your way when you don’t. It is extensible by design, so new features and workflows can be layered on as needs evolve.

_This document describes GSL as it is practiced today. New conventions and elements may be introduced in future extensions—see project documentation for updates._

* * *

## High-Level Purpose

At its core, GSL solves a fundamental challenge in software and project development: aligning language and process between people and roles with different backgrounds, skills, and vocabularies. In any collaborative effort—especially in technology—the biggest obstacles often arise not from technical limitations, but from misunderstanding and inconsistency in how requirements, workflows, and goals are described.

GSL addresses this by establishing an **agreed-upon, machine-validated language** for capturing requirements, processes, and rules. By encoding these agreements in a shared, structured syntax (enforced by schemas and validation tools), GSL provides a neutral ground where developers, management, and automation can “speak the same language.”

This idea is well-established in software engineering. The concept of a shared, universal vocabulary is a cornerstone of methodologies like **Domain-Driven Design (DDD)**, where the goal is to create a “ubiquitous language”—a consistent set of terms and structures used by everyone involved in a project. GSL brings this spirit into a formal, enforceable, and extensible machine syntax.

**The key insight:**  
GSL does not force teams to work a certain way, but rather offers the _option_ of shared language and process. Anyone is free to ignore these rules—but if they do, they lose the ability to validate, automate, and trust their documents within the OBK ecosystem.

**In summary:**  
GSL makes language and process explicit, extensible, and enforceable. It defines what is “in-bounds” and what is not, so everyone who chooses to participate in the shared agreement can build, communicate, and automate with less confusion and more trust.

* * *

## Enabling Synergy Between Natural and Structured Language

A major benefit of GSL is that it **combines natural language with parseable, structured language**—directly in the same document. This unified approach provides two powerful capabilities:

1. **Leverage LLMs for natural language understanding and generation:**  
    Prompts, descriptions, and specifications written in plain language can be interpreted, summarized, or expanded by large language models (LLMs), unlocking creativity and rapid prototyping.
    
2. **Enable precise, auditable processing with traditional programming:**  
    The structured XML elements provide machine-readable context, constraints, and metadata, which can be reliably validated, queried, or transformed using standard programming languages and tools.
    

**The true power comes from combining both, side by side, in context.**  
An LLM working with a GSL document can use its natural language skills to interpret instructions, ask clarifying questions, or suggest changes, while the structured elements make it easy to extract tasks, validate rules, or run data pipelines—**without losing track of the original context.**

### Example

Suppose a prompt describes a new feature:

```xml
<gsl-prompt id="20250804T100000+0000">
<gsl-header>  
  
# Integrate Payment Gateway</gsl-header>
<gsl-block>
<gsl-description>

The goal is to support credit card and ACH payments for all users. 
We must comply with PCI DSS and ensure all transactions are logged.
</gsl-description>
<gsl-inputs>

  | Input         | Notes                          |
  |-------------- |-------------------------------|
  | payment_api   | API keys must be securely stored |
  | user_accounts | Must be verified before payment |
</gsl-inputs>

<!-- other elements -->
</gsl-block>
</gsl-prompt>
```

* The **LLM** can interpret the goal, rationale, and requirements, even answering questions or rewriting descriptions.
    
* At the same time, **programmatic tools** can parse `<gsl-inputs>` for dependencies, or enforce compliance checks.
    
* Both operate on the same document—**no context is lost or duplicated**.
    

**In summary:**  
GSL enables a future where LLM-driven reasoning and classical data processing operate in tandem, each augmenting the other. This dual approach makes projects more expressive, more automatable, and more reliable than relying on either language or structure alone.

* * *

## Development Workflow Summary

GSL supports structured, repeatable workflows for both feature development and release management—while remaining intentionally flexible and non-prescriptive. The “out-of-the-box” workflows provide guides for contributors and reviewers, especially those new to the OBK ecosystem, but **there are no built-in enforcement mechanisms** for process adherence. The only consequence for not following a workflow is that the artifacts (such as prompt files or documentation) may be missing, incomplete, or out-of-date in the repository. This visibility, rather than strict validation, encourages best practices without restricting creative or urgent work.

**The two primary documented workflows are:**

1. **Feature Workflow:**  
    A step-by-step process for designing, developing, testing, and integrating new features, starting with a feature article and progressing through prompt-driven task definition, Codex automation, and manual/automated testing before merging to main.
    
2. **Release Workflow:**  
    A controlled process for preparing, validating, and deploying official releases to PyPI, emphasizing reviewer approval, version synchronization, and post-release documentation updates.
    

These workflows are intended as **standards against which practices can be compared**, not as rigid rules. They can be shortened for quick fixes, adapted for unique cases, or even bypassed if the situation demands. Any missing or skipped steps are visible in the repository’s history, making process adherence (or its absence) part of the project’s transparent record. Management or maintainers can choose to enforce stricter rules by extending GSL, but out-of-the-box, the workflows remain guides—**not constraints**.

**In summary:**  
GSL supports and documents flexible, best-practice workflows that help onboard contributors, clarify expectations, and standardize project history, all without imposing hard validation or limiting creativity.

* * *

## GSL Elements and Attributes

The GSL schema defines a structured, extensible set of XML elements—encapsulating Markdown—that capture project context, requirements, workflows, and validation logic. Each element has a clear, documented purpose.  
Here are the core elements and attributes:

### GSL Elements Table

| Element | Description | Typical Content | Attributes |
| --- | --- | --- | --- |
| `<gsl-prompt>` | Root element for the prompt document. Identifies and contains all sections. | All other elements | `id` (required) |
| `<gsl-description>` | Optional text summary or contextual description. | Freeform text or Markdown comment | None |
| `<gsl-header>` | Human-friendly prompt/document title (often Markdown header). | Text, usually one top-level header | None |
| `<gsl-block>` | Strictly ordered group of all main content sections. | See below | None |
| `<gsl-purpose>` | Section describing the purpose or intent of the prompt/task. | Freeform text/Markdown | None |
| `<gsl-inputs>` | Lists all required files, resources, or dependencies for the task. | Markdown table/list | None |
| `<gsl-outputs>` | Defines deliverables or results expected from the task. | Markdown list/text | None |
| `<gsl-workflows>` | Describes step-by-step procedures, manual test scripts, or command guides. | Freeform/Markdown, often step lists | None |
| `<gsl-tdd>` | Test-driven development section. Contains tests for the prompt. | `<gsl-description>`, `<gsl-test>` | None |
| `<gsl-test>` | Describes a single test case. | Description, code block, CLI command | `id` (required, unique) |
| `<gsl-document-spec>` | Describes how the prompt document itself should be maintained or updated. | Section rules, numbering, agent policy | None |

### Key Attributes

* `id` (on `<gsl-prompt>`): Uniquely identifies the prompt file, usually a timestamp string (e.g., `20250802T024329+0000`)
    
* `id` (on `<gsl-test>`): Uniquely identifies the test case within the prompt (e.g., `T1`, `T2`)
    

### Section Order (inside `<gsl-block>`)

Elements inside `<gsl-block>` are strictly ordered as follows:

1. `<gsl-purpose>`
    
2. `<gsl-inputs>`
    
3. `<gsl-outputs>`
    
4. `<gsl-workflows>`
    
5. `<gsl-tdd>`
    
6. `<gsl-document-spec>`
    

* * *

### Example GSL Prompt

```xml
<gsl-prompt id="20250802T024329+0000">
<gsl-description>
<!-- Self-contained prompt and spec for OBK/Codex agent work. -->
</gsl-description>
<gsl-header>

# UTC-Synchronized "Today" Folder Logic for OBK CLI
</gsl-header>
<gsl-block>
<gsl-purpose>

Update the `obk` CLI so that all commands referencing "today"... (see full file for details)
</gsl-purpose>
<gsl-inputs>

| Input       | Notes |
|-------------|-------|
| ...         | ...   |
</gsl-inputs>
<gsl-outputs>

- Refactored folder/date logic for “today” in `cli.py`
- CLI commands ... (etc)
</gsl-outputs>
<gsl-workflows>

## 4. Workflows
Manual Acceptance Test...
</gsl-workflows>
<gsl-tdd>
<gsl-description>
<!-- Manual tests section -->
</gsl-description>
<gsl-test id="T1">

- T1: Manual test for default UTC “today” folder selection...
</gsl-test>
<!-- More <gsl-test> elements -->
</gsl-tdd>
<gsl-document-spec>

## 6. Document Specification
<!-- Conventions and agent update rules -->
</gsl-document-spec>
</gsl-block>
</gsl-prompt>
```

* * *

## Conventions and Practices

GSL’s power comes not just from its schema, but from a set of shared conventions—some enforced by tooling, others by project discipline:

### 1. Deterministic Date File Paths

Prompt file locations are deterministic: each prompt file lives in a path structured as `prompts/YYYY/MM/DD/`, based on the current date and (optionally) timezone. This approach ensures reproducibility, consistency, and supports automation.

### 2. Trace ID Format and Validation

Every prompt (and some elements like tests) is uniquely identified. The `id` attribute uses a strict, time-based format: `YYYYMMDDTHHMMSS±ZZZZ`. IDs are always validated for correctness.

### 3. Markdown Harmonization Rules

To make GSL XML elements and Markdown coexist cleanly in `.md` files, two harmonization rules are critical:

1. **Left-Justify GSL Elements:** All `<gsl-*>` tags must be at the start of the line (no indentation). This is a manual best practice.
    
2. **Blank Line After Opening Tag:** There should always be an empty line immediately following the opening tag of any GSL element. This is automatically enforced and corrected by the `harmonize` functions.
    

### 4. No Mixed Content (XML Rule)

Where an element contains child elements, it should not also include free text directly. Instead, free text is wrapped in `<gsl-description>` as needed.

### 5. Validation Boundaries

Validation focuses on XML structure. The OBK CLI’s validation functions are mainly concerned with XML validity, correct element/attribute usage, and required/optional section presence.

### 6. Update and Edit Policies

Some document sections are designated as safe for agent (Codex) edits—like workflows and tests—while others (like specifications) are reserved for human maintainers. These policies are documented within the prompt files themselves (see `<gsl-document-spec>`).

* * *

## Term Glossary

| Term | Definition |
| --- | --- |
| **article** | A Markdown document (often in `articles/`) describing a new feature, bug, process, or policy. Usually serves as the narrative basis for new work or discussion. |
| **prompt** | The core structured document (with root `<gsl-prompt>`) that defines the context, requirements, and validation logic for a development or automation task. |
| **task** | An actionable, trackable unit of work (sometimes mapped to a prompt or a Codex job). Can be either ad hoc (feature, bugfix) or maintenance (refactor, docs, etc.). |
| **Codex** | OpenAI’s advanced code-generation and automation product, integrated into ChatGPT since May 2025. In GSL, Codex agents interpret, generate, and automate code and documentation based on prompts, tasks, and directives. |
| **conversation** | A sequence of user and agent interactions, typically from a chat session; conversations can be saved, exported, or reintroduced for continuity. |
| **chat session** | A live, interactive communication window (e.g., with Codex, OBK, or ChatGPT), where one or more conversations may take place. |
| **directive** | An instruction, rule, or command. Directives may appear in prompts, tasks, or specifications; sometimes specification-like (rule), sometimes imperative (do this). Only tasks and prompts are formally tracked as artifacts. |
| **harmonization** | The process of rewriting or formatting prompt files so their structure, whitespace, and tag layout match GSL conventions, ensuring consistency and parseability. |
| **GSL document** | A Markdown file combining custom GSL XML elements and Markdown prose. GSL documents are both human-readable and machine-parseable, and can be rendered as HTML. |
| **extended GSL** | New or planned additions to GSL, such as `<gsl-label>`, `<gsl-title>`, `<gsl-surgery>`, or the `type` attribute. These features may be adopted by teams as needs arise, expanding the capabilities of GSL while maintaining compatibility. |
| **obsoleting** | The act of formally marking a GSL element, prompt, workflow, or convention as no longer recommended or in active use, often in favor of a newer or extended alternative. Obsoleted items remain for historical reference and backward compatibility. |
| **feature workflow** | The recommended step-by-step process for adding new features, from writing an article and a prompt, through Codex-driven development, to testing and review. |
| **release workflow** | The recommended process for preparing, reviewing, and deploying a new release, including all validation, documentation, and post-release updates. |
| **deterministic date file path** | The strict convention for prompt file storage: `prompts/YYYY/MM/DD/`, ensuring reproducibility and automation compatibility. |
| **trace ID** | A unique, time-based identifier for each prompt file and some elements, generated as `YYYYMMDDTHHMMSS±ZZZZ` (see `trace_id.py`). Used for tracking and validation. |

* * *

## Integration Points and Use Cases

### Integration Points

* **OBK CLI:**  
    GSL prompt files are validated, harmonized, and manipulated using OBK’s command-line interface (`cli.py`). OBK commands like `validate-all`, `harmonize-today`, and `trace-id` operate directly on GSL files, leveraging both their XML structure and deterministic paths.
    
* **Codex Agents:**  
    Codex interprets GSL prompt files as input for generating, updating, or validating code, tests, and documentation. GSL’s strict structure enables agents to extract requirements, constraints, and workflow steps reliably.
    
* **Validation & Automation:**  
    Automated validation functions enforce GSL structure (per the XSD), check IDs, and support repeatable, auditable workflows. Harmonization tools ensure Markdown and GSL syntax coexist predictably.
    

* * *

### Typical Use Cases

**1. Authoring a New Feature Prompt**

* A contributor drafts an “article” explaining a new feature.
    
* Using the template, they create a GSL prompt file (`<gsl-prompt>`) in the date-based folder, filling out purpose, inputs, outputs, and test sections.
    
* Manual and Codex-driven tests are added in `<gsl-tdd>`, and the prompt is validated via OBK before development proceeds.
    

**2. Release Preparation and Validation**

* Before deploying, maintainers run `validate-all` and `harmonize-all` to ensure all prompts are up to date and meet project standards.
    
* The CLI’s validation catches missing or misformatted prompts, preventing incomplete releases.
    
* After deployment, version and changelog updates are recorded as new prompts, preserving history.
    

**3. Task and Workflow Automation**

* Agents can scan the prompt directory to identify incomplete, stale, or missing prompts by date or type.
    
* Routine maintenance tasks (like code formatting or dependency checks) are triggered by agent-driven prompts referencing the relevant GSL files.
    

* * *

_GSL is continuously evolving. New elements and conventions may be introduced in future extensions, expanding its capabilities while maintaining compatibility with the established structure and principles described here._

* * *