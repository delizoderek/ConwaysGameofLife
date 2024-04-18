import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QSlider,
    QLineEdit,
    QLabel,
)
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer

ON = 255
OFF = 0


class Square(QWidget):
    def __init__(self, val=0):
        super().__init__()
        self.value = val
        self.color = QColor(val, val, val)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.end()

    def mousePressEvent(self, event):
        if self.value == 0:
            self.setValue(255)
        else:
            self.setValue(0)

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val
        if val == 0:
            self.color = QColor('black')
        else:
            self.color = QColor('white')
        self.update()


class Grid(QWidget):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)  # Remove spaces between squares
        self.setLayout(self.grid_layout)
        self.updateGrid()

    def randomMatrix(self, n):
        return np.random.choice([ON, OFF], n * n, p=[0.2, 0.8]).reshape(n, n)

    def updateGrid(self):
        self.matrix = self.randomMatrix(self.n)
        self.squares = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                square = Square(self.matrix[i][j])
                square.mousePressEvent = lambda event, i=i, j=j: self.squarePressed(event, i, j)  # Update matrix when square is pressed
                self.grid_layout.addWidget(square, i, j)
                row.append(square)
            self.squares.append(row)

    def squarePressed(self, event, i, j):
        if self.matrix[i][j] == ON:
            self.matrix[i][j] = OFF
        else:
            self.matrix[i][j] = ON
        self.squares[i][j].setValue(self.matrix[i][j])

    def set_matrix(self, n):
        self.n = n
        for square in sum(self.squares, []):
            square.deleteLater()
        self.updateGrid()

    def update_matrix(self, newMatrix):
        self.matrix = newMatrix
        for i in range(self.n):
            for j in range(self.n):
                self.squares[i][j].setValue(newMatrix[i][j])


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.n = 10
        self.ON = 255
        self.OFF = 0
        self.grid = Grid(self.n)
        self.grid_size_input = QLineEdit()
        self.grid_size_button = QPushButton("Set grid size")
        self.start_button = QPushButton("Start")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(10, 500)
        self.slider.setValue(100)
        self.slider_label = QLabel(str(self.slider.value()))
        layout = QGridLayout()
        layout.addWidget(self.grid, 0, 0, 1, 3)
        layout.addWidget(QLabel("Grid size:"), 1, 0)
        layout.addWidget(self.grid_size_input, 1, 1)
        layout.addWidget(self.grid_size_button, 1, 2)
        layout.addWidget(QLabel("Update interval (ms):"), 2, 0)
        layout.addWidget(self.slider, 2, 1)
        layout.addWidget(self.slider_label, 2, 2)
        layout.addWidget(self.start_button, 3, 0, 1, 3)
        self.setLayout(layout)

        self.grid_size_button.clicked.connect(self.set_grid_size)
        self.start_button.clicked.connect(self.start_animation)
        self.slider.valueChanged.connect(self.update_timer_interval)
        self.slider.valueChanged.connect(lambda x: self.slider_label.setText(str(x)))

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        # Set the window size to fit the squares
        self.setMinimumSize(400, 400)  # Adjust this size as needed

    def update_timer_interval(self):
        self.timer.setInterval(self.slider.value())
        self.slider_label.setText(str(self.slider.value()))

    def update_timer_interval(self):
        self.timer.setInterval(self.slider.value())

    def set_grid_size(self):
        n = int(self.grid_size_input.text())
        self.n = n
        self.grid.set_matrix(n)

    def start_animation(self):
        if self.start_button.text() == "Start":
            self.start_button.setText("Stop")
            self.timer.start(self.slider.value())  # call update every x ms
        else:
            self.start_button.setText("Start")
            self.timer.stop()

    def update(self):
        # Implement your update function here
        N = self.n
        currMatrix = self.grid.matrix
        newMatrix = currMatrix.copy()
        for i in range(N):
            for j in range(N):
                # compute 8-neghbor sum
                total = int(
                    (
                        currMatrix[i, (j - 1) % N]
                        + currMatrix[i, (j + 1) % N]
                        + currMatrix[(i - 1) % N, j]
                        + currMatrix[(i + 1) % N, j]
                        + currMatrix[(i - 1) % N, (j - 1) % N]
                        + currMatrix[(i - 1) % N, (j + 1) % N]
                        + currMatrix[(i + 1) % N, (j - 1) % N]
                        + currMatrix[(i + 1) % N, (j + 1) % N]
                    )
                    / 255
                )

                # apply Conway's rules
                if currMatrix[i, j] == ON:
                    if (total < 2) or (total > 3):
                        newMatrix[i, j] = OFF
                else:
                    if total == 3:
                        newMatrix[i, j] = ON
        self.grid.update_matrix(newMatrix)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())