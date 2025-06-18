import sys, time, threading, json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QSlider, QTextEdit
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QColor, QMouseEvent
from pynput import keyboard, mouse
import mouse as GHUB

current_pattern = []
current_speed = 1.0
total_steps = 5
shot_delay = 0.07
holding_alt = False
holding_lclick = False
running = True

def move_mouse(dx, dy):
    GHUB.mouse_move(0, int(dx), int(dy), 0)

def dynamic_multiplier(index, speed):
    return speed if index < 10 else speed * 0.75 if index < 20 else speed * 0.6

def smooth_step(dx, dy, steps, total_time, mult):
    dy *= 1.15
    for _ in range(steps):
        move_mouse((dx * mult) / steps, (dy * mult) / steps)
        time.sleep(total_time / steps)

def recoil_loop():
    global holding_alt, holding_lclick
    while running:
        if holding_alt and holding_lclick:
            for i, (x, y) in enumerate(current_pattern):
                if not (holding_alt and holding_lclick): break
                smooth_step(x, y, total_steps, shot_delay, dynamic_multiplier(i, current_speed))
        time.sleep(0.001)

def on_press(key):
    global holding_alt
    if key == keyboard.Key.alt_l:
        holding_alt = True

def on_release(key):
    global holding_alt
    if key == keyboard.Key.alt_l:
        holding_alt = False

def on_click(x, y, button, pressed):
    global holding_lclick
    if button == mouse.Button.left:
        holding_lclick = pressed

class RecoilCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.points = []

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(30, 30, 30))
        painter.setPen(QColor(200, 100, 255))
        for i in range(1, len(self.points)):
            painter.drawLine(*self.points[i - 1], *self.points[i])
        painter.setBrush(QColor(180, 80, 255))
        for x, y in self.points:
            painter.drawEllipse(x - 4, y - 4, 8, 8)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            point = event.position().toPoint()
            self.points.append((point.x(), point.y()))
        elif event.button() == Qt.RightButton and self.points:
            self.points.pop()
        self.update()

    def get_pattern(self):
        if not self.points: return []
        origin = self.points[0]
        return [(x - origin[0], y - origin[1]) for (x, y) in self.points[1:]]

    def set_pattern(self, pattern):
        self.points = []
        origin = (200, 200)
        self.points.append(origin)
        for dx, dy in pattern:
            last = self.points[-1]
            self.points.append((last[0] + dx, last[1] + dy))
        self.update()

    def clear(self):
        self.points = []
        self.update()

class RecoilGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("svhost.exe")
        self.setFixedSize(450, 550)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.old_pos = QPoint()
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #b084f7; font-family: Segoe UI; border-radius: 12px; }
            QPushButton, QSlider, QTextEdit {
                background-color: #1e1e1e; color: #b084f7; padding: 6px; border-radius: 6px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title_bar = QHBoxLayout()
        title = QLabel("Credit @IrisDMA")
        title.setStyleSheet("padding: 6px; font-size: 16px;")
        title_bar.addWidget(title)
        title_bar.addStretch()
        for txt, act in [("_", self.showMinimized), ("X", self.close)]:
            btn = QPushButton(txt)
            btn.setFixedSize(24, 24)
            btn.clicked.connect(act)
            title_bar.addWidget(btn)
        layout.addLayout(title_bar)

        self.canvas = RecoilCanvas()
        layout.addWidget(QLabel("Custom Recoil Path:"))
        layout.addWidget(self.canvas)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(500)
        self.speed_slider.setValue(100)
        layout.addWidget(QLabel("Speed"))
        layout.addWidget(self.speed_slider)

        self.share_box = QTextEdit()
        self.share_box.setPlaceholderText("Paste or copy recoil code here")
        layout.addWidget(self.share_box)

        row = QHBoxLayout()
        gen_btn = QPushButton("Generate Code")
        gen_btn.clicked.connect(self.generate_code)
        row.addWidget(gen_btn)

        load_btn = QPushButton("Load Code")
        load_btn.clicked.connect(self.load_code)
        row.addWidget(load_btn)

        clear_btn = QPushButton("Clear Canvas")
        clear_btn.clicked.connect(self.canvas.clear)
        row.addWidget(clear_btn)

        layout.addLayout(row)

    def generate_code(self):
        global current_pattern, current_speed
        pattern = self.canvas.get_pattern()
        speed = self.speed_slider.value() / 100
        code = json.dumps({"pattern": pattern, "speed": speed})
        self.share_box.setText(code)
        current_pattern = pattern
        current_speed = speed

    def load_code(self):
        global current_pattern, current_speed
        try:
            data = json.loads(self.share_box.toPlainText())
            self.canvas.set_pattern(data["pattern"])
            self.speed_slider.setValue(int(data["speed"] * 100))
            current_pattern = data["pattern"]
            current_speed = data["speed"]
        except Exception as e:
            self.share_box.setText(f"Error loading: {e}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.old_pos.isNull():
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = QPoint()

if __name__ == "__main__":
    GHUB.mouse_open()
    threading.Thread(target=recoil_loop, daemon=True).start()
    keyboard.Listener(on_press=on_press, on_release=on_release).start()
    mouse.Listener(on_click=on_click).start()
    app = QApplication(sys.argv)
    gui = RecoilGUI()
    gui.show()
    sys.exit(app.exec())
