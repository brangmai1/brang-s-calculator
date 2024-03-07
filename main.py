"""
1: the user will perform an action or request on our views
2: The view will tell the controller it has a user action
3: The controller will ge the user's request and queries the model
4: The model will process the controller query perform the required operation, and return an answer or result
5: The controller receives the model's answer and updates the view
6: The user sees the request
"""
# step one, we'll build the skeleton
# step two, finish the view, starting with the 4th commit for this file
# step three, create a basic controller starting with 10th commit for this file
# ToDo create the model
# ToDo complete the controller model -> controller -> view


import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from functools import partial

ERROR_MSG = 'ERROR'


class PyCalcUi(QMainWindow):
    def __init__(self):
        super().__init__()
        # Standard Basics
        self.setWindowTitle('BRANG\'S CALCULATOR')
        self.setFixedSize(350, 550)

        # Central Widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Create a display and add some buttons
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        # Widget
        self.display = QLineEdit()
        font = QtGui.QFont('Arial')
        font.setPointSize(46)
        self.display.setFont(font)

        # Standards
        self.display.setFixedSize(325, 75)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        # Added to general Layout
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()

        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),

                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),

                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),

                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4)
                   }
        # Use a for loop to add the buttons to the grid layout

        for btnText, pos in buttons.items():
            font = QtGui.QFont('Arial')
            font.setPointSize(32)
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(70, 70)
            self.buttons[btnText].setFont(font)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])

        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText("")


class PyCalcCtrl:
    def __init__(self, model, view):

        # Initialization of controller
        self._evaluate = model
        self._view = view

        # Signals and slots
        self._connectSignals()

    def _calculateResult(self):
        result = self._evaluate(expression = self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)


def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result


def main():

    # Out instance of above class
    pycalc = QApplication(sys.argv)

    # View
    view = PyCalcUi()
    view.show()

    # instance of model and controller
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view)

    # Main event loop
    sys.exit(pycalc.exec())


if __name__ == '__main__':
    main()