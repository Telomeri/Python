import sys
from PyQt5.QtWidgets import QApplication
from GUI import Window

def main():
    global app
    app = QApplication(sys.argv) #Starts the program
    gui = Window()
    sys.exit(app.exec_())

    
if __name__ == '__main__':
    main()