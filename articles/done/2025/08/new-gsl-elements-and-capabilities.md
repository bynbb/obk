# New GSL Elements and Capabilities

## Introduction

The Grit Structured Language (GSL) continues to evolve, enabling teams and automation agents to collaborate with even greater clarity, flexibility, and auditability. This article introduces the latest extensions to GSL: new XML elements, new attribute capabilities, and updated conventions that address common pain points from earlier versions. These changes expand what can be expressed and tracked in GSL.

Whether you’re a human contributor, a Codex agent, or a project maintainer, understanding these new elements and capabilities will help you take full advantage of GSL’s evolving power.

---

## Why Extend GSL?

As projects mature, the needs of contributors and automation agents grow more sophisticated. The original GSL schema provided structure, repeatability, and machine validation, but several limitations became clear over time:

* It lacked a formal way to capture UI-like labels, titles, or fine-grained metadata.
* There was no standard attribute for prompt categorization or type.
* There was no mechanism for transparently documenting major changes or removals (“surgery”) to prompts or sections.
* The line between free text, section summaries, and machine-parseable elements was often blurred, leading to ambiguity or awkward formatting.

To address these challenges—and to anticipate future ones—GSL now supports a set of **new elements and conventions**.

---

## New Global Elements: `<gsl-label>`, `<gsl-title>`, and `<gsl-value>`

### Purpose and Usage

GSL introduces three universal elements—**global elements**—that can be used as the first children of almost any non-text, non-global element to provide richer structure and display semantics.

#### `<gsl-label>`

* **Definition:** Used to enclose a human-facing, UI-style label for an element, such as “Title”, “Description”, “Name”, etc. Think of how a web form label appears above an input field. This is for human readability, not for tags or automation.
* **Cardinality:** 0 or 1 per parent element.

#### `<gsl-title>`

* **Definition:** Used to give a short, concise, section-specific headline or identifier.
* **Cardinality:** 0 or 1 per parent element.

#### `<gsl-value>`

* **Definition:** Used to enclose the value of a non-text element when that value is a single piece of data and there is no more specific child element for it. Use this when an element’s content is not direct text, but needs structure (e.g., date, identifier, etc).
* **Cardinality:** 0 or 1 per parent element.

#### Example

```xml
    <gsl-when>
    <gsl-title>
        
    #### When
    </gsl-title>
    <gsl-value>
        
    2025-08-01
    </gsl-value>
    </gsl-when>
```

* Here, `<gsl-title>` provides a Markdown-renderable title for the “when” section, and `<gsl-value>` provides the actual date value.

**Cardinality:**  For any non-global, non-text element, you may have at most one `<gsl-label>`, one `<gsl-title>`, and one `<gsl-value>` as the first children, in any order. These are optional and should be omitted if not needed.

---

## `<gsl-surgery>` Element

**Purpose:**
Documents major changes, removals, or replacements—what was changed (“surgery”), when, why, the impact, and next steps. This brings full auditability and traceability to your prompt documents, allowing both humans and agents to understand not just *what* is present, but *how* and *why* it evolved.

**Supported child elements:**

* `<gsl-when>`: When the change occurred
* `<gsl-what>`: What was removed/changed
* `<gsl-why>`: Reason for the change
* `<gsl-impact>`: Expected or observed impact
* `<gsl-action>`: Follow-up or mitigation plan

**Example:**

```xml
    <gsl-surgery>
    <gsl-when>
    <gsl-title>
    
    #### When</gsl-title>
    <gsl-value>
    
    2025-08-02</gsl-value>
    </gsl-when>
    <gsl-what>
    <gsl-value>
    
    Automated release draft</gsl-value>
    </gsl-what>
    <gsl-why>
    <gsl-value>
    
    Caused race condition during concurrent PR merges</gsl-value>
    </gsl-why>
    <gsl-impact>
    <gsl-value>
    
    Delayed releases, increased human intervention</gsl-value>
    </gsl-impact>
    <gsl-action>
    <gsl-value>
    
    Rewrite workflow to use queueing mechanism</gsl-value>
    </gsl-action>
    </gsl-surgery>
```

---

## `type` Attribute on `<gsl-prompt>`

**Purpose:**
Adds a machine-parseable classification to each prompt, enabling grouping, filtering, and automated reporting.

**Allowed values (following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard):**

* `feat`, `fix`, `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`



**Example:**

```xml
<gsl-prompt id="20250803T120000+0000" type="feat">
  ...
</gsl-prompt>
```

---

## Updated Conventions and Guidelines

### 1. No Mixed Content

Continue to avoid mixing free text with child elements. Use `<gsl-description>`, `<gsl-label>`, `<gsl-title>`, and `<gsl-value>` for all text content within a parent element that otherwise contains elements.

### 2. Section Header Order

When present, `<gsl-label>`, `<gsl-title>`, `<gsl-value>`, and `<gsl-description>` should appear at the top of their parent section, in any order.

### 3. Using `<gsl-surgery>` for Audit Trails

Document any significant “surgery” (removal, replacement, or major refactor) to a prompt, workflow, or section using `<gsl-surgery>`.
This element should appear directly under the section affected, or within a dedicated audit or history block if preferred.


---

## Best Practices and Adoption Tips

* **Be explicit:** Use `<gsl-label>`, `<gsl-title>`, `<gsl-value>`, and the `type` attribute wherever they add clarity.
* **Audit changes:** Record significant changes with `<gsl-surgery>` to build a transparent project history.
* **Update tools:** Update agents and validators to recognize new elements and attributes, but never break on older, simpler files.
* **Document conventions:** Keep your AGENTS.md file or project README up to date with examples and definitions.

---

## Looking Forward

GSL remains extensible and open to further evolution as team and automation needs change.
If new roles, workflows, or audit requirements emerge, they can be integrated using the same principles—machine-parseable structure, human-friendly conventions, and backward compatibility.

---

*For the authoritative data dictionary and up-to-date element definitions, see the project’s global AGENTS.md file.*

---
