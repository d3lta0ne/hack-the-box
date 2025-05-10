# This script provides functionality to update a README.md file by adding project entries under specified categories.
# Functions:
#     update_readme(config):
#         If the category already exists, the project is added to the category's list.
#             config (dict): A dictionary containing:

import os


def update_readme(config):
    """
    Updates the README.md file by adding a project entry under the specified category.
    If the category already exists in the README, the project is added to the category's list.
    If the category does not exist, it is created, and the project is added under it.
    Args:
        config (dict): A dictionary containing the following keys:
            - 'category' (str): The category under which the project should be listed.
            - 'project_name' (str): The name of the project to be added.
    Raises:
        FileNotFoundError: If the README.md file does not exist in the base directory.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(base_dir, 'README.md')

    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        section_found = False
        for i, line in enumerate(lines):
            if line.strip().lower() == f"## {config['category'].lower()}":
                section_found = True
                lines.insert(i + 1, f"- [{config['project_name']}]({config['category']}/{config['project_name']}/)\n")
                break

        if not section_found:
            lines.append(f"\n## {config['category']}\n")
            lines.append(f"- [{config['project_name']}]({config['category']}/{config['project_name']}/)\n")

        with open(readme_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
