
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QCheckBox, QPushButton, QLabel, QLineEdit

from PyQt5 import QtCore, QtGui, QtWidgets


class TextProcessingWindow(QtWidgets.QDialog):
    def __init__(self, workspace):
        super().__init__()
        self.workspcae = workspace
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Text-Processing Window')
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        self.checkbox1 = QCheckBox('alpha', self)
        self.checkbox2 = QCheckBox('stop_words', self)
        self.checkbox3 = QCheckBox('lemmatizer', self)
        options = self.workspcae.text_processing_options
        checkboxes = [self.checkbox1, self.checkbox2, self.checkbox3]
        params = ['alpha', 'stop_words', 'lemmatizer']

        for el, param in zip(checkboxes, params):
            el.setChecked(options.get(param, False))
            layout.addWidget(el)



        apply_button = QPushButton('Apply', self)
        layout.addWidget(apply_button)
        apply_button.clicked.connect(self.apply_clicked)
        self.setLayout(layout)

        # set workspace params

    def apply_clicked(self):
        state1 =  self.checkbox1.isChecked()
        state2 =  self.checkbox2.isChecked()
        state3 =  self.checkbox3.isChecked()
        text_processing_options = {
            'alpha': state1,
            'stop_words': state2,
            'lemmatizer': state3
        }
        self.workspcae.set_text_processing_options(text_processing_options)
        print(f'alpha: {state1}')
        print(f'stop_words: {state2}')
        print(f'lemmatizer: {state3}')
        self.close()