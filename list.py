import sys, os, subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

TITLE = "GAME"

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class LibraryList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{TITLE}s")
        self.resize(600, 200)
        self.folder_path = rf"C:\{TITLE}"

        layout = QVBoxLayout(self)
        self.list = QListWidget()
        layout.addWidget(self.list)

        self.populate_list()
        self.list.itemDoubleClicked.connect(self.launch_item)

    def populate_list(self):
        files = sorted(os.listdir(self.folder_path))
        for file in files:
            if not file.lower().endswith((".exe", ".lnk", ".ico")):
                continue
            full_path = os.path.join(self.folder_path, file)
            title = file.replace(".lnk", "")
            icon_path = resource_path(f"resources/{title}.ico")
            icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()
            item = QListWidgetItem(icon, title)
            item.setData(Qt.ItemDataRole.UserRole, full_path)
            self.list.addItem(item)

    def launch_item(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        try:
            subprocess.Popen(path, shell=True)
            QApplication.quit()
        except Exception as e:
            print(f"Launch failed: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = QIcon(resource_path(f"resources/{TITLE}.ico"))
    app.setWindowIcon(icon)
    win = LibraryList()
    win.setWindowIcon(icon)
    win.show()
    sys.exit(app.exec())
