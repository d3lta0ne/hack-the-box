import os
import shutil
from datetime import datetime
from setup_script.utils import slugify

def build_project(config):
    """
    Builds a project directory structure based on the provided configuration.
    This function creates a new project directory by copying a template folder,
    updates specific files with the provided configuration details, and generates
    environment variable files.
    Args:
        config (dict): A dictionary containing the project configuration. It should include:
            - 'category' (str): The category name for the project.
            - 'project_name' (str): The name of the project.
            - 'author' (str): The name of the author.
            - 'difficulty' (str): The difficulty level of the project.
            - 'env' (dict): A dictionary of environment variables to be written to vars.bash and .env files.
    Returns:
        None
    Side Effects:
        - Creates directories for the project.
        - Copies the TEMPLATE folder to the new project directory.
        - Updates the WRITEUP.md file with project-specific details.
        - Creates vars.bash and .env files with environment variables.
    Raises:
        None
    Notes:
        - If the project directory already exists, the function will print an error message and exit.
        - The WRITEUP.md file is updated with placeholders replaced by values from the config.
        - The current date is inserted into the WRITEUP.md file in MM/DD/YYYY format.
    """
    # Set the base directory to the root of the workspace
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(base_dir, 'setup_script', 'TEMPLATE')
    category_dir = os.path.join(base_dir, config['category'], config['difficulty'])
    project_dir = os.path.join(category_dir, slugify(config['project_name']))

    # Ensure category and difficulty directories exist
    os.makedirs(category_dir, exist_ok=True)

    # Check if project directory already exists
    if os.path.exists(project_dir):
        print(f"Error: The project directory '{project_dir}' already exists.")
        return

    # Copy TEMPLATE folder to new project directory
    shutil.copytree(template_dir, project_dir)

    # Update WRITEUP.md
    writeup_path = os.path.join(project_dir, 'writeup', 'WRITEUP.MD')
    if os.path.exists(writeup_path):
        with open(writeup_path, 'r', encoding='utf-8') as file:
            content = file.read()
        content = content.replace("[Challenge/Box Name]", config['project_name'])
        content = content.replace("[Created By]", config['author'])
        content = content.replace("[Difficulty Level]", config['difficulty'])
        content = content.replace("[2/17/2025]", datetime.now().strftime("%m/%d/%Y"))
        with open(writeup_path, 'w', encoding='utf-8') as file:
            file.write(content)

    # Create vars.bash
    vars_bash_path = os.path.join(project_dir, 'writeup', 'vars.bash')
    with open(vars_bash_path, 'w', encoding='utf-8') as file:
        for key, value in config['env'].items():
            file.write(f"export {key}={value}\n")

    # Create .env
    env_path = os.path.join(project_dir, '.env')
    with open(env_path, 'w', encoding='utf-8') as file:
        for key, value in config['env'].items():
            file.write(f"{key}={value}\n")
