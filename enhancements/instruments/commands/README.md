# Agent Zero Core Commands

A collection of 15 modular, reusable command-line instruments for Agent Zero.

## Overview

These commands provide comprehensive tools for testing, analysis, code quality, collaboration, planning, and execution within the Agent Zero framework.

## Installation

All commands are located in `instruments/commands/` and are executable:

```bash
cd /home/shayne/agent-zero/usr/projects/agent_zero_enhancements_and_extensions/instruments/commands/
chmod +x *.py
```

## Commands

### Testing & Analysis Commands

#### test.py
Run tests with smart filtering and reporting.

```bash
# Run all tests
./test.py

# Run specific file
./test.py tests/test_example.py

# With markers and coverage
./test.py -k "test_login" --cov

# Parallel execution
./test.py --parallel -n auto

# Output format
./test.py --format json --output results.json
```

**Options:**
- `-k EXPRESSION`: Filter tests by expression
- `-m MARKER`: Run tests with marker
- `--cov`: Generate coverage report
- `--parallel -n N`: Parallel execution
- `--format FORMAT`: Output format (text, json)

#### explain.py
Explain code, systems, or technical concepts.

```bash
# Explain a file
./explain.py src/module.py

# Explain function
./explain.py src/module.py --function my_function

# Complexity level
./explain.py src/module.py --level detailed

# Output format
./explain.py src/module.py --format markdown
```

**Options:**
- `--function NAME`: Explain specific function
- `--level LEVEL`: Complexity (basic, detailed, expert)
- `--format FORMAT`: Output format

#### debug.py
Debug code issues systematically.

```bash
# Analyze code for bugs
./debug.py src/buggy.py

# Analyze test failures
./debug.py --analyze-failures pytest-report.xml

# Analyze logs
./debug.py --logs /var/log/app.log --pattern "ERROR"

# Interactive mode
./debug.py src/buggy.py --interactive
```

**Options:**
- `--analyze-failures FILE`: Analyze pytest failures
- `--logs PATH`: Analyze log files
- `--pattern PATTERN`: Search pattern
- `--interactive`: Interactive debugging

#### optimize.py
Optimize code for performance.

```bash
# Analyze performance
./optimize.py src/slow.py

# Profile code
./optimize.py src/slow.py --profile

# Benchmark
./optimize.py src/slow.py --benchmark

# Focus area
./optimize.py src/ --focus cpu
```

**Options:**
- `--profile`: Profile code execution
- `--benchmark`: Run benchmarks
- `--suggest`: Suggest only
- `--apply`: Apply automatically
- `--focus FOCUS`: cpu, memory, io, all

#### refactor.py
Refactor code for maintainability.

```bash
# Analyze code smells
./refactor.py src/module.py

--detect-smells

# Suggest refactoring
./refactor.py src/module.py --suggest

# Apply refactorings
./refactor.py src/module.py --apply

# Dry run
./refactor.py src/module.py --dry-run
```

**Options:**
- `--detect-smells`: Detect code smells
- `--suggest`: Suggest refactorings
- `--apply`: Apply changes
- `--dry-run`: Preview changes

### Code Quality Commands

#### review.py
Review code for quality and best practices.

```bash
# Review a file
./review.py src/module.py

# Review changes
./review.py --git-diff HEAD~1

# Specific checks
./review.py src/module.py --check style,security,complexity

# Output format
./review.py src/module.py --format json
```

**Options:**
- `--git-diff REF`: Review git changes
- `--check TYPES`: Comma-separated check types
- `--severity LEVEL`: Minimum severity
- `--format FORMAT`: Output format

#### commit.py
Generate commit messages based on changes.

```bash
# Generate commit message
./commit.py

# Specific type
./commit.py --type feat

# Include scope
./commit.py --scope api --type feat

# Use template
./commit.py --template conventional
```

**Options:**
- `--type TYPE`: Commit type (feat, fix, docs, etc.)
- `--scope SCOPE`: Commit scope
- `--template NAME`: Use template
- `--output FILE`: Write to file

#### deps.py
Analyze and manage dependencies.

```bash
# Check dependencies
./deps.py check

# Check for outdated
./deps.py check --outdated

# Security scan
./deps.py check --security

# Dependency tree
./deps.py tree --depth 2
```

**Options:**
- `--file PATH`: Dependency file
- `--outdated`: Check outdated packages
- `--security`: Check vulnerabilities
- `--unused`: Find unused deps
- `--depth N`: Tree depth

#### fix-issue.py
Fix reported issues systematically.

```bash
# Fix issue from description
./fix-issue.py "Login fails with invalid token"

# From file
./fix-issue.py --file issue-report.md

# Issue type
./fix-issue.py --type bug --priority high "Login fails"

# Create plan
./fix-issue.py "Login fails" --create-plan
```

**Options:**
- `-f, --file PATH`: Issue file
- `--type TYPE`: Issue type
- `--priority LEVEL`: Issue priority
- `--create-plan`: Create implementation plan
- `--auto-fix`: Attempt auto-fix

### Collaboration Commands

#### pr.py
Generate pull request descriptions.

```bash
# Generate PR description
./pr.py

# Specify base branch
./pr.py --base develop

# Include changelog
./pr.py --include-changelog

# Include commits
./pr.py --include-commits

# Output format
./pr.py --format markdown
```

**Options:**
- `--base BRANCH`: Base branch
- `--head BRANCH`: Head branch
- `----include-changelog`: Include changelog
- `--include-commits`: Include commit list
- `--format FORMAT`: markdown or json

#### document.py
Generate documentation.

```bash
# API documentation
./document.py src/module.py --type api

# README generation
./document.py . --type readme

# Architecture docs
./document.py src/ --type architecture

# Output format
./document.py src/ --format html --output-dir docs/
```

**Options:**
- `--type TYPE`: api, readme, inline, architecture
- `--format FORMAT`: markdown, html, rst
- `--output-dir PATH`: Output directory
- `--include-private`: Include private members
- `--toc`: Include table of contents

### Planning & Execution Commands

#### plan.py
Create implementation plans.

```bash
# Create plan for feature
./plan.py implement user authentication

# With breakdown
./plan.py "add payment gateway" --breakdown

# With estimates
./plan.py "migrate database" --breakdown --estimate

# Dependency analysis
./plan.py "refactor API" --dependencies
```

**Options:**
- `--template NAME`: Use plan template
- `--output FILE`: Output file
- `--breakdown`: Detailed breakdown
- `--estimate`: Time estimates
- `--dependencies`: Dependency analysis

#### execute.py
Execute implementation plans.

```bash
# Execute plan from file
./execute.py plan.md

# Execute specific step
./execute.py plan.md --step 3

# Dry run
./execute.py plan.md --dry-run

# Continue on error
./execute.py plan.md --continue-on-error
```

**Options:**
- `--step N`: Execute specific step
- `--dry-run`: Preview execution
- `--continue-on-error`: Don't stop on errors
- `--log-file PATH`: Execution log
- `--batch`: Batch execution

#### design.py
Design systems and architectures.

```bash
# System architecture
./design.py "e-commerce platform" --type architecture

# API design
./design.py "REST API" --type api

# Microservices
./design.py "user service" --type microservices

# With diagrams
./design.py "payment system" --diagram mermaid

# Trade-off analysis
./design.py "data pipeline" --include-tradeoffs
```

**Options:**
- `--type TYPE`: architecture, api, database, microservices, monolith, component
- `--diagram TYPE`: mermaid, plantuml, none
- `--output-dir PATH`: Output directory
- `----adr`: Create Architecture Decision Records
- `--include-tradeoffs`: Trade-off analysis

## Base Module

All commands extend `BaseCommand` from `base.py`, which provides:

- Argument parsing with argparse
- Logging configuration
- Output formatting (text, json, markdown)
- File validation
- Project root detection

## Usage Patterns

### Chain Commands

```bash
# Test and review
./test.py && ./review.py src/

# Plan and execute
./plan.py "new feature" --breakdown > plan.md
./execute.py plan.md

# Debug and fix
./debug.py src/buggy.py
./fix-issue.py "Bug found in module" --create-plan
```

### Integration with Agent Zero

These commands can be called from Agent Zero instruments and skills:

```python
import subprocess

result = subprocess.run(
    ["./test.py", "--format", "json"],
    capture_output=True,
    text=True
)
```

## Common Options

All commands support:

- `--output-format FORMAT`: text, json, markdown
- `--output-file PATH`: Output to file
- `-v, --verbose`: Verbose output
- `-q, --quiet`: Quiet mode
- `--log-level LEVEL`: DEBUG, INFO, WARNING, ERROR

## Verification

Test each command:

```bash
for cmd in *.py; do
    echo "Testing $cmd..."
    python3 $cmd --help
    echo "---"
done
```

## License

Part of Agent Zero Enhancements and Extensions project.
