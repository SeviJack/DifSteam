import sys, os, subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QPushButton, QSplitter, QMessageBox
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer

TITLE = "GAME"
HOURS = 2  # countdown hours

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def icon_for(title):
    png = resource_path(f"resources/{title}.png")
    ico = resource_path(f"resources/{title}.ico")
    return png if os.path.exists(png) else (ico if os.path.exists(ico) else None)

class LibraryList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{TITLE.lower()}s")
        self.resize(900, 500)
        self.folder_path = rf"C:\{TITLE}"
        self.remaining_seconds = 0

        # Split layout
        splitter = QSplitter(Qt.Orientation.Horizontal, self)

        # Left list
        self.list = QListWidget()
        self.list.setIconSize(QSize(32, 32))
        splitter.addWidget(self.list)

        # Right panel
        self.detail = QWidget()
        dlay = QVBoxLayout(self.detail)
        dlay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title + timer top bar
        top_bar = QHBoxLayout()
        self.title_lbl = QLabel("Select an item")
        self.title_lbl.setStyleSheet("font-size: 18px;")
        top_bar.addWidget(self.title_lbl)

        self.timer_lbl = QLabel("")
        self.timer_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.timer_lbl.setStyleSheet("font-size: 16px; color: #00ff00;")
        top_bar.addWidget(self.timer_lbl)
        dlay.addLayout(top_bar)

        # Details
        self.icon_lbl = QLabel()
        self.icon_lbl.setFixedSize(256, 256)
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.path_lbl = QLabel("")
        self.path_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.launch_btn = QPushButton("Launch")
        self.launch_btn.setEnabled(False)
        self.launch_btn.clicked.connect(self.launch_current)

        self.test_btn = QPushButton("Test Alert")
        self.test_btn.clicked.connect(self.alert)


        dlay.addWidget(self.icon_lbl)
        dlay.addWidget(self.path_lbl)
        dlay.addWidget(self.test_btn)
        dlay.addWidget(self.launch_btn)
        dlay.addStretch(1)

        splitter.addWidget(self.detail)
        splitter.setSizes([300, 600])

        root = QHBoxLayout(self)
        root.addWidget(splitter)

        # countdown timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # events
        self.populate_list()
        self.list.itemSelectionChanged.connect(self.update_detail)
        self.list.itemDoubleClicked.connect(self.launch_item)

        if self.list.count():
            self.list.setCurrentRow(0)

    def populate_list(self):
        self.list.clear()
        if not os.path.exists(self.folder_path):
            return
        for file in sorted(os.listdir(self.folder_path)):
            if not file.lower().endswith((".exe", ".lnk", ".url")):
                continue
            full_path = os.path.join(self.folder_path, file)
            title = os.path.splitext(file)[0]
            icon_path = icon_for(title)
            icon = QIcon(icon_path) if icon_path else QIcon()
            item = QListWidgetItem(icon, title)
            item.setData(Qt.ItemDataRole.UserRole, full_path)
            item.setData(Qt.ItemDataRole.UserRole + 1, icon_path or "")
            self.list.addItem(item)

    def update_detail(self):
        items = self.list.selectedItems()
        if not items:
            self.title_lbl.setText("Select an item")
            self.icon_lbl.clear()
            self.path_lbl.setText("")
            self.launch_btn.setEnabled(False)
            return
        item = items[0]
        title = item.text()
        path = item.data(Qt.ItemDataRole.UserRole)
        icon_path = item.data(Qt.ItemDataRole.UserRole + 1)

        self.title_lbl.setText(title)
        self.path_lbl.setText(path)
        self.launch_btn.setEnabled(True)

        if icon_path and os.path.exists(icon_path):
            pm = QPixmap(icon_path)
            if not pm.isNull():
                pm = pm.scaled(
                    self.icon_lbl.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.icon_lbl.setPixmap(pm)
            else:
                self.icon_lbl.clear()
        else:
            self.icon_lbl.clear()

    def launch_item(self, item):
        self._launch(item.data(Qt.ItemDataRole.UserRole))

    def launch_current(self):
        items = self.list.selectedItems()
        if items:
            self._launch(items[0].data(Qt.ItemDataRole.UserRole))

    def _launch(self, path):
        try:
            subprocess.Popen(path, shell=True)
            self.start_timer()
        except Exception as e:
            print(f"Launch failed: {e}")

    # countdown logic
    def start_timer(self):
        self.remaining_seconds = 10 #HOURS * 60 * 60
        self.update_timer_label()
        self.timer.start(1000)

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_label()
        else:
            self.timer.stop()
            self.timer_lbl.setText("Time’s up")
            self.alert()

    def alert(self):
        box = QMessageBox(self)
        box.setWindowTitle("Time's up!")
        box.setText("The countdown has finished.")
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()

    def update_timer_label(self):
        h, rem = divmod(self.remaining_seconds, 3600)
        m, s = divmod(rem, 60)
        self.timer_lbl.setText(f"{h:02}:{m:02}:{s:02}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #1e1e1e; color: white; }")
    icon = QIcon(resource_path(f"resources/{TITLE}.ico"))
    app.setWindowIcon(icon)
    win = LibraryList()
    win.setWindowIcon(icon)
    win.show()
    sys.exit(app.exec())
