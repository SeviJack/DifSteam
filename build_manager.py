import json, os, sys, subprocess
from PyQt6.QtWidgets import QApplication, QInputDialog, QFileDialog

CONFIG_FILE = "folders.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return []
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_folder_entry():
    name, ok = QInputDialog.getText(None, "Folder Name", "Enter folder name:")
    if not ok or not name:
        return None
    folder = QFileDialog.getExistingDirectory(None, "Select Folder")
    if not folder:
        return None
    resources = QFileDialog.getExistingDirectory(None, "Select Resources Folder")
    if not resources:
        return None
    return {"name": name, "folder": folder, "resources": resources}

def build_exe(entry):
    subprocess.run([
        "pyinstaller", "--onefile", "--noconsole",
        "--icon", os.path.join(entry["resources"], f"{entry['name']}.ico"),
        "--add-data", f"{entry['resources']};resources",
        "folder.py", "--name", entry["name"]
    ])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = load_config()

    choice, ok = QInputDialog.getItem(
        None, "Select Folder", "Choose existing or add new:",
        [e["name"] for e in config] + ["<Add new>"], 0, False
    )

    if ok:
        if choice == "<Add new>":
            entry = add_folder_entry()
            if entry:
                config.append(entry)
                save_config(config)
                build_exe(entry)
        else:
            entry = next(e for e in config if e["name"] == choice)
            build_exe(entry)
