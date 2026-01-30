#!/usr/bin/env python3
"""
Agent Zero Instrument: Create Implementation Plan

Generates detailed implementation plans with tasks grouped by subsystem.
Supports plan templates (feature, bugfix, refactor) and saves plans with
date-based naming following the Agent Zero workflow mapping.

Usage:
    python create_implementation_plan.py --type feature --name "user-auth" --goal "Add user authentication"
    python create_implementation_plan.py --type bugfix --name "fix-login-bug" --goal "Fix login timeout issue"
    python create_implementation_plan.py --type refactor --name "cleanup-auth" --goal "Refactor auth module"

Author: Agent Zero Framework
Created: 2025-01-15
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Constants
PROJECT_ROOT = Path("/home/shayne/agent-zero/usr/projects/agent_zero_enhancements_and_extensions")
PLANS_DIR = PROJECT_ROOT / "plans"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# Plan templates
PLAN_TEMPLATES = {
    "feature": '''
# [FEATURE_NAME] Implementation Plan

> **Status:** DRAFT
> **Type:** Feature
> **Created:** {date}
> **Author:** Agent Zero

## Specification

**Goal:** {goal}

**Success Criteria:**

- [ ] All acceptance criteria met
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated

## Context Loading

_Run before starting:_

```bash
# Read relevant source files
glob src/**/*.{{ts,js,py}}

# Read existing tests
glob tests/**/*.{{test.ts,test.py,spec.js}}

# Check dependencies
ls -la package.json || ls -la requirements.txt
```

## Tasks

### Task 1: [Setup and Foundation]

**Context:** `src/`, `tests/`

**Steps:**

1. [ ] Review existing codebase structure
2. [ ] Set up necessary directories
3. [ ] Configure development dependencies

**Verify:** `ls -la src/ tests/`

---

### Task 2: [Core Implementation]

**Context:** `src/feature/`, `tests/feature/`

**Steps:**

1. [ ] Implement core feature logic
2. [ ] Add comprehensive tests
3. [ ] Export and integrate

**Verify:** `npm test -- tests/feature/ || pytest tests/feature/`

---

### Task 3: [Integration and Polish]

**Context:** `src/`, `docs/`

**Steps:**

1. [ ] Integrate with existing system
2. [ ] Update documentation
3. [ ] Run full test suite

**Verify:** `npm test || pytest`
''',

    "bugfix": '''
# [BUGFIX_NAME] Bug Fix Plan

> **Status:** DRAFT
> **Type:** Bugfix
> **Created:** {date}
> **Author:** Agent Zero

## Specification

**Goal:** {goal}

**Root Cause:** [To be identified during debugging]

**Success Criteria:**

- [ ] Bug reproduces before fix
- [ ] Bug no longer reproduces after fix
- [ ] Regression tests added
- [ ] All existing tests still pass

## Context Loading

_Run before starting:_

```bash
# Read relevant source files
glob src/**/*.{{ts,js,py}}

# Read error logs
cat logs/error.log || journalctl -u service -n 50

# Check recent changes
git log --oneline -10
```

## Tasks

### Task 1: [Reproduce and Investigate]

**Context:** `src/`, `tests/`, `logs/`

**Steps:**

1. [ ] Reproduce the bug reliably
2. [ ] Add reproduction test case
3. [ ] Investigate root cause

**Verify:** Test case reproduces the bug

---

### Task 2: [Implement Fix]

**Context:** `src/`, `tests/`

**Steps:**

1. [ ] Implement the fix
2. [ ] Verify fix resolves issue
3. [ ] Add regression tests

**Verify:** `npm test -- tests/bugfix/ || pytest tests/bugfix/`

---

### Task 3: [Verify and Deploy]

**Context:** `src/`, `tests/`

**Steps:**

1. [ ] Run full test suite
2. [ ] Check for regressions
3. [ ] Document the fix

**Verify:** `npm test || pytest`
''',

    "refactor": '''
# [REFACTOR_NAME] Refactoring Plan

> **Status:** DRAFT
> **Type:** Refactor
> **Created:** {date}
> **Author:** Agent Zero

## Specification

**Goal:** {goal}

**Refactoring Principles:**
- Behavior must be preserved
- Tests must pass throughout
- Improve code quality and maintainability

**Success Criteria:**

- [ ] All tests pass before and after refactor
- [ ] Code complexity reduced
- [ ] Documentation updated
- [ ] No regressions introduced

## Context Loading

_Run before starting:_

```bash
# Read code to be refactored
glob src/**/*.{{ts,js,py}}

# Read existing tests
glob tests/**/*.{{test.ts,test.py,spec.js}}

# Run baseline tests
npm test || pytest --cov
```

## Tasks

### Task 1: [Prepare Baseline]

**Context:** `src/`, `tests/`

**Steps:**

1. [ ] Ensure all tests pass
2. [ ] Document current behavior
3. [ ] Take code coverage snapshot

**Verify:** `npm test || pytest --cov`

---

### Task 2: [Apply Refactoring]

**Context:** `src/module/`, `tests/module/`

**Steps:**

1. [ ] Apply refactoring changes
2. [ ] Verify tests still pass
3. [ ] Update type hints/annotations

**Verify:** `npm test -- tests/module/ || pytest tests/module/`

---

### Task 3: [Cleanup and Verify]

**Context:** `src/`, `tests/`, `docs/`

**Steps:**

1. [ ] Remove deprecated code
2. [ ] Update documentation
3. [ ] Run full test suite

**Verify:** `npm test || pytest --cov`
'''
}


class PlanGenerator:
    """Generates implementation plans from templates."""

    def __init__(self, plan_type: str, name: str, goal: str,
                 output_dir: Optional[Path] = None):
        """
        Initialize the plan generator.

        Args:
            plan_type: Type of plan (feature, bugfix, refactor)
            name: Plan name (will be slugified for filename)
            goal: High-level goal description
            output_dir: Directory to save plans (defaults to PLANS_DIR)
        """
        self.plan_type = plan_type.lower()
        self.name = name
        self.goal = goal
        self.output_dir = output_dir or PLANS_DIR
        self.date = datetime.now().strftime("%Y-%m-%d")

        if self.plan_type not in PLAN_TEMPLATES:
            raise ValueError(
                f"Invalid plan type: {plan_type}. "
                f"Must be one of: {list(PLAN_TEMPLATES.keys())}"
            )

    def slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        slug = text.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug

    def generate_filename(self) -> str:
        """Generate plan filename with date-based naming."""
        slug_name = self.slugify(self.name)
        return f"{self.date}-{slug_name}.md"

    def generate_content(self) -> str:
        """Generate plan content from template."""
        template = PLAN_TEMPLATES[self.plan_type]
        content = template.format(
            date=self.date,
            goal=self.goal
        )

        feature_name_title = self.name.replace("-", " ").title()
        content = content.replace("[FEATURE_NAME]", feature_name_title)
        content = content.replace("[BUGFIX_NAME]", feature_name_title)
        content = content.replace("[REFACTOR_NAME]", feature_name_title)

        return content

    def save_plan(self) -> Path:
        """
        Generate and save the plan to disk.

        Returns:
            Path to the saved plan file
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        filename = self.generate_filename()
        content = self.generate_content()

        plan_path = self.output_dir / filename
        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return plan_path

    def add_task_group(self, plan_path: Path, group_name: str,
                       tasks: List[Dict]) -> None:
        """
        Add a task group to an existing plan.

        Args:
            plan_path: Path to the plan file
            group_name: Name of the task group/subsystem
            tasks: List of task dictionaries with 'context', 'steps', 'verify'
        """
        if not plan_path.exists():
            raise FileNotFoundError(f"Plan not found: {plan_path}")

        with open(plan_path, 'r', encoding='utf-8') as f:
            content = f.read()

        group_section = f"\n## {group_name}\n\n"
        for i, task in enumerate(tasks, 1):
            task_name = task.get('name', f'Task {i}')
            task_context = task.get('context', '')
            task_verify = task.get('verify', '')
            task_steps = task.get('steps', [])

            task_section = f"""### Task {i}: {task_name}

**Context:** `{task_context}`

**Steps:**
"""
            for step in task_steps:
                task_section += f"1. [ ] {step}\n"

            task_section += f"""
**Verify:** `{task_verify}`

---

"""
            group_section += task_section

        if "## Tasks" in content:
            parts = content.split("## Tasks")
            content = parts[0] + "## Tasks" + group_section + parts[1]
        else:
            content += "\n## Tasks\n" + group_section

        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(content)


def create_plan_interactive() -> None:
    """Interactive mode for creating plans."""
    print("\n=== Agent Zero Implementation Plan Generator ===\n")

    print("Available plan types:")
    for i, ptype in enumerate(PLAN_TEMPLATES.keys(), 1):
        print(f"  {i}. {ptype}")

    while True:
        choice = input("\nSelect plan type (number or name): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(PLAN_TEMPLATES):
            plan_type = list(PLAN_TEMPLATES.keys())[int(choice) - 1]
            break
        elif choice.lower() in PLAN_TEMPLATES:
            plan_type = choice.lower()
            break
        else:
            print("Invalid choice. Please try again.")

    name = input("\nEnter plan name (e.g., 'user-authentication'): ").strip()
    if not name:
        print("Error: Plan name is required.")
        return

    goal = input("\nEnter goal description: ").strip()
    if not goal:
        print("Error: Goal description is required.")
        return

    try:
        generator = PlanGenerator(plan_type, name, goal)
        plan_path = generator.save_plan()
        print(f"\n✓ Plan created successfully: {plan_path}")
        print(f"\nTo edit the plan, open: {plan_path}")
        print("To execute the plan, run: python execute_implementation_plan.py --plan {plan_path.name}")
    except Exception as e:
        print(f"\n✗ Error creating plan: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Agent Zero implementation plans",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --type feature --name "user-auth" --goal "Add user authentication"
  %(prog)s --type bugfix --name "fix-login" --goal "Fix login timeout issue"
  %(prog)s --type refactor --name "cleanup" --goal "Refactor auth module"
  %(prog)s --interactive
        """
    )

    parser.add_argument(
        "--type", "-t",
        choices=list(PLAN_TEMPLATES.keys()),
        help="Type of plan to create"
    )

    parser.add_argument(
        "--name", "-n",
        help="Name of the plan (used in filename)"
    )

    parser.add_argument(
        "--goal", "-g",
        help="High-level goal description"
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=PLANS_DIR,
        help=f"Output directory for plans (default: {PLANS_DIR})"
    )

    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )

    args = parser.parse_args()

    if args.interactive or (not args.type and not args.name and not args.goal):
        create_plan_interactive()
        return

    if not all([args.type, args.name, args.goal]):
        parser.error("--type, --name, and --goal are required unless using --interactive")

    try:
        generator = PlanGenerator(args.type, args.name, args.goal, args.output)
        plan_path = generator.save_plan()
        print(f"Plan created: {plan_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
