"""
Main module for the setup script.
This script serves as the entry point for the setup process. It orchestrates the following tasks:
1. Running an interactive menu to collect user configuration.
2. Building a project based on the collected configuration.
3. Updating the root README.md file with the new project entry.
Modules:
- `setup_script.menu`: Handles the interactive menu for collecting user input.
- `setup_script.project_builder`: Responsible for creating project files, directories, and setting up dependencies.
- `setup_script.readme_updater`: Updates the README.md file with details of the newly created project.
Functions:
- `main()`: Executes the setup process by calling the appropriate modules in sequence.
Usage:
Run this script directly to start the setup process.
"""

from setup_script.menu import run_menu
from setup_script.project_builder import build_project
from setup_script.readme_updater import update_readme


def main():
    """Main function to execute the setup script."""

    # Run the interactive menu to collect user configuration
    config = run_menu()

    # Build the project based on the collected configuration
    build_project(config)

    # Update the root README.md with the new project entry
    update_readme(config)

if __name__ == "__main__":
    main()