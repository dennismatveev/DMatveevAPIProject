from PySide2.QtWidgets import QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem, QFileDialog, QComboBox, \
    QHBoxLayout
from typing import List, Dict
import main


class WindowSelectAction(QWidget):
    def __init__(self):
        super().__init__()
        self.update_action = ""
        self.visualize_action = ""
        self.setWindowTitle("combo box demo")
        self.setGeometry(100, 100, 400, 300)
        self.setup_window()

    def setup_window(self):
        combo_box1 = QComboBox(self)
        combo_box2 = QComboBox(self)

        combo_box1.addItem("Select Which DB To Update")
        combo_box1.addItem("Update API DB")
        combo_box1.addItem("Update XLSX DB")
        combo_box1.move(50, 50)
        combo_box1.resize(combo_box1.sizeHint())
        combo_box1.currentIndexChanged.connect(self.selection_choice_update)

        combo_box2.addItem("Select Form of Data Visualization")
        combo_box2.addItem("Color Coded Text (Ascending)")
        combo_box2.addItem("Color Coded Text (Descending)")
        combo_box2.addItem("Render Map")
        combo_box2.move(50, 175)
        combo_box2.resize(combo_box2.sizeHint())
        combo_box2.currentIndexChanged.connect(self.selection_choice_visualize)

        quit_button = QPushButton("Quit Now", self)
        quit_button.move(270, 100)
        quit_button.resize(quit_button.sizeHint())
        quit_button.clicked.connect(QApplication.instance().quit)

    def selection_choice_update(self, combo_box):
        if combo_box == 1:
            self.update_action = 1
            main.populate_api_database(populate_api_database(cursor, main.get_data("https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="), api_table_name))
        elif combo_box == 2:
            self.update_action = 2
            file_name = self.choose_xlsx_file()
            main.update_db_from_xl(file_name, cursor, "Updated_XLSX_Data")

    def selection_choice_visualize(self, combo_box):
        if combo_box == 1:
            self.visualize_action = 1
            pass
        elif combo_box == 2:
            self.visualize_action = 2
            pass
        elif combo_box == 3:
            self.visualize_action = 3
            pass

    def choose_xlsx_file(self):
        filename = QFileDialog.getOpenFileName(self, "Open Image", None,"Image Files *.xlsx")
        return filename

