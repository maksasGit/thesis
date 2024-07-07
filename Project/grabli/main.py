from PyQt5.QtWidgets import  QApplication
from mainWindow import MainWindow                             #   <--- MainWindow to create GUI
import sys

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



