import sys, os, subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QScrollArea,
    QGridLayout, QLabel, QFrame 
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QCursor, QPalette, QColor,QIcon

CONFIG_FILE = "folders.json"
TITLE = "GAME"
def resource_path(relative_path):
    """Get absolute path to resource (works for PyInstaller and dev)."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class ClickableTile(QFrame):
    """Tile that displays an image and text, with click feedback."""
    def __init__(self, title, image_path=None, launch_path=None):
        super().__init__()
        self.launch_path = launch_path
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAutoFillBackground(True)

        # Layout and widgets
        layout = QVBoxLayout(self)
        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if image_path and os.path.exists(image_path):
            pix = QPixmap(image_path).scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)
            self.icon.setPixmap(pix)
        else:
            self.icon.setText("🗂️")  # fallback symbol

        self.label = QLabel(title)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon)
        layout.addWidget(self.label)

    def enterEvent(self, event):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2a2a2a"))
        self.setPalette(palette)

    def leaveEvent(self, event):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
        self.setPalette(palette)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setStyleSheet("background-color: #444;")
        elif event.button() == Qt.MouseButton.RightButton:
            print(f"Right-clicked: {self.launch_path}")
        

    def mouseReleaseEvent(self, event):
        self.setStyleSheet("")
        if event.button() == Qt.MouseButton.LeftButton and self.launch_path:
            try:
                subprocess.Popen(self.launch_path, shell=True)
                QApplication.quit()  # Close the app after launching
            except Exception as e:
                print(f"Launch failed: {e}")


class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(TITLE)
        self.resize(1000, 600)
        self.folder_path = rf"C:\{TITLE}"
        

        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.grid = QGridLayout(self.content)
        scroll.setWidget(self.content)
        layout.addWidget(scroll)

        self.populate_grid()

    def populate_grid(self):
        files = sorted(os.listdir(self.folder_path))
        print(files)
        row, col = 0, 0
        for file in files:
            if not file.lower().endswith((".exe", ".lnk", ".ico")):
                continue
            full_path = os.path.join(self.folder_path, file)
            title = file.replace(".lnk", "")
            image_path = resource_path(f"resources/{title}.ico")
            tile = ClickableTile(title=title, image_path=image_path, launch_path=full_path)
            self.grid.addWidget(tile, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #1e1e1e; color: white; }")
    win = LibraryApp()
    win.show()
    icon = QIcon(resource_path(f"resources/{TITLE}.ico"))
    app.setWindowIcon(icon)      # taskbar
    win.setWindowIcon(icon)      # title bar
    sys.exit(app.exec())