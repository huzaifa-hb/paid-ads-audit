# Contributing

Thanks for helping keep this accurate. Ad platforms change their products every few months, so most useful contributions are corrections.

## What to send

- A benchmark that is out of date, with a source and date.
- A check that no longer applies, or a new one the platform now needs (for example a new attribution setting or a new campaign type).
- A wrong threshold. If you have account data that shows a rule misfires, describe the situation in the issue.
- Clearer wording in the instructions. Shorter is better; the AI reads these files on every run.

## How the repo is organized

`claude/ads` and `chatgpt/ads` are two versions of the same skill. Checklists, benchmarks, and scoring live in `references/` inside each. If you change a reference file in one version, make the same change in the other unless the difference is on purpose.

Platform-specific instructions are in `skills/<platform>/instructions.md`.

## Making a change

1. Fork the repo and edit the files in `claude/ads` and `chatgpt/ads`.
2. Run `./scripts/package.sh` to rebuild the `.skill` files in `dist/`.
3. Test the change in at least one of ChatGPT, Claude.ai, Claude Code, or Codex. Say which one in the pull request.
4. Open a pull request. Describe what changed and why, and link a source for any number you changed.

Keep the writing in the skill files plain. No marketing language, no filler. The AI follows these instructions literally.

## Reporting a problem

Use the issue templates. Include which app you ran the skill in, which platform you were auditing, and what the skill said versus what you expected. Never paste account IDs, tokens, or customer data into an issue.
