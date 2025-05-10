from setup_script.menu import run_menu
from setup_script.project_builder import build_project
from setup_script.readme_updater import update_readme

def main():
    # Run the interactive menu to collect user configuration
    config = run_menu()

    # Build the project based on the collected configuration
    build_project(config)

    # Update the root README.md with the new project entry
    update_readme(config)

if __name__ == "__main__":
    main()