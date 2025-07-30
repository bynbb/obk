# 🗭 The Real Difference Between a Prompt and a Directive

In the world of intelligent agents, automation tools, and prompt-driven development, two terms show up again and again: **prompt** and **directive**.

At first glance, they seem easy to separate. Directives are commands; prompts are requests. But if you’ve ever built a system where agents follow both, you’ve likely noticed that the line between them isn’t so clear. Sometimes they look the same. Sometimes they *are* the same.

So what's the real difference?

Let’s unpack it.

---

## 🔀 Same Content, Different Roles

A **prompt** and a **directive** can contain the **exact same text** and still be different. Why?

Because the distinction isn’t about the words themselves — it’s about what **role** those words are playing in the system.

* A **directive** instructs: "Do this."
* A **prompt** triggers: "Here’s a thing to act on."

Both can be action-driving. Both can tell an agent what to do. The difference is **functional**, not structural.

---

## 🧐 A Matter of Intent and Form

|                            | **Directive**                            | **Prompt**                                     |
| -------------------------- | ---------------------------------------- | ---------------------------------------------- |
| **Function**               | Instructs, enforces, constrains behavior | Triggers action, response, or generation       |
| **Form**                   | Rule-based, imperative                   | Often contextual, narrative, or example-driven |
| **May include a command?** | Yes                                      | Yes                                            |
| **May be context-only?**   | No                                       | Yes                                            |

**Prompts** are broader. They might contain tasks, questions, scenarios, or even just background information.

**Directives** are narrower. They must contain an instruction and are always meant to constrain or guide behavior.

---

## 🤖 Specificity Is Relative

People often say a directive is more "general," and a prompt is more "specific."

But **specificity isn’t absolute**. It’s a **relative** property. You can't say a thing is "specific" unless you're comparing it to something else.

For example:

* Prompt A: “Format the code.”
* Prompt B: “Format `main.py` using Black with line length 88.”

Prompt B is more specific *than* A. But neither is specific on its own. Same goes for directives.

So we don’t separate prompts and directives by how specific they are. That changes depending on what you're comparing them to.

---

## 🗳 Prompts Can Act Like Directives (and Vice Versa)

A directive can say:

> “Follow Prompt A.”

And Prompt A might say:

> “Add tests for `argparse_cli.py` using the one-line test format.”

Which one is the command? Both. But the **directive points**; the **prompt does**.

So it’s not about structure or specificity. It’s about **function**:

* A **directive** tells the agent to do something.
* A **prompt** *is* the thing the agent is supposed to do.

Even if they're the same file, same text, same scope.

---

## 📄 When a Specification Acts Like a Directive

A **specification** is usually a formal document that defines how a system behaves. But in agent-based systems, a specification often contains directives. Sometimes it *is* the directive.

Example:

```xml
<gsl-document-spec>
  Agents MUST NOT delete any <gsl-test> entries once written.
</gsl-document-spec>
```

This isn’t just documentation — it’s an active policy that governs agent behavior. So yes, a **specification can behave as a directive**.

---

## 🔗 How OBK Uses Prompts and Directives

Now that we’ve got the general definitions out of the way, here’s how "prompt" and "directive" are used in the **OBK** project.

OBK is a system built around **prompt-driven development**, where agents generate and modify source code based on structured input documents. In OBK, prompts and directives are both first-class artifacts — but they play different roles.

### ✅ Example: Prompt

This is an actual OBK prompt file:

```xml
<gsl-prompt id="20250730T062755-0400">
  <gsl-purpose>
    Implement classes in my Python project.
  </gsl-purpose>
  <gsl-tdd>
    <gsl-test id="T1">
    - T1: TBD
    </gsl-test>
  </gsl-tdd>
  <gsl-document-spec>
    Agents MUST NOT modify existing <gsl-test> entries.
    Agents MAY append new tests.
  </gsl-document-spec>
</gsl-prompt>
```

This prompt sets the task, the context, and the constraints. It’s not just a request — it’s a hybrid of **task input**, **context provider**, and **governing rules**.

### ✅ Example: Directive

Here’s a corresponding OBK directive:

```
## Unified Prompt-Driven Functions to Classes Task

Objective:
Sequentially implement and test features in `obk` by reproducing behaviors from a reference article.

1. Analyze the repo.
2. Extract features from the article.
3. Write manual tests in prompt `20250730T062755-0400`.
4. Follow file modification constraints.
```

This is clearly an **instruction document**. It tells the agent what to do, in what order, with which constraints. The agent is expected to follow it line-by-line, using the named prompt to drive implementation.

The **directive refers to the prompt**, and the **prompt contains the implementation rules**. They are distinct, but deeply interdependent.

---

## 🔺 Final Word

So, what’s the real difference between a prompt and a directive?

It’s not about specificity.
It’s not about structure.
It’s not even about whether it contains a command.

> ✨ **It’s about the role the message plays in the system.**

* A **prompt** is a thing you act on.
* A **directive** is a thing that tells you to act.
* A **specification** might do both.

Sometimes they overlap. Sometimes they are indistinguishable. And that’s okay.

In systems like OBK, we embrace the blur — because what matters is **traceability**, **intent**, and **consistency**. Not rigid labels.

That’s the real difference.
