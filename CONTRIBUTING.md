# Contributing

This project uses the **Conventional Commits** standard.
Use `npx git-cz` (provided by Commitizen) instead of `git commit` for a guided prompt.

## Local Setup

1. Run `npm install` inside the `devtools/` folder to install commitlint, commitizen, and husky.
2. Run `npm run prepare` to set up Husky git hooks.

All commits are linted automatically. Release notes and the `CHANGELOG.md` file are updated by [Release Drafter](https://github.com/release-drafter/release-drafter) when pull requests are merged to `main`.
