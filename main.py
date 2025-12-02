import json
from datetime import datetime




NOTES_FILE = "notes.json"


# -----------------------
#   FILE HANDLING
# -----------------------
ט
def load_notes():
    """Load notes from the JSON file."""
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_notes(notes):
    """Save notes to the JSON file."""
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4, ensure_ascii=False)


# -----------------------
#   NOTE OPERATIONS
# -----------------------

def add_note(notes):
    """Add a new note to the list."""
    print("\n--- Add a New Note ---")
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

    # מוסיפים תאריך אוטומטי
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
    """Print all notes."""
    print("\n--- All Notes ---")
    if not notes:
        print("No notes yet.")
        return

    for idx, note in enumerate(notes, start=1):
        print(f"\n[{idx}] {note['title']}")
        print(f"Date: {note.get('date', '')}")
        if note.get("tags"):
            print("Tags:", ", ".join(note["tags"]))
        print("-" * 30)
        print(note["content"])
        print("-" * 30)


def search_notes(notes):
    """Search notes by keyword in title or content."""
    print("\n--- Search Notes ---")
    keyword = input("Enter keyword: ").strip().lower()

    if not keyword:
        print("No keyword entered.")
        return

    results = []
    for idx, note in enumerate(notes, start=1):
        if keyword in note["title"].lower() or keyword in note["content"].lower():
            results.append((idx, note))

    if not results:
        print("No notes found for this keyword.")
        return

    print(f"\nFound {len(results)} note(s):")
    for idx, note in results:
        print(f"\n[{idx}] {note['title']}")
        print(f"Date: {note.get('date', '')}")
        if note.get("tags"):
            print("Tags:", ", ".join(note["tags"]))
        print("-" * 30)
        print(note["content"])
        print("-" * 30)


def filter_by_tag(notes):
    """Filter notes by tag."""
    print("\n--- Filter Notes by Tag ---")
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
        print(f"\n[{idx}] {note['title']}")
        print(f"Date: {note.get('date', '')}")
        if note.get("tags"):
            print("Tags:", ", ".join(note["tags"]))
        print("-" * 30)
        print(note["content"])
        print("-" * 30)


def edit_note(notes):
    """Edit an existing note."""
    print("\n--- Edit a Note ---")
    if not notes:
        print("No notes to edit.")
        return

    list_notes(notes)

    try:
        num = int(input("Enter the note number to edit: "))
    except ValueError:
        print("Invalid number.")
        return

    if num < 1 or num > len(notes):
        print("Note number out of range.")
        return

    note = notes[num - 1]
    print(f"\nEditing note [{num}] - {note['title']}")

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


def delete_note(notes):
    """Delete a note by its number."""
    print("\n--- Delete a Note ---")
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

    note = notes[num - 1]
    confirm = input(f"Are you sure you want to delete '{note['title']}'? (y/n): ").strip().lower()
    if confirm == "y":
        notes.pop(num - 1)
        save_notes(notes)
        print("Note deleted.")
    else:
        print("Delete cancelled.")


# -----------------------
#   MAIN MENU LOOP
# -----------------------

def main():
    notes = load_notes()

    while True:
        print("\n--- Personal Notebook Manager ---")
        print("1. Add a new note")
        print("2. List all notes")
        print("3. Search notes")
        print("4. Filter notes by tag")
        print("5. Edit a note")
        print("6. Delete a note")
        print("0. Exit")

        choice = input("Enter your choice: ")

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
        elif choice == "0":
            save_notes(notes)
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
