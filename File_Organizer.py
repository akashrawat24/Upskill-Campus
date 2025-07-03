import os
import shutil
import json
from tkinter import Tk, Label, Button, filedialog, messagebox

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".xls"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
}

MOVE_LOG_FILE = "move_log.json"  


def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return "Others"


def organize_files(directory):
    moved_files = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath):
            _, ext = os.path.splitext(filename)
            category = get_category(ext)

            category_folder = os.path.join(directory, category)
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)

            new_path = os.path.join(category_folder, filename)
            shutil.move(filepath, new_path)

            moved_files.append({"from": filepath, "to": new_path})
    with open(MOVE_LOG_FILE, "w") as log_file:
        json.dump(moved_files, log_file, indent=4)

    messagebox.showinfo("Success", "Files organized successfully and logged!")


def undo_last_action():
    if not os.path.exists(MOVE_LOG_FILE):
        messagebox.showwarning("Warning", "No move log found to undo.")
        return

    with open(MOVE_LOG_FILE, "r") as log_file:
        moved_files = json.load(log_file)

    for record in moved_files:
        try:
            shutil.move(record["to"], record["from"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move {record['to']} back.\n{str(e)}")

    os.remove(MOVE_LOG_FILE)
    messagebox.showinfo("Undo Complete", "All files have been moved back.")


def choose_and_organize():
    folder = filedialog.askdirectory(title="Select Directory to Organize")
    if folder:
        organize_files(folder)
    else:
        messagebox.showwarning("Warning", "No directory selected.")

root = Tk()
def create_gui():
    
    root.title("File Organizer")
    root.geometry("400x200")

    Label(root, text="File Organizer", font=("Arial", 16)).pack(pady=10)

    Button(root, text="Select Folder and Organize", command=choose_and_organize, width=30).pack(pady=10)
    Button(root, text="Undo Last Organization", command=undo_last_action, width=30).pack(pady=10)
    Button(root, text="Exit", command=root.destroy, width=30).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
