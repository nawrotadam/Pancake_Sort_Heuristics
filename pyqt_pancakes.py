from PyQt5.QtWidgets import *
import sys


class App(QWidget):
    def __init__(self, pancakes,pancakeSequence):
        number_of_flips = 0
        for el in pancakeSequence:
            first_split = pancakes[0:el]  # part which is not reversed
            second_split = pancakes[el:len(pancakes)]  # part prepared to reverse
            second_split.reverse()
            pancakes = first_split + second_split
            number_of_flips += 1
            super().__init__()
            self.pancakes = pancakes
            self.setWindowTitle("Naleśniki numer obrotu: " + str(number_of_flips))
            self.setGeometry(0, 0, 600, 200)
            for i in range(len(self.pancakes)):
                # reversed_number = (self.pancakes[len(self.pancakes) - 1] / 2 - self.pancakes[
                #     i] / 2)  # sets pancake x position, printed on screen
                button = QPushButton('', self)
                button.setStyleSheet("background-color : orange")
                button.resize(self.pancakes[i] * 40, 10)
                # button.move(0 + (40 * reversed_number), 0 + (i * 10))
                button.move(0, 0 + (i * 10))
            self.show()


def print_pancakes(pancakes,pancakeSequence):
    app = QApplication(sys.argv)
    ex = App(pancakes,pancakeSequence)
    sys.exit(app.exec_())
