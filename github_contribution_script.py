import os
import random
import subprocess
from datetime import date, timedelta
from pathlib import Path

# Define the commit messages
MESSAGES = [
    "update docs",
    "minor fix", 
    "readme update",
    "clean up",
    "small tweak",
    "update",
    "fix typo",
    "formatting"
]

SCRIPT_DIR = Path(__file__).resolve().parent
README_PATH = SCRIPT_DIR / "README.md"

def toggle_trailing_space(filepath):
    """Toggle the trailing space in the file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.endswith(' '):
        content = content[:-1]
    else:
        content += ' '
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def make_commit(date_obj, message):
    """Make a commit on the given date with the given message."""
    date_str = date_obj.strftime("%Y-%m-%d 12:00:00")
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str

    # Make the script independent from the shell's current directory.
    toggle_trailing_space(README_PATH)

    subprocess.run(['git', 'add', str(README_PATH)], cwd=SCRIPT_DIR, env=env, check=True)
    subprocess.run(['git', 'commit', '-m', message], cwd=SCRIPT_DIR, env=env, check=True)


def validate_environment():
    """Fail fast when the script is not placed inside a git repository."""
    if not README_PATH.exists():
        raise FileNotFoundError(f"README.md not found next to the script: {README_PATH}")

    subprocess.run(
        ['git', 'rev-parse', '--is-inside-work-tree'],
        cwd=SCRIPT_DIR,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def main():
    validate_environment()
    start_date = date(2025, 1, 6)  # Monday, January 6, 2025
    end_date = date(2026, 5, 4)    # May 4, 2026
    
    current_week_start = start_date
    
    while current_week_start <= end_date:
        # Get the weekdays for this week (Mon-Fri)
        weekdays = [current_week_start + timedelta(days=i) for i in range(5)]
        
        # Randomly choose 3, 4, or 5 days
        num_days = random.choice([3, 4, 5])
        selected_days = random.sample(weekdays, num_days)
        
        # Sort the days to commit in order
        selected_days.sort()
        
        for day in selected_days:
            if day > end_date:
                continue
            # Random number of commits (1-8)
            num_commits = random.randint(1, 8)
            for _ in range(num_commits):
                message = random.choice(MESSAGES)
                make_commit(day, message)
        
        # Move to next week
        current_week_start += timedelta(days=7)

if __name__ == "__main__":
    main()
