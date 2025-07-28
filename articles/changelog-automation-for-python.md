# Modern CHANGELOG Automation for Python Projects

#### *A Step-by-Step Guide Using Conventional Commits and GitHub Actions*

Keeping a well-structured, up-to-date `CHANGELOG.md` is essential for any Python project—but maintaining it manually is tedious and error-prone. Modern teams use automated tools to ensure every feature, bugfix, and change is documented accurately, directly from commit history. This guide walks you through **the industry-standard workflow** for Python apps: combining Conventional Commits, commit linting, and GitHub Actions with Release Drafter to generate a clean, fully automated changelog.

* * *

## Table of Contents

1. [Why Automate Your CHANGELOG?](#why-automate-your-changelog)
    
2. [What Are Conventional Commits?](#what-are-conventional-commits)
    
3. [The Best Toolchain for Python Projects](#the-best-toolchain-for-python-projects)
    
4. [Step 1: Enforce Commit Message Standards with Commitlint](#step-1-enforce-commit-message-standards-with-commitlint)
    
5. [Step 2: Make Commit Messages Easy with Commitizen](#step-2-make-commit-messages-easy-with-commitizen)
    
6. [Step 3: Automate Your CHANGELOG with Release Drafter](#step-3-automate-your-changelog-with-release-drafter)
    
7. [Step 4: CI Integration with GitHub Actions](#step-4-ci-integration-with-github-actions)
    
8. [Best Practices & Pro Tips](#best-practices--pro-tips)
    
9. [Sample devtools Folder and Config Files](#sample-devtools-folder-and-config-files)
    
10. [Conclusion](#conclusion)
    

* * *

## Why Automate Your CHANGELOG?

A changelog tells users, teammates, and future-you what changed and why. But without automation:

* Developers forget to update it.
    
* Entries are inconsistent or missing.
    
* Releases require tedious manual review.
    

**Automating your changelog** ensures:

* Every change is tracked and categorized.
    
* Release notes are always ready to go.
    
* Less busywork, more focus on code.
    

* * *

## What Are Conventional Commits?

**Conventional Commits** are a simple convention for writing commit messages. Each message begins with a type (`feat:`, `fix:`, etc.), optionally followed by a scope and a short description. For example:

```
feat(cli): add --help option
fix: correct typo in documentation
chore: update dependencies
```

**Why use them?**

* Tools can parse, group, and release based on these tags.
    
* Clean, human-readable history.
    
* Enables automated versioning and changelogs.
    

* * *

## The Best Toolchain for Python Projects

While many changelog tools exist, the modern, low-friction, cross-language standard stack is:

| Step | Tool(s) | Purpose |
| --- | --- | --- |
| 1 | **commitlint + husky** | Enforce commit message conventions |
| 2 | **commitizen** (optional) | Guide contributors to write good commits |
| 3 | **Release Drafter** | Auto-generate CHANGELOG and release notes |
| 4 | **GitHub Actions** | Enforce checks & automation in CI |

> **Note:** These tools work for _any_ language—your Python code and environment remain untouched.

* * *

## Step 1: Enforce Commit Message Standards with Commitlint

**commitlint** is the industry-standard linter for Conventional Commits. It doesn’t care what language your code is—just that your commits follow the format.

### Installation

In your repo (you can use a `/devtools` folder to keep Node tools out of your main codebase):

```sh
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky
```

Add a commitlint config (`commitlint.config.js`):

```js
module.exports = {extends: ['@commitlint/config-conventional']};
```

### Add a Husky Git Hook

```sh
npx husky install
npx husky add .husky/commit-msg "npx --no-install commitlint --edit \$1"
```

Now, **every commit message is linted** before it's saved.

* * *

## Step 2: Make Commit Messages Easy with Commitizen (Optional)

**commitizen** provides an interactive CLI (`git cz`) to help you write well-formed commit messages. This removes guesswork and lowers the barrier for contributors.

```sh
npm install --save-dev commitizen
npx commitizen init cz-conventional-changelog --save-dev --save-exact
```

Add to your docs:

> “Use `npx git-cz` instead of `git commit` for a guided commit message prompt.”

* * *

## Step 3: Automate Your CHANGELOG with Release Drafter

**Release Drafter** is a GitHub Action that drafts release notes and updates your changelog based on merged pull requests—organized by labels or by commit message tags.

### Set Up Release Drafter

1. Create `.github/release-drafter.yml` with category configuration:
    

```yaml
name-template: 'v$NEXT_PATCH_VERSION'
tag-template: 'v$NEXT_PATCH_VERSION'
categories:
  - title: "🚀 Features"
    labels:
      - "feature"
    pull_request_title:
      - '^feat:'
  - title: "🐛 Fixes"
    labels:
      - "fix"
    pull_request_title:
      - '^fix:'
  - title: "🧹 Chores"
    pull_request_title:
      - '^chore:'
change-template: '- $TITLE @$AUTHOR (#$NUMBER)'
```

2. Add the Release Drafter Action to your workflows (e.g., `.github/workflows/release-drafter.yml`):
    

```yaml
name: Release Drafter

on:
  push:
    branches:
      - main
  pull_request:
    types: [closed]

jobs:
  update_release_draft:
    runs-on: ubuntu-latest
    steps:
      - uses: release-drafter/release-drafter@v6
        with:
          config-name: release-drafter.yml
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Every time a PR is merged, a draft release and changelog is updated automatically.

* * *

## Step 4: CI Integration with GitHub Actions

**Don’t just enforce locally—use CI too.**

Example `.github/workflows/commitlint.yml` for checking all commit messages on PRs:

```yaml
name: Commit Lint

on: [pull_request]

jobs:
  commitlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: wagoid/commitlint-github-action@v6
```

This ensures no bad commits sneak in via PRs, even from forks or external contributors.

* * *

## Best Practices & Pro Tips

* **Document the workflow:** Add a `CONTRIBUTING.md` that explains the commit format, how to use `git cz`, and any local setup steps.
    
* **Keep Node tooling out of Python:** Isolate Node tools (commitlint, commitizen, husky) in `/devtools` or similar folder.
    
* **Use PR titles or commit messages:** Release Drafter can categorize changelog entries using either; just be consistent in your workflow.
    
* **Don’t forget labels:** Label PRs with `feature`, `fix`, etc., to give Release Drafter extra context.
    
* **Semantic-release?** If you want _full_ automation (including version bumps and PyPI deploys), semantic-release is another option, but it’s more common in JavaScript ecosystems.
    

* * *

## Sample devtools Folder and Config Files

```
devtools/
  package.json             # for commitlint, commitizen, husky, etc.
  commitlint.config.js
  .cz-config.js            # if you customize commitizen
  .husky/
.github/
  release-drafter.yml
  workflows/
    release-drafter.yml
    commitlint.yml
CONTRIBUTING.md
CHANGELOG.md               # (optional—Release Drafter keeps this up to date)
```

* * *

## Conclusion

**Automated changelogs are now standard, not a luxury.**  
By enforcing Conventional Commits, helping contributors with commitizen, and auto-generating your changelog and releases with Release Drafter and GitHub Actions, you’ll save time, prevent errors, and deliver a polished developer experience—no matter how fast your project grows.

* * *