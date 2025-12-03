import json
from datetime import datetime

# ==============================
#   CONFIGURATION
# ==============================

NOTES_FILE = "notes.json"

# Simple password for login (bonus: password protection)
# You can change it to whatever you want.
APP_PASSWORD = "1234"


# ==============================
#   FILE HANDLING
# ==============================

def load_notes():
    """
    Load notes from the JSON file.
    If the file does not exist or is invalid, return an empty list.
    """
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_notes(notes):
    """
    Save notes to the JSON file in pretty JSON format.
    """
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4, ensure_ascii=False)


# ==============================
#   UI HELPERS (ASCII STYLE)
# ==============================

def print_header(title):
    """
    Print a nice ASCII header for better readability (bonus UI).
    """
    print("\n" + "=" * 40)
    print(f"{title:^40}")   # center the title
    print("=" * 40)


def print_note(idx, note):
    """
    Print a single note in a consistent format.
    """
    print(f"\n[{idx}] {note['title']}")
    print(f"Date: {note.get('date', '')}")
    tags = note.get("tags", [])
    if tags:
        print("Tags:", ", ".join(tags))
    print("-" * 30)
    print(note["content"])
    print("-" * 30)


# ==============================
#   NOTE OPERATIONS
# ==============================

def add_note(notes):
    """
    Add a new note to the list.
    Bonus: automatically add timestamp using datetime.
    """
    print_header("Add a New Note")

    title = input("Title: ").strip()
    while title == "":
        print("Title cannot be empty.")
        title = input("Title: ").strip()

    content = input("Content: ").strip()

    tags_input = input("Tags (separated by commas, e.g. work,school,todo): ").strip()
    if tags_input:
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
    else:
        tags = []

    # Bonus: automatic timestamp
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    note = {
        "title": title,
        "content": content,
        "tags": tags,
        "date": date_str
    }

    notes.append(note)
    save_notes(notes)
    print("Note added successfully!")


def list_notes(notes):
    """
    Print all notes.
    """
    print_header("All Notes")

    if not notes:
        print("No notes yet.")
        return

    for idx, note in enumerate(notes, start=1):
        print_note(idx, note)


def search_notes(notes):
    """
    Search notes by keyword in title or content.
    Bonus: allow selecting a result to edit or delete.
    """
    print_header("Search Notes")

    keyword = input("Enter keyword: ").strip().lower()
    if not keyword:
        print("No keyword entered.")
        return

    # Collect (global_index, note) pairs
    results = []
    for idx, note in enumerate(notes, start=1):
        if keyword in note["title"].lower() or keyword in note["content"].lower():
            results.append((idx, note))

    if not results:
        print("No notes found for this keyword.")
        return

    print(f"\nFound {len(results)} note(s):")
    for idx, note in results:
        print_note(idx, note)

    # Bonus: choose one of the found notes to edit or delete
    action = input("\nDo you want to (e)dit or (d)elete one of these notes? (Enter to skip): ").strip().lower()
    if action not in ("e", "d"):
        return

    try:
        num = int(input("Enter the global note number: "))
    except ValueError:
        print("Invalid number.")
        return

    if num < 1 or num > len(notes):
        print("Note number out of range.")
        return

    if action == "e":
        edit_note(notes, num - 1)  # index in list (0-based)
    elif action == "d":
        delete_note_by_index(notes, num - 1)


def filter_by_tag(notes):
    """
    Filter notes by tag (case-insensitive).
    """
    print_header("Filter Notes by Tag")

    tag = input("Enter tag: ").strip().lower()
    if not tag:
        print("No tag entered.")
        return

    results = []
    for idx, note in enumerate(notes, start=1):
        note_tags_lower = [t.lower() for t in note.get("tags", [])]
        if tag in note_tags_lower:
            results.append((idx, note))

    if not results:
        print("No notes with this tag.")
        return

    print(f"\nFound {len(results)} note(s) with tag '{tag}':")
    for idx, note in results:
        print_note(idx, note)


def edit_note(notes, index=None):
    """
    Edit an existing note.
    If index is None, ask the user which note to edit.
    (Used both from main menu and from search bonus.)
    """
    print_header("Edit a Note")

    if not notes:
        print("No notes to edit.")
        return

    if index is None:
        # Show all notes and let user choose
        list_notes(notes)
        try:
            num = int(input("Enter the note number to edit: "))
        except ValueError:
            print("Invalid number.")
            return

        if num < 1 or num > len(notes):
            print("Note number out of range.")
            return

        index = num - 1  # convert to 0-based index

    note = notes[index]
    print(f"\nEditing note [{index + 1}] - {note['title']}")

    new_title = input(f"New title (Enter to keep: '{note['title']}'): ").strip()
    if new_title:
        note["title"] = new_title

    new_content = input("New content (Enter to keep current): ").strip()
    if new_content:
        note["content"] = new_content

    tags_input = input(
        f"New tags (comma separated) (Enter to keep: {', '.join(note.get('tags', []))}): "
    ).strip()
    if tags_input:
        note["tags"] = [t.strip() for t in tags_input.split(",") if t.strip()]

    save_notes(notes)
    print("Note updated successfully!")


def delete_note_by_index(notes, index):
    """
    Delete a note by its list index (0-based).
    This helper is used both from the main menu and from search bonus.
    """
    note = notes[index]
    confirm = input(f"Are you sure you want to delete '{note['title']}'? (y/n): ").strip().lower()
    if confirm == "y":
        notes.pop(index)
        save_notes(notes)
        print("Note deleted.")
    else:
        print("Delete cancelled.")


def delete_note(notes):
    """
    Delete a note by its number from the user (1-based).
    """
    print_header("Delete a Note")

    if not notes:
        print("No notes to delete.")
        return

    list_notes(notes)

    try:
        num = int(input("Enter the note number to delete: "))
    except ValueError:
        print("Invalid number.")
        return

    if num < 1 or num > len(notes):
        print("Note number out of range.")
        return

    delete_note_by_index(notes, num - 1)


# ==============================
#   BONUS: SORTING
# ==============================

def sort_notes(notes):
    """
    Bonus: sort notes by title or by date.
    The sort is in-place and saved to the JSON file.
    """
    print_header("Sort Notes")

    if not notes:
        print("No notes to sort.")
        return

    print("1. Sort by title (A-Z)")
    print("2. Sort by date (oldest first)")
    print("3. Sort by date (newest first)")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        notes.sort(key=lambda n: n["title"].lower())
        print("Notes sorted by title (A-Z).")
    elif choice == "2":
        notes.sort(key=lambda n: n.get("date", ""))
        print("Notes sorted by date (oldest first).")
    elif choice == "3":
        notes.sort(key=lambda n: n.get("date", ""), reverse=True)
        print("Notes sorted by date (newest first).")
    else:
        print("Invalid choice, no sorting applied.")
        return

    save_notes(notes)


# ==============================
#   MAIN MENU + LOGIN
# ==============================

def login():
    """
    Simple login for password protection (bonus).
    Very basic: compares the input to APP_PASSWORD.
    """
    print_header("Notebook Login")

    for attempt in range(3):
        pwd = input("Enter password: ").strip()
        if pwd == APP_PASSWORD:
            print("Login successful.\n")
            return True
        else:
            print("Wrong password.")
    print("Too many attempts. Exiting.")
    return False


def main():
    """
    Main loop of the application.
    Shows a menu and calls the appropriate functions.
    """
    # Bonus: password protection
    if not login():
        return

    notes = load_notes()

    while True:
        print_header("Personal Notebook Manager")
        print("1. Add a new note")
        print("2. List all notes")
        print("3. Search notes")
        print("4. Filter notes by tag")
        print("5. Edit a note")
        print("6. Delete a note")
        print("7. Sort notes (bonus)")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_note(notes)
        elif choice == "2":
            list_notes(notes)
        elif choice == "3":
            search_notes(notes)
        elif choice == "4":
            filter_by_tag(notes)
        elif choice == "5":
            edit_note(notes)
        elif choice == "6":
            delete_note(notes)
        elif choice == "7":
            sort_notes(notes)
        elif choice == "0":
            save_notes(notes)
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()

