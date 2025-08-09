# **Prompt vs Task – Part 2**

_Clarifying the roles of specification and implementation in the Codex workflow_

In our development workflow, “prompt” and “task” are both written documents, both describe work we want done, and both can even talk about the same feature. But they have **different jobs** and operate at **different stages** in the process. Confusing them can lead to misaligned expectations, so here’s the clear breakdown.

* * *

## **1. What is a Prompt?**

A **prompt** is our **structured specification**. It’s written in `<gsl-prompt>` format, which Codex uses to ingest and reason about a feature request in a predictable way.

The **prompt’s job** is to:

* Describe the **desired end state** of the feature.
    
* Define **acceptance criteria** that tell us when the feature is “done.”
    
* Provide enough **context and examples** for anyone reading it to understand the intended behavior without seeing the code.
    

A prompt is **solution-neutral** about _how_ to implement the feature. It focuses on _what_ the software should do, not the low-level changes to make that happen.

**Example:**

> “Add `set-project-path` to manage project root paths, using env var or config file, with a deprecated fallback to the old walk-up search.”

* * *

## **2. What is a Task?**

A **task** is our **implementation playbook**. It’s derived from a prompt (or several prompts) but lives closer to the code.

The **task’s job** is to:

* Translate the feature’s desired behavior into **explicit engineering actions**.
    
* Resolve **ambiguities** from the prompt by making final decisions on scope and approach.
    
* Provide **step-by-step changes** to code, tests, and documentation.
    
* Specify **what must be removed, replaced, or refactored**.
    

Tasks are **prescriptive**, not just descriptive. They tell a developer or agent _exactly what to do next_.

**Example:**

> “Remove the legacy walk-up search entirely. Fail with an error if no env var or config. Update `validate-all` and `harmonize-all` to call `resolve_project_root()`.”

* * *

## **3. How They Relate**

| Stage | Document | Purpose | Key Characteristic |
| --- | --- | --- | --- |
| **Feature definition** | **Prompt** | Define the desired end state and acceptance criteria | Describes _what_ to build |
| **Implementation** | **Task** | Give explicit steps to achieve that end state in the codebase | Describes _how_ to build it |

It’s common for a **task** to **narrow or expand** the scope from the original **prompt**. For example:

* The prompt might allow a deprecated fallback for compatibility.
    
* The task might decide to remove it immediately for simplicity.
    

When that happens, the task takes precedence — it’s the final authority for what gets shipped.

* * *

## **4. Why Both Are Useful**

If we only had prompts:

* We’d know the desired outcome but risk inconsistent implementation approaches.
    

If we only had tasks:

* We’d have instructions for one implementation, but lose the reusable, high-level specification that future features could reference.
    

Keeping **both** means we can:

* Preserve a clear history of _why_ a feature was designed the way it was.
    
* Allow implementation plans to adapt over time without rewriting the original intent.
    

* * *

## **5. Key Takeaways**

* **Prompt** = _specification_: high-level, end-state, acceptance criteria.
    
* **Task** = _execution_: detailed, scoped, actionable steps.
    
* The **prompt** lives longer; the **task** may be disposable after implementation.
    
* When the two conflict, the **task’s instructions override the prompt** for that implementation cycle.
    

* * *

If Part 1 of _Prompt vs Task_ was about defining these terms, Part 2 is about recognizing that **they are deliberately different tools** in the workflow — one to set the target, the other to guide the shot.

* * *
