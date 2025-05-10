import curses

def _menu_logic(stdscr):
    # Remove curses.curs_set as it is not critical and causes compatibility issues
    stdscr.clear()
    stdscr.refresh()

    # Example menu logic
    categories = ["challenges", "academy", "machines", "misc"]
    difficulties = ["Easy", "Medium", "Hard", "Insane"]

    def display_menu(options, title):
        current_row = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, title, curses.A_BOLD)

            for idx, option in enumerate(options):
                if idx == current_row:
                    stdscr.addstr(idx + 2, 0, option, curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 2, 0, option)

            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(options) - 1:
                current_row += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                return options[current_row]

    def get_user_input(prompt):
        stdscr.clear()
        stdscr.addstr(0, 0, prompt, curses.A_BOLD)
        input_str = ""
        while True:
            key = stdscr.getch()
            if key in [10, 13]:  # Enter key
                break
            elif key in [8, 127]:  # Backspace key
                input_str = input_str[:-1]
                stdscr.clear()
                stdscr.addstr(0, 0, prompt + input_str, curses.A_BOLD)
            else:
                input_str += chr(key)
                stdscr.addstr(0, 0, prompt + input_str, curses.A_BOLD)
        return input_str

    # Step 1: Choose category
    category = display_menu(categories, "Select a category:")

    # Step 2: Enter project name
    project_name = get_user_input("Enter the new project name: ")

    # Step 3: Choose difficulty
    difficulty = display_menu(difficulties, "Select a difficulty level:")

    # Step 4: Enter author name
    author = get_user_input("Enter the author or team name: ")

    # Step 5: Enter environment variables
    env_vars = {}
    while True:
        key = get_user_input("Enter environment variable key (or press Enter to finish): ")
        if not key:
            break
        value = get_user_input(f"Enter value for {key}: ")
        env_vars[key] = value

    return {
        "category": category,
        "project_name": project_name,
        "author": author,
        "difficulty": difficulty,
        "env": env_vars
    }

def run_menu():
    return curses.wrapper(_menu_logic)
