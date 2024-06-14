from PyQt5.QtWidgets import  QApplication
from mainWindow import MainWindow                             #   <--- MainWindow to create GUI
import sys


#TODO mb prints should be replaced on logs????


#TODO del bag of words
#TODO modify TF-IDF params -->  min_df , max_df
#TODO modify Word2vec params -->  vector_size, window, min_count, sg



def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



