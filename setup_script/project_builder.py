import os
import shutil
from datetime import datetime
from setup_script.utils import slugify

def build_project(config):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, 'TEMPLATE')
    category_dir = os.path.join(base_dir, config['category'])
    project_dir = os.path.join(category_dir, slugify(config['project_name']))

    # Ensure category directory exists
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
        with open(writeup_path, 'r') as file:
            content = file.read()
        content = content.replace("[Challenge/Box Name]", config['project_name'])
        content = content.replace("[Created By]", config['author'])
        content = content.replace("[Difficulty Level]", config['difficulty'])
        content = content.replace("[2/17/2025]", datetime.now().strftime("%m/%d/%Y"))
        with open(writeup_path, 'w') as file:
            file.write(content)

    # Create vars.bash
    vars_bash_path = os.path.join(project_dir, 'writeup', 'vars.bash')
    with open(vars_bash_path, 'w') as file:
        for key, value in config['env'].items():
            file.write(f"export {key}={value}\n")

    # Create .env
    env_path = os.path.join(project_dir, '.env')
    with open(env_path, 'w') as file:
        for key, value in config['env'].items():
            file.write(f"{key}={value}\n")
