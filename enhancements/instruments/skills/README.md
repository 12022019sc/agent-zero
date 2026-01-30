# Agent Zero Skills

This directory contains 16 reusable Python skill modules that provide specialized capabilities for Agent Zero. Skills are modular, self-contained components that can be invoked by agents or commands to perform specific tasks.

## Skills Overview

### Testing Skills

#### 1. writing_tests.py
**Description**: Write comprehensive tests following the Testing Trophy methodology.

**Features**:
- Generate integration tests with real dependencies
- Generate E2E tests for critical paths
- Generate unit tests only for pure functions
- Use pytest framework with markers
- Support multiple test types (integration, e2e, unit)

**Usage**:
```python
from skills.writing_tests import execute_skill

# Generate tests for a function
result = execute_skill(
    function_name="my_function",
    test_types=["integration", "e2e"],
    output_path="tests/test_my_function.py"
)
```

#### 2. systematic_debugging.py
**Description**: Debug issues systematically with pattern recognition.

**Features**:
- Analyze code for bugs systematically
- Identify failure patterns
- Suggest debugging strategies
- Integrate with test failure analysis
- Provide step-by-step debugging process

**Usage**:
```python
from skills.systematic_debugging import execute_skill

# Debug an error
result = execute_skill(
    error_message="TypeError: unsupported operand type(s)",
    stack_trace="...",
    code_context="def my_function(): ...",
    log_path="logs/error.log"
)
```

### Code Quality Skills

#### 3. refactoring_code.py
**Description**: Refactor code safely with best practices.

**Features**:
- Identify code smells
- Suggest safe refactoring strategies
- Apply refactoring patterns
- Maintain behavior
- Generate refactoring reports

**Usage**:
```python
from skills.refactoring_code import execute_skill

# Refactor code
result = execute_skill(
    code_path="src/module.py",
    refactor_patterns=["extract_method", "rename_variable"],
    dry_run=True
)
```

#### 4. optimizing_performance.py
**Description**: Optimize code performance systematically.

**Features**:
- Profile code execution
- Identify bottlenecks
- Suggest optimizations
- Compare before/after performance
- Generate optimization reports

**Usage**:
```python
from skills.optimizing_performance import execute_skill

# Optimize performance
result = execute_skill(
    code_path="src/module.py",
    benchmark=True,
    optimization_level="aggressive"
)
```

### Planning Skills

#### 5. writing_plans.py
**Description**: Write structured implementation plans.

**Features**:
- Create structured implementation plans
- Support plan templates
- Generate task breakdowns
- Include time estimates
- Analyze dependencies

**Usage**:
```python
from skills.writing_plans import execute_skill

# Create a plan
result = execute_skill(
    plan_name="Implement Feature X",
    description="Add new feature for ...",
    template="feature",
    tasks=[
        "Design database schema",
        "Implement API endpoints",
        "Write tests"
    ]
)
```

#### 6. executing_plans.py
**Description**: Execute implementation plans with context management.

**Features**:
- Execute implementation plans
- Manage context between tasks
- Support batch execution
- Track progress
- Verify completion

**Usage**:
```python
from skills.executing_plans import execute_skill

# Execute a plan
result = execute_skill(
    plan_path="plans/2026-01-15-feature-x.md",
    batch_size=5,
    continue_on_error=True
)
```

### Documentation Skills

#### 7. documenting_code_comments.py
**Description**: Generate inline code documentation.

**Features**:
- Generate inline docstrings
- Document function parameters
- Document return values
- Add usage examples
- Follow style guides (PEP257, Google, NumPy)

**Usage**:
```python
from skills.documenting_code_comments import execute_skill

# Generate docstrings
result = execute_skill(
    code_path="src/module.py",
    style="google",
    include_examples=True
)
```

#### 8. documenting_systems.py
**Description**: Generate system-level documentation.

**Features**:
- Generate system architecture docs
- Document APIs and interfaces
- Create README files
- Generate user guides
- Support multiple output formats

**Usage**:
```python
from skills.documenting_systems import execute_skill

# Generate system documentation
result = execute_skill(
    project_path="/path/to/project",
    doc_types=["api", "architecture", "readme"],
    output_format="markdown"
)
```

### Design Skills

#### 9. architecting_systems.py
**Description**: Design system architectures.

**Features**:
- Design system architectures
- Generate component diagrams
- Document design decisions
- Suggest architectural patterns
- Analyze trade-offs

**Usage**:
```python
from skills.architecting_systems import execute_skill

# Design architecture
result = execute_skill(
    system_name="E-commerce Platform",
    requirements=["Scalability", "High availability"],
    components=["API Gateway", "Microservices", "Database"]
)
```

#### 10. design.py
**Description**: Design components and patterns.

**Features**:
- Design components and patterns
- Generate class diagrams
- Document interfaces
- Suggest design patterns
- Validate designs

**Usage**:
```python
from skills.design import execute_skill

# Design a component
result = execute_skill(
    component_name="UserService",
    interfaces=["create_user", "get_user", "update_user"],
    design_patterns=["Singleton", "Factory"]
)
```

### Additional Skills

#### 11. reading_logs.py
**Description**: Read and analyze log files.

**Features**:
- Read and parse log files
- Filter logs by level, time, pattern
- Identify errors and warnings
- Generate log summaries
- Extract relevant information

**Usage**:
```python
from skills.reading_logs import execute_skill

# Analyze logs
result = execute_skill(
    log_path="/var/log/application.log",
    level="ERROR",
    pattern="database",
    start_time="2026-01-15T10:00:00"
)
```

#### 12. handling_errors.py
**Description**: Handle errors systematically.

**Features**:
- Parse error messages
- Identify error types
- Suggest error handling strategies
- Generate error handlers
- Document error patterns

**Usage**:
```python
from skills.handling_errors import execute_skill

# Handle errors
result = execute_skill(
    error_message="ConnectionError: ...",
    context="API request failed",
    generate_handler=True
)
```

#### 13. migrating_code.py
**Description**: Migrate code between frameworks.

**Features**:
- Analyze source code
- Identify migration patterns
- Generate migration scripts
- Map APIs between frameworks
- Validate migrations

**Usage**:
```python
from skills.migrating_code import execute_skill

# Migrate code
result = execute_skill(
    source_path="old_framework",
    target_framework="new_framework",
    generate_script=True
)
```

#### 14. verification_before_completion.py
**Description**: Verify work before completion.

**Features**:
- Define verification criteria
- Check completion status
- Validate results
- Generate verification reports
- Ensure quality gates

**Usage**:
```python
from skills.verification_before_completion import execute_skill

# Verify completion
result = execute_skill(
    task="Implement feature X",
    criteria=["All tests pass", "Code reviewed"],
    strict_mode=True
)
```

#### 15. visualizing_with_mermaid.py
**Description**: Generate Mermaid diagrams.

**Features**:
- Generate Mermaid diagrams
- Support multiple diagram types
- Generate flowcharts, sequence diagrams
- Generate class diagrams, state diagrams
- Export to various formats

**Usage**:
```python
from skills.visualizing_with_mermaid import execute_skill

# Generate diagram
result = execute_skill(
    diagram_type="flowchart",
    nodes=["Start", "Process", "End"],
    edges=[["Start", "Process"], ["Process", "End"]],
    output_format="svg"
)
```

#### 16. condition_based_waiting.py
**Description**: Wait for conditions dynamically.

**Features**:
- Wait for conditions to be met
- Support timeouts
- Poll conditions periodically
- Handle timeouts gracefully
- Log wait progress

**Usage**:
```python
from skills.condition_based_waiting import execute_skill

# Wait for condition
result = execute_skill(
    condition=lambda: check_service_ready(),
    timeout=300,
    poll_interval=5
)
```

## Installation

All skills are located in `/home/shayne/agent-zero/usr/projects/agent_zero_enhancements_and_extensions/instruments/skills/`.

To use a skill in your code:

```python
from skills.<skill_name> import execute_skill

# Execute the skill directly
result = execute_skill(
    # skill-specific arguments
)
```

Or use the class-based approach:

```python
from skills.<skill_name> import <SkillName>

# Create an instance
skill = <SkillName>(config={...})

# Execute the skill
result = skill.execute(
    # skill-specific arguments
)
```

## Base Skill Class

All skills inherit from `BaseSkill` which provides:
- Logging configuration
- Error handling
- Result formatting
- Common utility methods

## Integration with Existing Instruments

Skills are designed to integrate seamlessly with existing Agent Zero instruments:

- **test.py** uses `writing_tests.py` and `systematic_debugging.py`
- **refactor.py** uses `refactoring_code.py` and `optimizing_performance.py`
- **plan.py** uses `writing_plans.py`
- **execute.py** uses `executing_plans.py`
- **document.py** uses `documenting_code_comments.py` and `documenting_systems.py`
- **design.py** uses `architecting_systems.py` and `design.py`
- **optimize.py** uses `optimizing_performance.py`

## Development Guidelines

### Creating New Skills

1. Inherit from `BaseSkill`
2. Implement the `execute()` method
3. Add comprehensive docstrings
4. Include error handling
5. Provide a convenience function `execute_skill()`

### Skill Structure

```python
"""
Skill: <skill_name>
Description: <brief description>

This skill provides <detailed description>.
"""

import logging
from typing import Any, Dict, List, Optional
from pathlib import Path
from base import BaseSkill

class <SkillName>(BaseSkill):
    """<Skill description>."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the skill."""
        super().__init__(config)
        # Additional initialization

    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute the skill."""
        # Implementation here
        pass

# Convenience function
def execute_skill(*args, **kwargs) -> Dict[str, Any]:
    """Execute the skill directly."""
    skill = <SkillName>()
    return skill.execute(*args, **kwargs)
```

## Contributing

When adding new skills:
1. Follow the existing structure
2. Add comprehensive documentation
3. Include usage examples
4. Test the skill independently
5. Update this README

## License

This module is part of the Agent Zero Enhancements and Extensions project.
