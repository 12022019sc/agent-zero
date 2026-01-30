#!/usr/bin/env python3
"""
Agent Zero Instrument: Execute Implementation Plan

Executes implementation plans with smart task grouping. Groups related tasks
to share agent context, parallelizes across independent subsystems.

Usage:
    python execute_implementation_plan.py --plan 2025-01-15-feature.md
    python execute_implementation_plan.py --plan 2025-01-15-feature.md --batch-size 3
    python execute_implementation_plan.py --plan 2025-01-15-feature.md --dry-run

Author: Agent Zero Framework
Created: 2025-01-15
"""

import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Constants
PROJECT_ROOT = Path("/home/shayne/agent-zero/usr/projects/agent_zero_enhancements_and_extensions")
PLANS_DIR = PROJECT_ROOT / "plans"


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    """Represents a single task in the implementation plan."""
    id: str
    name: str
    context: str
    steps: List[str]
    verify: str
    status: TaskStatus = TaskStatus.PENDING
    subsystem: str = ""
    group: str = ""
    result: Optional[str] = None
    error: Optional[str] = None


@dataclass
class TaskGroup:
    """Represents a group of tasks that share context."""
    name: str
    subsystem: str
    tasks: List[Task] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    
    def add_task(self, task: Task) -> None:
        """Add a task to this group."""
        task.group = self.name
        task.subsystem = self.subsystem
        self.tasks.append(task)
    
    def is_ready(self, completed_groups: set) -> bool:
        """Check if all dependencies are completed."""
        return all(dep in completed_groups for dep in self.dependencies)


class PlanParser:
    """Parses implementation plan files into structured data."""
    
    def __init__(self, plan_path: Path):
        self.plan_path = plan_path
        self.content = ""
        self.specification = {}
        self.context_loading = []
        self.task_groups: List[TaskGroup] = []
    
    def parse(self) -> None:
        """Parse the plan file and extract all components."""
        if not self.plan_path.exists():
            raise FileNotFoundError(f"Plan not found: {self.plan_path}")
        
        with open(self.plan_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        self._parse_specification()
        self._parse_context_loading()
        self._parse_tasks()
    
    def _parse_specification(self) -> None:
        """Extract specification section."""
        spec_match = re.search(
            r'## Specification\n(.*?)(?=##|\Z)',
            self.content,
            re.DOTALL
        )
        if spec_match:
            spec_text = spec_match.group(1)
            self.specification = {
                'goal': self._extract_field(spec_text, 'Goal'),
                'success_criteria': self._extract_list(spec_text, 'Success Criteria'),
                'type': self._extract_field(spec_text, 'Type', 'Unknown'),
                'status': self._extract_field(spec_text, 'Status', 'DRAFT')
            }
    
    def _parse_context_loading(self) -> None:
        """Extract context loading commands."""
        context_match = re.search(
            r'## Context Loading\n(.*?)(?=##|\Z)',
            self.content,
            re.DOTALL
        )
        if context_match:
            context_text = context_match.group(1)
            code_blocks = re.findall(r'```bash\n(.*?)```', context_text, re.DOTALL)
            self.context_loading = [cmd.strip() for cmd in code_blocks if cmd.strip()]
    
    def _parse_tasks(self) -> None:
        """Parse tasks and group them by subsystem."""
        # Find the '## Tasks' section - only parse content within this section
        tasks_match = re.search(
            r'## Tasks\n(.*)',
            self.content,
            re.DOTALL
        )

        if not tasks_match:
            return

        tasks_content = tasks_match.group(1)
        # Find where the next '## ' section starts and trim
        next_section = re.search(r'\n## ', tasks_content)
        if next_section:
            tasks_content = tasks_content[:next_section.start()]

        lines_list = tasks_content.split('\n')

        current_subsystem = "General"
        current_group: Optional[TaskGroup] = None
        task_id = 1
        i = 0

        # Create default group for tasks without subsystem headers
        current_group = TaskGroup(
            name="General",
            subsystem="General"
        )
        self.task_groups.append(current_group)

        while i < len(lines_list):
            line = lines_list[i]

            # Check for subsystem header (## Something that's not 'Tasks')
            subsystem_match = re.match(r'^##\s+(.+)$', line)
            if subsystem_match:
                subsystem_name = subsystem_match.group(1).strip()
                if subsystem_name != 'Tasks':
                    current_subsystem = subsystem_name
                    current_group = TaskGroup(
                        name=subsystem_name,
                        subsystem=subsystem_name
                    )
                    self.task_groups.append(current_group)

            # Check for task header
            task_match = re.match(r'^### Task\s+(\d+):\s*(.+)$', line)
            if task_match:
                task_num = task_match.group(1)
                task_name = task_match.group(2).strip()

                context = ""
                steps = []
                verify = ""

                i += 1
                while i < len(lines_list):
                    task_line = lines_list[i]

                    if task_line.startswith('**Context:**'):
                        context_match = re.search(r'`([^`]+)`', task_line)
                        if context_match:
                            context = context_match.group(1)

                    elif task_line.startswith('**Steps:**'):
                        i += 1
                        while i < len(lines_list) and not lines_list[i].startswith('**Verify:**'):
                            step_match = re.match(r'^\d+\.\s*\[\s*[x ]?\s*\]\s*(.+)$', lines_list[i])
                            if step_match:
                                steps.append(step_match.group(1).strip())
                            i += 1
                        continue

                    elif task_line.startswith('**Verify:**'):
                        verify_match = re.search(r'`([^`]+)`', task_line)
                        if verify_match:
                            verify = verify_match.group(1)
                        break

                    elif task_line.startswith('###') or task_line.startswith('##'):
                        break

                    i += 1

                task = Task(
                    id=f"task-{task_num}",
                    name=task_name,
                    context=context,
                    steps=steps,
                    verify=verify
                )

                if current_group is None:
                    current_group = TaskGroup(
                        name="General",
                        subsystem="General"
                    )
                    self.task_groups.append(current_group)

                current_group.add_task(task)
                task_id += 1

            i += 1

    def _extract_field(self, text: str, field: str, default: str = "") -> str:
        """Extract a field value from text."""
        pattern = rf'\*\*{field}:\*\*\s*([^\n\*]+)'
        match = re.search(pattern, text)
        return match.group(1).strip() if match else default
    
    def _extract_list(self, text: str, field: str) -> List[str]:
        """Extract a list of items from text."""
        items = []
        pattern = rf'\*\*{field}:\*\*\s*\n((?:-\s*\[\s*[x ]?\s*\].+\n)+)'
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            list_text = match.group(1)
            items = re.findall(r'-\s*\[\s*[x ]?\s*\]\s*(.+)', list_text)
        return items


class PlanExecutor:
    """Executes implementation plans with smart task grouping."""
    
    def __init__(self, plan_path: Path, batch_size: int = 3, 
                 dry_run: bool = False, verbose: bool = True):
        self.plan_path = plan_path
        self.batch_size = batch_size
        self.dry_run = dry_run
        self.verbose = verbose
        self.parser = PlanParser(plan_path)
        self.completed_groups: set = set()
        self.failed_groups: set = set()
        self.execution_log: List[Dict] = []
    
    def execute(self) -> bool:
        """Execute the implementation plan."""
        self._log("info", f"Starting execution of plan: {self.plan_path.name}")
        
        try:
            self.parser.parse()
        except Exception as e:
            self._log("error", f"Failed to parse plan: {e}")
            return False
        
        self._print_plan_summary()
        
        if self.dry_run:
            self._log("info", "DRY RUN MODE - No changes will be made")
            return True
        
        self._update_plan_status("IN_PROGRESS")
        self._execute_context_loading()
        success = self._execute_task_groups()
        
        final_status = "COMPLETED" if success else "FAILED"
        self._update_plan_status(final_status)
        
        if success:
            self._log("success", "Plan execution completed successfully!")
        else:
            self._log("error", "Plan execution failed. Check logs for details.")
        
        return success
    
    def _print_plan_summary(self) -> None:
        """Print a summary of the plan."""
        spec = self.parser.specification
        print(f"\n{'='*60}")
        print(f"Plan: {self.plan_path.stem}")
        print(f"Type: {spec.get('type', 'Unknown')}")
        print(f"Goal: {spec.get('goal', 'Not specified')}")
        print(f"\nTask Groups: {len(self.parser.task_groups)}")
        for group in self.parser.task_groups:
            print(f"  - {group.name}: {len(group.tasks)} tasks")
        print(f"{'='*60}\n")
    
    def _execute_context_loading(self) -> None:
        """Execute context loading commands."""
        if not self.parser.context_loading:
            return
        
        self._log("info", "Loading context...")
        
        for cmd in self.parser.context_loading:
            if self.verbose:
                print(f"  $ {cmd}")
            
            if not self.dry_run:
                try:
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode != 0 and self.verbose:
                        print(f"    Warning: Command failed")
                except Exception as e:
                    if self.verbose:
                        print(f"    Error: {e}")
    
    def _execute_task_groups(self) -> bool:
        """Execute task groups in dependency order."""
        self._build_dependencies()
        
        max_iterations = len(self.parser.task_groups) * 2
        iteration = 0
        
        while len(self.completed_groups) < len(self.parser.task_groups):
            if iteration >= max_iterations:
                self._log("error", "Maximum iterations reached - possible circular dependency")
                return False
            
            ready_groups = [
                g for g in self.parser.task_groups
                if g.status == TaskStatus.PENDING and g.is_ready(self.completed_groups)
            ]
            
            if not ready_groups:
                if len(self.completed_groups) < len(self.parser.task_groups):
                    self._log("error", "No ready groups found - possible unmet dependencies")
                    return False
                break
            
            batch = ready_groups[:self.batch_size]
            
            if len(batch) == 1:
                success = self._execute_group(batch[0])
            else:
                success = self._execute_groups_parallel(batch)
            
            if not success:
                return False
            
            iteration += 1
        
        return True
    
    def _build_dependencies(self) -> None:
        """Build dependency graph between task groups."""
        for i, group in enumerate(self.parser.task_groups):
            if i > 0:
                group.dependencies.append(self.parser.task_groups[i-1].name)
    
    def _execute_group(self, group: TaskGroup) -> bool:
        """Execute a single task group."""
        self._log("info", f"Executing group: {group.name}")
        group.status = TaskStatus.IN_PROGRESS
        
        for task in group.tasks:
            success = self._execute_task(task, group)
            
            if not success:
                group.status = TaskStatus.FAILED
                self.failed_groups.add(group.name)
                return False
            
            task.status = TaskStatus.COMPLETED
        
        group.status = TaskStatus.COMPLETED
        self.completed_groups.add(group.name)
        self._log("success", f"Completed group: {group.name}")
        return True
    
    def _execute_groups_parallel(self, groups: List[TaskGroup]) -> bool:
        """Execute multiple task groups in parallel."""
        self._log("info", f"Executing {len(groups)} groups in parallel...")
        
        with ThreadPoolExecutor(max_workers=len(groups)) as executor:
            futures = {executor.submit(self._execute_group, g): g for g in groups}
            
            for future in as_completed(futures):
                group = futures[future]
                try:
                    success = future.result()
                    if not success:
                        for f in futures:
                            f.cancel()
                        return False
                except Exception as e:
                    self._log("error", f"Group {group.name} failed with exception: {e}")
                    group.status = TaskStatus.FAILED
                    self.failed_groups.add(group.name)
                    return False
        
        return True
    
    def _execute_task(self, task: Task, group: TaskGroup) -> bool:
        """Execute a single task."""
        self._log("info", f"  Task: {task.name}")
        task.status = TaskStatus.IN_PROGRESS
        
        # Print task context
        if task.context and self.verbose:
            print(f"    Context: {task.context}")
        
        # Execute steps
        for step in task.steps:
            if self.verbose:
                print(f"    Step: {step}")
            
            if not self.dry_run:
                # Here you would integrate with Agent Zero's agent system
                # For now, we'll simulate execution
                try:
                    # Check if step is a command
                    if step.startswith('$') or step.startswith('git') or step.startswith('npm') or step.startswith('python'):
                        result = subprocess.run(
                            step,
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                        if result.returncode != 0:
                            task.error = result.stderr
                            self._log("error", f"    Step failed: {result.stderr}")
                            return False
                except Exception as e:
                    task.error = str(e)
                    self._log("error", f"    Step failed: {e}")
                    return False
        
        # Run verification
        if task.verify and self.verbose:
            print(f"    Verify: {task.verify}")
        
        if not self.dry_run and task.verify:
            try:
                result = subprocess.run(
                    task.verify,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode != 0:
                    task.error = result.stderr
                    self._log("error", f"    Verification failed: {result.stderr}")
                    return False
            except Exception as e:
                task.error = str(e)
                self._log("error", f"    Verification failed: {e}")
                return False
        
        self._log("success", f"    Task completed: {task.name}")
        return True
    
    def _update_plan_status(self, status: str) -> None:
        """Update the plan status in the file."""
        if self.dry_run:
            return
        
        content = self.parser.content
        content = re.sub(
            r'\*\*Status:\*\*\s*\w+',
            f'**Status:** {status}',
            content
        )
        content = re.sub(
            r'\*\*Status:\*\*\s*DRAFT',
            f'**Status:** {status}',
            content
        )
        
        with open(self.plan_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _log(self, level: str, message: str) -> None:
        """Log a message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
        self.execution_log.append(log_entry)
        
        if level == "error":
            print(f"[ERROR] {message}")
        elif level == "success":
            print(f"[OK] {message}")
        else:
            print(f"[INFO] {message}")


def list_plans() -> None:
    """List all available plans."""
    if not PLANS_DIR.exists():
        print("No plans directory found.")
        return
    
    plans = sorted(PLANS_DIR.glob("*.md"))
    
    if not plans:
        print("No plans found.")
        return
    
    print("\nAvailable plans:\n")
    for plan in plans:
        print(f"  - {plan.name}")
    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Execute Agent Zero implementation plans",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --plan 2025-01-15-feature.md
  %(prog)s --plan 2025-01-15-feature.md --batch-size 3
  %(prog)s --list
  %(prog)s --plan 2025-01-15-feature.md --dry-run
        """
    )
    
    parser.add_argument(
        "--plan", "-p",
        type=Path,
        help="Path to the plan file to execute"
    )
    
    parser.add_argument(
        "--batch-size", "-b",
        type=int,
        default=3,
        help="Number of task groups to execute in parallel (default: 3)"
    )
    
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Simulate execution without making changes"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Reduce output verbosity"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available plans"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_plans()
        return
    
    if not args.plan:
        parser.error("--plan is required (use --list to see available plans)")
    
    # Resolve plan path
    plan_path = args.plan
    if not plan_path.is_absolute():
        plan_path = PLANS_DIR / plan_path
    
    # Execute plan
    executor = PlanExecutor(
        plan_path=plan_path,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
        verbose=not args.quiet
    )
    
    success = executor.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
