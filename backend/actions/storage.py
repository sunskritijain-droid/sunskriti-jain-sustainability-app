import json
import os

# The JSON file will live inside the "actions" app folder.
DATA_FILE = os.path.join(os.path.dirname(__file__), 'actions.json')


def load_actions():
    """
    Read the list of actions from the JSON file.
    Return a Python list of dictionaries.
    If the file doesn't exist or is empty/broken, return an empty list.
    """
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_actions(actions):
    """
    Save the list of action dictionaries to the JSON file.
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(actions, f, indent=2)


def next_id(actions):
    """
    Compute the next ID to use.
    If there are no actions yet, start at 1.
    Otherwise, take the max existing id and add 1.
    """
    if not actions:
        return 1
    return max(a['id'] for a in actions) + 1
