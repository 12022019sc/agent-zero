"""
New Project Enhancement Module

This module provides the functionality to create new Agent Zero projects
with the /newproject command.

Updated to fix issues with project creation not appearing in project picker.
"""

import os
import json
from datetime import datetime
from typing import Dict, Optional, Tuple


class NewProjectEnhancement:
    """Enhancement for creating new Agent Zero projects."""
    
    def __init__(self, base_dir: str = "/home/shayne/agent-zero/usr/projects"):
        """
        Initialize the NewProjectEnhancement.
        
        Args:
            base_dir: Base directory for projects
        """
        self.base_dir = base_dir
        self.default_color = "#9ef01a"
        
    def sanitize_project_name(self, name: str) -> str:
        """
        Sanitize the project name for use as a directory name.
        
        Args:
            name: The raw project name
            
        Returns:
            Sanitized project name
        """
        # Convert to lowercase and replace spaces with underscores
        sanitized = name.lower().strip().replace(" ", "_")
        # Remove any characters that aren't alphanumeric, underscores, or hyphens
        sanitized = "".join(c for c in sanitized if c.isalnum() or c in "_-")
        return sanitized
    
    def create_project_structure(self, project_path: str) -> bool:
        """
        Create the directory structure for a new project.
        
        Args:
            project_path: The full path to the project
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create main project directory
            os.makedirs(project_path, exist_ok=True)
            
            # Create .a0proj directory and subdirectories
            a0proj_path = os.path.join(project_path, ".a0proj")
            os.makedirs(a0proj_path, exist_ok=True)
            
            # Create .a0proj subdirectories
            os.makedirs(os.path.join(a0proj_path, "instructions"), exist_ok=True)
            
            # Create knowledge subdirectories at project root (not in .a0proj)
            knowledge_path = os.path.join(project_path, "knowledge")
            os.makedirs(knowledge_path, exist_ok=True)
            
            knowledge_subdirs = ["main", "longterm", "volatile"]
            for subdir in knowledge_subdirs:
                os.makedirs(os.path.join(knowledge_path, subdir), exist_ok=True)
                
            return True
        except Exception as e:
            print(f"Error creating project structure: {e}")
            return False
    
    def create_project_metadata(self, project_path: str, title: str, description: str,
                                instructions: str, color: Optional[str] = None) -> bool:
        """
        Create the project metadata files.
        
        Args:
            project_path: The full path to the project
            title: The project title
            description: The project description
            instructions: The project instructions
            color: The project color (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            a0proj_path = os.path.join(project_path, ".a0proj")
            
            # Set default color if not provided
            if color is None:
                color = self.default_color
            
            # Read default gitignore if available
            gitignore_content = ""
            try:
                with open("/home/shayne/agent-zero/conf/projects.default.gitignore", "r") as f:
                    gitignore_content = f.read()
            except:
                pass
            
            # Create project.json with exact format expected by the system
            project_data = {
                "title": title,
                "description": description,
                "instructions": instructions,
                "color": color,
                "memory": "own",
                "file_structure": {
                    "enabled": True,
                    "max_depth": 5,
                    "max_files": 20,
                    "max_folders": 20,
                    "max_lines": 250,
                    "gitignore": gitignore_content
                }
            }
            
            with open(os.path.join(a0proj_path, "project.json"), "w") as f:
                json.dump(project_data, f, indent=2)
            
            # Create description.txt for reference
            with open(os.path.join(a0proj_path, "description.txt"), "w") as f:
                f.write(description)
            
            # Create instructions.md for reference
            with open(os.path.join(a0proj_path, "instructions.md"), "w") as f:
                f.write(f"# {title}\n\n{instructions}")
                
            return True
        except Exception as e:
            print(f"Error creating project metadata: {e}")
            return False
    
    def create_project(self, name: str, title: Optional[str] = None,
                       description: Optional[str] = None,
                       instructions: Optional[str] = None,
                       color: Optional[str] = None) -> Tuple[bool, str, Optional[str]]:
        """
        Create a new Agent Zero project.
        
        Args:
            name: The project name (used for directory)
            title: The project title (defaults to name if not provided)
            description: The project description
            instructions: The project instructions
            color: The project color
            
        Returns:
            Tuple of (success, message, project_path)
        """
        # Sanitize the project name
        sanitized_name = self.sanitize_project_name(name)
        project_path = os.path.join(self.base_dir, sanitized_name)
        
        # Check if project already exists
        if os.path.exists(project_path):
            return False, f"Project '{sanitized_name}' already exists at {project_path}", None
        
        # Set defaults
        if title is None:
            title = name
        if description is None:
            description = f"Project for {name}"
        if instructions is None:
            instructions = "This project is focused on developing and implementing solutions."
        
        # Create project structure
        if not self.create_project_structure(project_path):
            return False, "Failed to create project structure", None
        
        # Create project metadata
        if not self.create_project_metadata(project_path, title, description, instructions, color):
            return False, "Failed to create project metadata", None
        
        return True, f"Project '{title}' created successfully at {project_path}", project_path


def create_new_project(name: str, title: Optional[str] = None,
                      description: Optional[str] = None,
                      instructions: Optional[str] = None,
                      color: Optional[str] = None) -> Dict:
    """
    Convenience function to create a new project.
    
    Args:
        name: The project name
        title: The project title
        description: The project description
        instructions: The project instructions
        color: The project color
        
    Returns:
        Dictionary with success status, message, and project path
    """
    enhancement = NewProjectEnhancement()
    success, message, project_path = enhancement.create_project(
        name, title, description, instructions, color
    )
    
    return {
        "success": success,
        "message": message,
        "project_path": project_path,
        "project_name": name
    }


if __name__ == "__main__":
    # Test the enhancement
    result = create_new_project(
        name="test_project",
        title="Test Project",
        description="This is a test project",
        instructions="Test instructions for the project"
    )
    print(json.dumps(result, indent=2))
