import os

def update_readme(config):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(base_dir, 'README.md')

    if os.path.exists(readme_path):
        with open(readme_path, 'r') as file:
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

        with open(readme_path, 'w') as file:
            file.writelines(lines)
