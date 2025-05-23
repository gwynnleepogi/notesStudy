import requests

BASE_URL = 'http://127.0.0.1:5000/api/notes'

def display_menu():
    print("\nNote-Taking Application")
    print("-----------------------")
    print("1. View All Notes")
    print("2. View Specific Note")
    print("3. Add New Note")
    print("4. Update Existing Note")
    print("5. Delete Note")
    print("6. Mark Note as Important")
    print("7. Exit")
    print("-----------------------")

def get_all_notes():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        notes = response.json()
        if notes:
            print("\n--- All Notes ---")
            for note in notes:
                print(f"ID: {note['id']}")
                print(f"Title: {note['title']}")
                print(f"Subject: {note['subject']}")
                print(f"Date Created: {note.get('created_at', 'N/A')}")
                print(f"Important: {'Yes' if note['is_important'] else 'No'}")
                print("-" * 20)
        else:
            print("\nNo notes found.")
    except requests.exceptions.RequestException as e:
        print(f"\nError fetching notes: {e}")

def get_specific_note(note_id):
    try:
        response = requests.get(f"{BASE_URL}/{note_id}")
        response.raise_for_status()
        note = response.json()
        print("\n--- Note Details ---")
        print(f"ID: {note['id']}")
        print(f"Title: {note['title']}")
        print(f"Subject: {note['subject']}")
        print(f"Content: {note['content']}")
        print(f"Date Created: {note.get('created_at', 'N/A')}")
        print(f"Important: {'Yes' if note['is_important'] else 'No'}")
        print("-" * 20)
    except requests.exceptions.RequestException as e:
        if response.status_code == 404:
            print("\nNote not found.")
        else:
            print(f"\nError fetching note: {e}")
    except ValueError:
        print("\nInvalid note ID.")

def add_new_note():
    title = input("Enter note title: ")
    content = input("Enter note content: ")
    subject = input("Enter note subject: ")
    is_important_input = input("Mark as important? (yes/no): ").lower()
    is_important = True if is_important_input == 'yes' else False

    new_note = {
        'title': title,
        'content': content,
        'subject': subject,
        'is_important': is_important
    }

    try:
        response = requests.post(BASE_URL, json=new_note)
        response.raise_for_status()
        added_note = response.json()
        print("\n--- Note Added ---")
        print(f"ID: {added_note['id']}")
        print(f"Title: {added_note['title']}")
        print(f"Subject: {added_note['subject']}")
        print(f"Date Created: {added_note.get('created_at', 'N/A')}")
        print(f"Important: {'Yes' if added_note['is_important'] else 'No'}")
        print("-" * 20)
    except requests.exceptions.RequestException as e:
        print(f"\nError adding note: {e}")
    except ValueError:
        print("\nInvalid response received.")

def update_existing_note(note_id):
    try:
        response = requests.get(f"{BASE_URL}/{note_id}")
        response.raise_for_status()
        existing_note = response.json()
    except requests.exceptions.RequestException as e:
        if response.status_code == 404:
            print("\nNote not found.")
        else:
            print(f"\nError fetching note: {e}")
        return
    except ValueError:
        print("\nInvalid note ID.")
        return

    print("\n--- Update Note ---")
    print("Leave fields blank to keep current value.")
    new_title = input(f"New title ({existing_note['title']}): ")
    new_content = input(f"New content ({existing_note['content']}): ")
    new_subject = input(f"New subject ({existing_note['subject']}): ")
    is_important_input = input(f"Mark as important? ({'yes' if existing_note['is_important'] else 'no'}): ").lower()

    updated_data = {}
    if new_title:
        updated_data['title'] = new_title
    if new_content:
        updated_data['content'] = new_content
    if new_subject:
        updated_data['subject'] = new_subject
    if is_important_input == 'yes':
        updated_data['is_important'] = True
    elif is_important_input == 'no':
        updated_data['is_important'] = False

    if not updated_data:
        print("\nNo updates provided.")
        return

    try:
        response = requests.put(f"{BASE_URL}/{note_id}", json=updated_data)
        response.raise_for_status()
        updated_note = response.json()
        print("\n--- Note Updated ---")
        print(f"ID: {updated_note['id']}")
        print(f"Title: {updated_note['title']}")
        print(f"Subject: {updated_note['subject']}")
        print(f"Content: {updated_note['content']}")
        print(f"Date Created: {updated_note.get('created_at', 'N/A')}")
        print(f"Important: {'Yes' if updated_note['is_important'] else 'No'}")
        print("-" * 20)
    except requests.exceptions.RequestException as e:
        if response.status_code == 404:
            print("\nNote not found.")
        else:
            print(f"\nError updating note: {e}")
    except ValueError:
        print("\nInvalid response received.")

def delete_note(note_id):
    confirmation = input(f"Are you sure you want to delete note ID {note_id}? (yes/no): ").lower()
    if confirmation == 'yes':
        try:
            response = requests.delete(f"{BASE_URL}/{note_id}")
            response.raise_for_status()
            print("\nNote deleted successfully.")
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                print("\nNote not found.")
            else:
                print(f"\nError deleting note: {e}")
    else:
        print("\nDeletion cancelled.")

def mark_note_important(note_id):
    try:
        response = requests.patch(f"{BASE_URL}/{note_id}/important")
        response.raise_for_status()
        updated_note = response.json()
        print("\n--- Note Marked as Important ---")
        print(f"ID: {updated_note['id']}")
        print(f"Title: {updated_note['title']}")
        print(f"Subject: {updated_note['subject']}")
        print(f"Important: {'Yes' if updated_note['is_important'] else 'No'}")
        print("-" * 20)
    except requests.exceptions.RequestException as e:
        if response.status_code == 404:
            print("\nNote not found.")
        else:
            print(f"\nError marking note as important: {e}")
    except ValueError:
        print("\nInvalid response received.")

if __name__ == "__main__":
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            get_all_notes()
        elif choice == '2':
            note_id = input("Enter note ID to view: ")
            get_specific_note(note_id)
        elif choice == '3':
            add_new_note()
        elif choice == '4':
            note_id = input("Enter note ID to update: ")
            update_existing_note(note_id)
        elif choice == '5':
            note_id = input("Enter note ID to delete: ")
            delete_note(note_id)
        elif choice == '6':
            note_id = input("Enter note ID to mark as important: ")
            mark_note_important(note_id)
        elif choice == '7':
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")
