import os
import re
import sys
import argparse
import json
import shutil
from datetime import datetime

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.shortcuts import clear
except ImportError:
    print("prompt_toolkit is not installed. Please install it with 'pip install prompt_toolkit' before running this script.")
    sys.exit(1)

DEBUG = False
VERBOSE = False
SESSION_LOG = []
STEP_STACK = []

class StepCancelled(Exception):
    pass

class StepBack(Exception):
    pass

class Prompter:
    def safe_prompt(self, prompt_text: str, allow_exit: bool = False) -> str:
        try:
            if DEBUG or VERBOSE:
                print(f"DEBUG: Prompting user with text: {prompt_text}")
            return prompt(f"{prompt_text} > ").strip()
        except KeyboardInterrupt as exc:
            if STEP_STACK:
                print("Returning to the previous step.")
                raise StepBack from exc
            else:
                print("Setup cancelled by user. Exiting.")
                raise StepCancelled from exc
        except EOFError as exc:
            if allow_exit:
                if DEBUG or VERBOSE:
                    print("DEBUG: EOF received with allow_exit=True. Exiting.")
                exit(0)
            raise StepCancelled from exc

    def get_input(self, title: str) -> str:
        return self.safe_prompt(title)

    def numbered_prompt(self, title: str, options: list[str]) -> str:
        try:
            print(f"\n{title}")
            for i, option in enumerate(options, 1):
                print(f" {i}. {option}")
            while True:
                choice = self.safe_prompt("Select an option")
                if VERBOSE:
                    print(f"VERBOSE: User selected: {choice}")
                if choice.isdigit() and 1 <= int(choice) <= len(options):
                    return options[int(choice) - 1]
                print("Invalid selection. Try again.")
        except StepBack:
            raise
        except StepCancelled:
            print("Step cancelled by user. Returning to the previous menu.")
            return None

class Utils:
    @staticmethod
    def sanitize_name(name):
        return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

    @staticmethod
    def slugify(name):
        return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

    @staticmethod
    def validate_ip(ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            n = int(part)
            if n < 0 or n > 255:
                return False
        return True

    @staticmethod
    def validate_port(port):
        try:
            p = int(port)
            return 1 <= p <= 65535
        except ValueError:
            return False

class FileManager:
    @staticmethod
    def update_vars_bash(file_path: str, variables: dict):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("#!/bin/bash\n\n")
            for var_key, var_value in variables.items():
                file.write(f"export {var_key}={var_value}\n")

    @staticmethod
    def update_readme(config):
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

class Builder:
    @staticmethod
    def build_project(config):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, 'TEMPLATE')
        category_name = config['category']
        if category_name == "Challenge":
            category_name = "Challenges"
        elif category_name == "Machine":
            category_name = "Machines"
        elif category_name == "Sherlock":
            category_name = "Sherlocks"
        category_dir = os.path.join(base_dir, category_name)

        if config['category'] == "Academy":
            project_dir = os.path.join(category_dir, config['tier'], config['level'], config['type'], Utils.slugify(config['project_name']))
        else:
            project_dir = os.path.join(category_dir, Utils.slugify(config['project_name']))

        os.makedirs(category_dir, exist_ok=True)

        if os.path.exists(project_dir):
            print(f"Error: The project directory '{project_dir}' already exists.")
            return

        shutil.copytree(template_dir, project_dir)

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

        vars_bash_path = os.path.join(project_dir, 'writeup', 'vars.bash')
        with open(vars_bash_path, 'w', encoding='utf-8') as file:
            for key, value in config['env'].items():
                file.write(f"export {key}={value}\n")

        env_path = os.path.join(project_dir, '.env')
        with open(env_path, 'w', encoding='utf-8') as file:
            for key, value in config['env'].items():
                file.write(f"{key}={value}\n")

class DefaultLoader:
    @staticmethod
    def load_and_prompt_defaults(defaults_path: str) -> dict:
        with open(defaults_path, encoding="utf-8") as f:
            defaults = json.load(f)

        p = Prompter()
        collected = {}
        keys = list(defaults.keys())
        i = 0
        while i < len(keys):
            key = keys[i]
            settings = defaults[key]
            STEP_STACK.append(key)
            try:
                if "choices" in settings:
                    val = p.numbered_prompt(settings["prompt"], settings["choices"])
                else:
                    val = p.get_input(f"{settings['prompt']} (default: {settings['default']})")
                    if not val:
                        val = settings["default"]
                collected[key] = val
                STEP_STACK.pop()
                i += 1
            except StepBack:
                STEP_STACK.pop()
                if i > 0:
                    i -= 1
                continue
        return collected

    @staticmethod
    def load_defaults() -> dict:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        defaults_path = os.path.join(script_dir, "defaults.json")
        return DefaultLoader.load_and_prompt_defaults(defaults_path)

def display_status(config, current_step, step_number, total_steps):
    clear()
    print("==============================")
    print(" Current Configuration Status")
    print("==============================")
    for key, value in config.items():
        if key != 'env':
            print(f"{key.capitalize()}: {value if value else '[Not set]'}")
    print("==============================")
    print(f" Step {step_number} of {total_steps}: {current_step.replace('_', ' ').title()}")
    print("==============================")
    print(" Press Ctrl+C to cancel or go back.")

def run_menu(debug, verbose):
    p = Prompter(debug, verbose)
    config = {"category": None, "project_name": None, "author": None, "difficulty": None, "env": {}, "tier": None, "level": None, "type": None}
    steps = ["category", "project_name"]
    academy_fields = ["tier", "level", "type", "difficulty"]
    other_fields = ["difficulty", "author"]
    total_steps = len(steps) + len(academy_fields) if "Academy" in steps else len(steps) + len(other_fields)
    try:
        while True:
            STEP_STACK.append("category")
            try:
                display_status(config, "category", 1, total_steps)
                config["category"] = p.numbered_prompt("Select the category", ["Challenge", "Machine", "Sherlock", "Academy"])
                STEP_STACK.pop()
                break
            except StepBack:
                STEP_STACK.pop()
                continue

        while True:
            STEP_STACK.append("project_name")
            try:
                display_status(config, "project_name", 2, total_steps)
                config["project_name"] = p.get_input("Enter the Project/Module name")
                STEP_STACK.pop()
                break
            except StepBack:
                STEP_STACK.pop()
                continue

        if config["category"] == "Academy":
            for field, prompt_text, choices in [
                ("tier", "Select Academy Tier", ["Tier 0", "Tier I", "Tier II", "Tier III", "Tier IV"]),
                ("level", "Select Academy Level", ["Fundamental", "Easy", "Medium", "Hard"]),
                ("type", "Select Academy Type", ["Offensive", "Defensive", "Purple", "General"]),
                ("difficulty", "Select the difficulty level", ["Informational", "Easy", "Medium", "Hard"])
            ]:
                while True:
                    STEP_STACK.append(field)
                    try:
                        step_number = steps.index(field) + 1
                        display_status(config, field, step_number, len(steps))
                        config[field] = p.numbered_prompt(prompt_text, choices)
                        STEP_STACK.pop()
                        break
                    except StepBack:
                        STEP_STACK.pop()
                        continue
        else:
            for field, prompt_text in [
                ("difficulty", "Select Academy Difficulty"),
                ("author", "Enter the author name")
            ]:
                while True:
                    STEP_STACK.append(field)
                    try:
                        step_number = steps.index(field) + 1
                        display_status(config, field, step_number, len(steps))
                        if field == "difficulty":
                            config[field] = p.numbered_prompt(prompt_text, ["Easy", "Medium", "Hard", "Insane"])
                        else:
                            config[field] = p.get_input(prompt_text)
                        STEP_STACK.pop()
                        break
                    except StepBack:
                        STEP_STACK.pop()
                        continue

        config["env"] = DefaultLoader.load_defaults()
        Builder.build_project(config)
        FileManager.update_readme(config)

    except StepCancelled:
        print("\nSetup cancelled by user. Exiting.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting cleanly.")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Project initializer")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()

    run_menu(args.debug, args.verbose)

if __name__ == "__main__":
    main()
