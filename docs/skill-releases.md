# Skill releases

This repository publishes `trinary-agents`, `trinary-rapid`, and
`trinary-workspace-backup` as separate GitHub Releases. Each release includes
a ZIP containing the skill's folder at the archive root, ready to upload to
Claude's Skills settings.

## Versioning and publishing

- Each skill has its own `VERSION` file and Semantic Versioning sequence.
- When a pull request changes a skill folder, it must increase that skill's
  version in the same pull request. The pull request check validates the
  version format and requires it to increase from the base branch.
- The `validate-version-bumps` check runs on every pull request to `main` and
  should be required by the `Protect main` ruleset. The importable ruleset
  configuration is in `.github/rulesets/protect-main.json`.
- The `test-skills` check runs each skill's supporting-tool tests on every pull
  request to `main` and is also required by that ruleset.
- Merging to `main` runs the publishing workflow for every skill. It creates a
  release only for a version whose tag has not been published yet. Unchanged
  versions are skipped, so unrelated repository merges do not create duplicate
  releases.
- Tags use `<skill-name>-v<version>`, for example
  `trinary-agents-v1.0.0`, `trinary-rapid-v1.0.0`, and
  `trinary-workspace-backup-v1.0.0`.
- Record user-facing changes in the skill's `CHANGELOG.md` under a
  `## <version>` heading matching `VERSION`. The publishing workflow uses that
  section as the release notes, followed by GitHub's generated list of merged
  pull requests. A version without a changelog section gets generated notes
  only.
- Releases are published with ZIP assets named
  `<skill-name>-v<version>.zip`. The ZIP contains the skill directory itself,
  so the `SKILL.md` file remains inside the folder when imported.

The initial version is `1.0.0` for each skill, including `trinary-rapid`. A
new skill passes the version check without a base-branch `VERSION`; it only
needs a valid `VERSION` file in the pull request that adds it. A manual
workflow run can retry a release if its first publishing attempt fails; already
published versions are skipped.
