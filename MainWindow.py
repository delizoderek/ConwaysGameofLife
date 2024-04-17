import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer

class Square(QWidget):
    def __init__(self, val = 0):
        super().__init__()
        self.value = val
        self.color = QColor(val,val,val)

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
    def __init__(self, matrix):
        super().__init__()
        self.n = len(matrix)
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.squares = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                square = Square(matrix[i][j])
                self.grid_layout.addWidget(square, i, j)
                row.append(square)
            self.squares.append(row)

    def set_matrix(self, matrix):
        self.n = len(matrix)
        for square in sum(self.squares, []):
            square.deleteLater()
        self.squares = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                square = Square(matrix[i][j])
                self.grid_layout.addWidget(square, i, j)
                row.append(square)
            self.squares.append(row)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.n = 10
        self.matrix = np.random.choice([0,1], self.n * self.n, p=[0.2, 0.8]).reshape(
            self.n, self.n)
        self.grid = Grid(self.matrix)
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
        self.matrix = [[0]*n for _ in range(n)]
        self.grid.set_matrix(self.matrix)

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