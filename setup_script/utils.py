import re
import os
from datetime import datetime

def slugify(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def check_folder_exists(path):
    return os.path.exists(path)

def prompt_yes_no(prompt):
    while True:
        choice = input(f"{prompt} (y/n): ").lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        print("Invalid input. Please enter 'y' or 'n'.")
