import PySide2.QtWidgets
import sys
import GuiWindowTest


def main():

    qt_app = PySide2.QtWidgets.QApplication(sys.argv)  # sys.argv is the list of command line arguments

    example = GuiWindowTest.Window()
    example.show()
    sys.exit(qt_app.exec_())


if __name__ == '__main__':
    main()
