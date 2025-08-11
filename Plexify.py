import os
import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Expanded regex pattern to support multiple formats
FILENAME_PATTERN = re.compile(
    r'(?P<show>.+?)[. _-]+(?:[Ss](?P<season>\d{1,2})[Ee](?P<episode>\d{1,2})|(?P<season_alt>\d{1,2})x(?P<episode_alt>\d{1,2}))',
    re.IGNORECASE
)

def normalize_filename(filename):
    match = FILENAME_PATTERN.search(filename)
    if not match:
        return None

    show_raw = match.group('show')
    season = match.group('season') or match.group('season_alt')
    episode = match.group('episode') or match.group('episode_alt')
    ext = Path(filename).suffix

    show_clean = re.sub(r'[._-]+', ' ', show_raw).strip().title()
    new_name = f"{show_clean} - S{int(season):02d}E{int(episode):02d}{ext}"
    return new_name

def rename_files_in_directory(directory, log_widget=None):
    renamed = 0
    skipped = 0
    log_path = os.path.join(directory, "rename_log.txt")

    with open(log_path, "a", encoding="utf-8") as log:
        for file in os.listdir(directory):
            full_path = os.path.join(directory, file)
            if os.path.isfile(full_path):
                new_name = normalize_filename(file)
                if new_name:
                    new_path = os.path.join(directory, new_name)

                    # Handle duplicates
                    if os.path.exists(new_path):
                        base, ext = os.path.splitext(new_name)
                        counter = 1
                        while os.path.exists(os.path.join(directory, f"{base} ({counter}){ext}")):
                            counter += 1
                        new_name = f"{base} ({counter}){ext}"
                        new_path = os.path.join(directory, new_name)

                    try:
                        os.rename(full_path, new_path)
                        msg = f"✅ Renamed: {file} → {new_name}"
                        renamed += 1
                    except Exception as e:
                        msg = f"❌ Error renaming {file}: {e}"
                else:
                    msg = f"⚠️ Skipped: {file} (no match)"
                    skipped += 1

                log.write(msg + "\n")
                if log_widget:
                    log_widget.insert(tk.END, msg + "\n")
                    log_widget.see(tk.END)

    messagebox.showinfo("Done", f"Renamed: {renamed} files\nSkipped: {skipped} files\nLog saved to rename_log.txt")

def pick_folder_and_run():
    root = tk.Tk()
    root.title("TV Show Renamer")

    # GUI layout
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    label = tk.Label(frame, text="Select a folder containing TV show episodes:")
    label.pack()

    log_widget = scrolledtext.ScrolledText(frame, width=80, height=20)
    log_widget.pack(pady=10)

    def run_renamer():
        folder = filedialog.askdirectory(title="Select TV Show Folder")
        if folder:
            log_widget.delete(1.0, tk.END)
            rename_files_in_directory(folder, log_widget)
        else:
            messagebox.showwarning("Cancelled", "No folder selected.")

    button = tk.Button(frame, text="Choose Folder and Rename", command=run_renamer)
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    pick_folder_and_run()
