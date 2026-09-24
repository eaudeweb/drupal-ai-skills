# Repository guidance

This repository is the `edw-drupal` Claude Code plugin, shared with the Eau de Web Drupal team. See README.md for the structure.

- Skills are located in `skills/<name>/SKILL.md` with `name` and `description` frontmatter. The description must say what the skill does and when to use it.
- Write skill content in clear, plain British English, in present tense. Use "-" instead of "—" and no curly quotes.
- Keep each `SKILL.md` focused and short. Put long material in `skills/<name>/references/`.
- Content must be generic to the team. No credentials, customer data or project-specific details.
- Bump `version` in `.claude-plugin/plugin.json` on every change that is shared.
- Validate with `claude plugin validate .` before committing.
