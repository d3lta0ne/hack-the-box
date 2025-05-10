import sys
from typing import Dict, List, Optional, Union

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import clear

from setup_script.input_handler import (sanitize_name, validate_ip,
                                        validate_port)

CATEGORIES: List[str] = ["Challenge", "Academy", "Machine", "MISC"]
DIFFICULTIES: List[str] = ["Easy", "Medium", "Hard", "Insane"]
PLATFORMS: List[str] = ["Windows", "Linux", "macOS"]

SESSION_LOG: List[str] = []

class StepCancelled(Exception):
    pass

def safe_prompt(prompt_text: str, allow_exit: bool = False, allow_back: bool = True) -> str:
    try:
        return prompt(prompt_text).strip()
    except KeyboardInterrupt:
        if allow_exit:
            clear()
            print("Exiting program.")
            sys.exit(1)
        if allow_back:
            raise StepCancelled
        raise

def numbered_terminal_prompt(title: str, options: List[str], step_num: Optional[int] = None, total_steps: Optional[int] = None, allow_exit: bool = False) -> str:
    try:
        while True:
            clear()
            for line in SESSION_LOG:
                print(line)
            if step_num is not None and total_steps is not None:
                print(f"\n[Step {step_num} of {total_steps}]")
            print("\n" + title)
            for i, option in enumerate(options):
                print(f" {i+1}. {option}")
            print(f" {len(options) + 1}. Go Back")
            print(f" {len(options) + 2}. Quit")
            answer: str = safe_prompt("\nSelect option by number: ", allow_exit=allow_exit)
            if answer.isdigit():
                idx = int(answer)
                if 1 <= idx <= len(options):
                    return options[idx - 1]
                elif idx == len(options) + 1:
                    raise StepCancelled
                elif idx == len(options) + 2:
                    sys.exit(0)
            print("Invalid selection. Try again.")
    except StepCancelled:
        raise

def get_input(title: str, step_num: Optional[int] = None, total_steps: Optional[int] = None) -> str:
    try:
        clear()
        for line in SESSION_LOG:
            print(line)
        if step_num is not None and total_steps is not None:
            print(f"\n[Step {step_num} of {total_steps}]")
        print("\n" + title)
        return safe_prompt(" > ")
    except StepCancelled:
        raise

def run_menu() -> Optional[Dict[str, Union[str, Dict[str, str]]]]:
    try:
        total_steps: int = 6
        while True:
            SESSION_LOG.clear()
            try:
                current_step = 1
                category: Optional[str] = None
                platform: Optional[str] = None
                project_name: Optional[str] = None
                difficulty: Optional[str] = None
                author: Optional[str] = None
                env_vars: Dict[str, str] = {}

                while current_step >= 1:
                    if current_step == 1:
                        try:
                            category = numbered_terminal_prompt("Select a category:", CATEGORIES, step_num=1, total_steps=total_steps, allow_exit=True)
                            SESSION_LOG.append(f"Selected category: {category}")
                            current_step += 1
                        except StepCancelled:
                            return None

                    if current_step == 2:
                        try:
                            platform = numbered_terminal_prompt("Select the operating system:", PLATFORMS, step_num=2, total_steps=total_steps)
                            SESSION_LOG.append(f"Selected platform: {platform}")
                            current_step += 1
                        except StepCancelled:
                            SESSION_LOG.pop()
                            current_step -= 1
                            continue

                    if current_step == 3:
                        try:
                            raw_input = get_input("Enter the new project name", step_num=3, total_steps=total_steps)
                            if not raw_input:
                                raise StepCancelled
                            project_name = sanitize_name(raw_input)
                            SESSION_LOG.append(f"Project name: {project_name}")
                            current_step += 1
                        except StepCancelled:
                            SESSION_LOG.pop()
                            current_step -= 1
                            continue

                    if current_step == 4:
                        try:
                            difficulty = numbered_terminal_prompt("Select a difficulty level:", DIFFICULTIES, step_num=4, total_steps=total_steps)
                            SESSION_LOG.append(f"Selected difficulty: {difficulty}")
                            current_step += 1
                        except StepCancelled:
                            SESSION_LOG.pop()
                            current_step -= 1
                            continue

                    if current_step == 5:
                        try:
                            author_input = get_input("Enter the author or team name", step_num=5, total_steps=total_steps)
                            if not author_input:
                                raise StepCancelled
                            author = sanitize_name(author_input)
                            SESSION_LOG.append(f"Author: {author}")
                            current_step += 1
                        except StepCancelled:
                            SESSION_LOG.pop()
                            current_step -= 1
                            continue

                    if current_step == 6:
                        while True:
                            try:
                                key = get_input("Enter environment variable key (leave blank to finish)", step_num=6, total_steps=total_steps)
                                if not key:
                                    break
                                value = get_input(f"Enter value for {key}")
                                env_vars[key] = value
                                SESSION_LOG.append(f"ENV {key} = {value}")
                            except StepCancelled:
                                break
                        break

                if all([category, platform, project_name, difficulty, author]):
                    return {
                        "category": category,
                        "platform": platform,
                        "project_name": project_name,
                        "author": author,
                        "difficulty": difficulty,
                        "env": env_vars,
                        "target_path": f"{category}/{difficulty}/{project_name}"
                    }
                return None

            except StepCancelled:
                continue

    except KeyboardInterrupt:
        clear()
        print("User exited the session.")
        return None

if __name__ == "__main__":
    result = run_menu()
    if result is None:
        sys.exit(1)
    clear()
    print("\nFinal result:")
    print(result)