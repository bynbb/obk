# AGENTS.md

## Overview

This document defines agent-facing policies, the GSL data dictionary, automation boundaries, file organization rules, conventions, and a comprehensive glossary for the OBK repository.  
It is the authoritative source for how agents (including Codex) and humans interact with repository artifacts, which GSL elements are in use, and how prompt/automation files are structured and validated.

* * *

| Element               | Description                                                  | Typical Content                                                         | Attributes                                        | Type         |
| --------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------- | ------------------------------------------------- | ------------ |
| `<gsl-prompt>`        | Root element for the prompt document. Contains all sections. | All other elements                                                      | `id` (required), `type`, default: feat) | **Non-Text** |
| `<gsl-description>`   | Optional summary or context (global).                        | Text                                                                    | None                                              | **Text**     |
| `<gsl-header>`        | Human-friendly title, often a Markdown header.               | One line of text/Markdown header                                        | None                                              | **Text**     |
| `<gsl-block>`         | Main container for content sections.                         | Other GSL elements                                                      | None                                              | **Non-Text** |
| `<gsl-purpose>`       | Purpose/intention for the prompt/task.                       | Freeform text/Markdown                                                  | None                                              | **Text**     |
| `<gsl-inputs>`        | Required files, resources, or dependencies.                  | `<gsl-label>`, `<gsl-title>`, `<gsl-description>`, `<gsl-value>`        | None                                              | **Non-Text** |
| `<gsl-outputs>`       | Expected deliverables/results.                               | `<gsl-label>`, `<gsl-title>`, `<gsl-description>`, `<gsl-value>`        | None                                              | **Non-Text** |
| `<gsl-workflows>`     | Step-by-step procedures or command guides.                   | `<gsl-label>`, `<gsl-title>`, `<gsl-description>`, `<gsl-value>`        | None                                              | **Non-Text** |
| `<gsl-tdd>`           | Section for TDD/tests.                                       | `<gsl-label>`, `<gsl-title>`, `<gsl-description>`, `<gsl-test>`         | None                                              | **Non-Text** |
| `<gsl-test>`          | Single test case definition.                                 | Description, code, CLI command                                          | `id` (required, unique)                           | **Text**     |
| `<gsl-document-spec>` | Maintenance/update rules for the prompt doc.                 | `<gsl-label>`, `<gsl-title>`, `<gsl-description>`, `<gsl-value>`        | None                                              | **Non-Text** |
| `<gsl-surgery>`       | Documents a major/breaking/removal/change event.             | `<gsl-when>`, `<gsl-what>`, `<gsl-why>`, `<gsl-impact>`, `<gsl-action>` | None                                              | **Non-Text** |
| `<gsl-when>`          | When a change occurred (non-text).                           | `<gsl-label>`, `<gsl-title>`, `<gsl-value>`                             | None                                              | **Non-Text** |
| `<gsl-what>`          | What was changed/removed (non-text).                         | `<gsl-label>`, `<gsl-title>`, `<gsl-value>`                             | None                                              | **Non-Text** |
| `<gsl-why>`           | Why the change occurred (non-text).                          | `<gsl-label>`, `<gsl-title>`, `<gsl-value>`                             | None                                              | **Non-Text** |
| `<gsl-impact>`        | Impact of change (non-text).                                 | `<gsl-label>`, `<gsl-title>`, `<gsl-value>`                             | None                                              | **Non-Text** |
| `<gsl-action>`        | Follow-up/mitigation (non-text).                             | `<gsl-label>`, `<gsl-title>`, `<gsl-value>`                             | None                                              | **Non-Text** |
| `<gsl-label>`         | UI-style field label (global).                               | Text                                                                    | None                                              | **Text**     |
| `<gsl-title>`         | Section/element headline (global).                           | Text                                                                    | None                                              | **Text**     |
| `<gsl-value>`         | Value of a non-text element (global).                        | Text, date, ID, etc.                                                    | None                                              | **Text**     |


_(Extend table as new elements/attributes are added)_

* * *

## 2. Core Conventions & File Organization

### 2.1 Deterministic File Paths

* Prompt files are stored under `prompts/YYYY/MM/DD/`, using UTC or agreed timezone.
    
* Filenames are trace IDs or timestamps (e.g., `20250803T120000+0000.md`).
    

### 2.2 Mixing Markdown with GSL

* All GSL element tags must be **left-justified** (no indentation).
    
* There must be an **empty line below any GSL opening tag** if the next line is text or Markdown.
    

### 2.3 Non-Text Elements

* The following are **non-text elements**—they must **never** contain direct text.  
    All content must be in a child element such as `<gsl-description>`, `<gsl-value>`, `<gsl-title>`, or `<gsl-label>`:
    
    * `<gsl-block>`
        
    * `<gsl-inputs>`
        
    * `<gsl-outputs>`
        
    * `<gsl-workflows>`
        
    * `<gsl-tdd>`
        
    * `<gsl-test>`
        
    * `<gsl-document-spec>`
        
    * `<gsl-purpose>`
        
    * `<gsl-surgery>`
        
    * `<gsl-when>`
        
    * `<gsl-what>`
        
    * `<gsl-why>`
        
    * `<gsl-impact>`
        
    * `<gsl-action>`
        
* **Text-only elements** (such as `<gsl-description>`) are for direct text/Markdown and do not require wrapping.
    

### 2.4 Global Elements

* `<gsl-label>`, `<gsl-title>`, `<gsl-description>` and `<gsl-value>` are **global elements**.  
    They may appear 0 or 1 time each as first children in any non-global, non-text element (in any order).
    

### 2.5 Trace IDs

* Prompts and select sub-elements require unique `trace ID`s (`YYYYMMDDTHHMMSS±ZZZZ`).
    
* IDs are validated for uniqueness and format.
    

### 2.6 Validation & Harmonization

* Validation checks for schema compliance, required attributes, structure, and forbidden direct text.
    
* Harmonization functions may auto-correct spacing and justification.
    

* * *

## 3. Agent Automation Guidance

* **Editable Sections:**  
    Agents may edit, update, or append to sections marked as agent-editable or by repo policy.
    
* **Human-only Sections:**  
    Elements like `<gsl-document-spec>` or major specs are reserved for human maintainers.
    
* **Obsoleting Elements:**  
    To mark an element, process, or convention as obsolete, update relevant docs (data dictionary, prompt, article) using **obsoleted** (in comments, a `status="obsolete"` attribute, or glossary note). Obsoleting is a documentation/policy action and does not require structural markup.
    
* **Surgical Changes (“Surgery”):**  
    Major structure/data/workflow changes should be recorded using `<gsl-surgery>`, whether or not obsoleting is involved. Surgery is a structural/historical record, not a policy change.
    
* **Distinction:**  
    _Obsoleting_ and _surgery_ may overlap but are distinct—obsoleting is status/policy, surgery is structural/historical.
    
* **New elements/extensions** must be added here and reviewed before agent/automation use.
    

* * *

## 4. Glossary of Key Terms

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
| **agent** | Any automation, such as Codex, that interprets, edits, or maintains repository artifacts based on GSL documents and this AGENTS.md. |
| **obsoleted** | A status assigned to elements, attributes, or processes that are no longer recommended for use, but may remain in the codebase or documentation for historical reference. |
| **surgery** | A major structural change, removal, or replacement—recorded using the `<gsl-surgery>` element. Surgery documents what, when, why, and the impact/action of the change. |
| **global elements** | Elements like `<gsl-label>`, `<gsl-title>`, and `<gsl-value>`, which may be used as first children in most non-text, non-global elements for labeling, titling, or providing values. |
| **non-text elements** | GSL elements that must not contain direct text content; instead, all content must be in child elements such as `<gsl-value>`, `<gsl-title>`, or `<gsl-label>`. See section 2.3 for a complete list. |
| **text-only elements** | GSL elements intended for direct text or Markdown content, such as `<gsl-description>`. |

* * *

## 5. Living Document Policy

* AGENTS.md must be kept current with any schema, convention, or process changes—before updating code or automation.
    
* Any discrepancy between AGENTS.md and code is considered a bug and should be resolved promptly.
    

* * *