import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer

class Square(QWidget):
    def __init__(self):
        super().__init__()
        self.color = QColor('black')

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.end()

    def mousePressEvent(self, event):
        if self.color == QColor('black'):
            self.color = QColor('white')
        else:
            self.color = QColor('black')
        self.update()

class Grid(QWidget):
    def __init__(self, n=10):
        super().__init__()
        self.n = n
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.squares = []
        for i in range(n):
            row = []
            for j in range(n):
                square = Square()
                self.grid_layout.addWidget(square, i, j)
                row.append(square)
            self.squares.append(row)

    def set_n(self, n):
        self.n = n
        for square in sum(self.squares, []):
            square.deleteLater()
        self.squares = []
        for i in range(n):
            row = []
            for j in range(n):
                square = Square()
                self.grid_layout.addWidget(square, i, j)
                row.append(square)
            self.squares.append(row)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = Grid()
        self.grid_size_input = QLineEdit()
        self.grid_size_button = QPushButton('Set grid size')
        self.start_button = QPushButton('Start')
        layout = QGridLayout()
        layout.addWidget(self.grid, 0, 0, 1, 3)
        layout.addWidget(QLabel('Grid size:'), 1, 0)
        layout.addWidget(self.grid_size_input, 1, 1)
        layout.addWidget(self.grid_size_button, 1, 2)
        layout.addWidget(self.start_button, 2, 0, 1, 3)
        self.setLayout(layout)

        self.grid_size_button.clicked.connect(self.set_grid_size)
        self.start_button.clicked.connect(self.start_animation)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

    def set_grid_size(self):
        n = int(self.grid_size_input.text())
        self.grid.set_n(n)

    def start_animation(self):
        if self.start_button.text() == 'Start':
            self.start_button.setText('Stop')
            self.timer.start(100)  # call update every 100ms
        else:
            self.start_button.setText('Start')
            self.timer.stop()

    def update(self):
        # Implement your update function here
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())