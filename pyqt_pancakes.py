from PyQt5.QtWidgets import *
import sys


class App(QWidget):
    def __init__(self, pancakes):
        super().__init__()
        self.pancakes = pancakes
        self.setWindowTitle("Naleśniki")
        self.setGeometry(0, 0, 40 * pancakes[len(pancakes) - 1], 10 * len(pancakes))
        for i in range(len(self.pancakes)):
            reversed_number = (self.pancakes[len(self.pancakes) - 1] / 2 - self.pancakes[
                i] / 2)  # sets pancake x position, printed on screen
            button = QPushButton('', self)
            button.setStyleSheet("background-color : orange")
            button.resize(self.pancakes[i] * 40, 10)
            button.move(0 + (40 * reversed_number), 0 + (i * 10))
        self.show()


def print_pancakes(pancakes):
    pancakes = pancakes[::-1]
    app = QApplication(sys.argv)
    ex = App(pancakes)
    sys.exit(app.exec_())
