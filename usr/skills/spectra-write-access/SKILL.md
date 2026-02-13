---
name: "spectra-write-access"
description: "Guidance for making code changes on feature branches when delegated from Spectra-One in write-access mode. Use when the task mentions CODE CHANGE TASK, write-access, or feature branch."
version: "1.0.0"
author: "Spectra-One Team"
tags: ["write-access", "code-change", "git", "spectra", "delegation"]
trigger_patterns:
  - "CODE CHANGE TASK"
  - "write-access"
  - "Write-Access Mode"
  - "feature branch"
  - "a0/"
---

# Spectra Write-Access Code Changes

## Context

You are handling a **write-access code change** delegated from Spectra-One. A feature branch has been created for you. Your job is to implement the requested changes on this branch.

**Working Directory:** `/home/shayne/spectra-one/`

## Workflow

1. **Checkout the branch** specified in the task (e.g., `git checkout a0/fix-tts-reconnect-1707712345678`)
2. **Read and understand** the relevant files before making changes
3. **Implement the changes** as described in the task
4. **Test your changes** — run relevant checks (`node -c` for syntax, any applicable tests)
5. **Stage and commit** your changes on the branch with a clear commit message
6. **Report what you did** — list files changed, what was modified, and any concerns

## Safety Rules — NON-NEGOTIABLE

### Git Operations
- NEVER checkout main or merge into main — stay on your feature branch
- NEVER push to any remote — all operations are LOCAL only
- NEVER force-push or rebase
- NEVER delete branches
- Commit messages should be descriptive: `feat: add retry logic to TTS reconnection`

### Code Safety
- Do NOT modify `.env` files or any file containing secrets
- Do NOT change service ports or bindings
- Do NOT modify `web/config/models.yaml` unless the task specifically requires it
- Do NOT install new npm dependencies unless the task specifically requires it
- Do NOT modify files outside the scope of the task

### Scope Boundaries
- Only modify files in `/home/shayne/spectra-one/` (NOT ~/agent-zero/, NOT ~/moltbot/)
- If the task requires changes outside spectra-one, report this in your response instead of making the changes
- If you are unsure about a change, describe what you WOULD do and why, rather than guessing

## Response Format

Write a FULL, DETAILED REPORT of what you did:

```
# Code Change Report

## Branch
- Branch: a0/feature-name-timestamp
- Base: main

## Changes Made
- `path/to/file.js`: Description of what changed and why
- `path/to/other.js`: Description of what changed and why

## Testing
- Ran `node -c path/to/file.js` — passed
- Ran `npm test` — X tests passed, 0 failed (or: no test suite exists)

## Commits
- `abc1234` feat: description of commit

## Concerns / Notes
- Any edge cases, risks, or things the reviewer should pay attention to
```

## Error Handling

If the task cannot be completed:

1. Explain what was attempted
2. Include full error messages
3. Describe the root cause
4. Suggest an alternative approach
5. Do NOT leave the branch in a broken state — revert uncommitted changes if needed (`git checkout -- .`)

## Access Tier

**Current Tier:** Write-Access (Feature Branch)

You CAN:
- Read, modify, create, and delete files in the spectra-one codebase
- Run build/lint/test commands
- Make git commits on the feature branch

You CANNOT:
- Merge into main (user approves via Spectra UI)
- Push to remotes
- Modify configuration or secrets
- Change other repos (agent-zero, moltbot)
