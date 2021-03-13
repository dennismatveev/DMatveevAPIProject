from PySide2.QtWidgets import QMainWindow, QAction, QMenu, QFileDialog, QMessageBox, QProgressBar
import DatabaseWork
import ApiData
import pathlib


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.progress = QProgressBar(self)
        self.setWindowTitle("Gui Interaction")
        self.setGeometry(300, 200, 500, 400)

        self.create_menu()

    def create_menu(self):
        main_menu = self.menuBar()
        update_menu = main_menu.addMenu('Update')
        visualize_menu = main_menu.addMenu("Visualize")
        exit_menu = main_menu.addMenu("Exit")

        update_api = QAction("Update Api DB", self)
        update_menu.addAction(update_api)
        update_api.triggered.connect(self.update_api_DB)

        update_xlsx = QAction("Update Xlsx DB", self)
        update_menu.addAction(update_xlsx)
        update_xlsx.triggered.connect(self.update_xlsx_DB_with_new_file)

        visualize_text_file = QMenu("Visualize TXT File", self)  # Make menubar with extended options

        visualize_ascending_order = QAction("Ascending Order", visualize_text_file)
        visualize_menu.addMenu(visualize_text_file)
        visualize_text_file.addAction(visualize_ascending_order)
        visualize_ascending_order.triggered.connect(self.close)  # still need to add function

        visualize_descending_order = QAction("Descending Order", visualize_text_file)
        visualize_text_file.addAction(visualize_descending_order)
        visualize_descending_order.triggered.connect(self.close)  # still need to add function

        visualize_map = QAction("Visualize Map", self)
        visualize_menu.addAction(visualize_map)
        visualize_map.triggered.connect(self.close)  # Still need to add function

        exit_action = QAction('Exit', self)
        exit_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close)

        self.progress.setGeometry(1, 22, 175, 20)

    def update_api_DB(self):

        conn, cursor = DatabaseWork.open_db("demo_db.sqlite")
        DatabaseWork.setup_api_db(cursor)
        DatabaseWork.populate_api_database(cursor, ApiData.get_data())
        DatabaseWork.close_db(conn)
        self.task_accomplished()

    def update_xlsx_DB_with_new_file(self):
        filename = QFileDialog.getOpenFileName(self, "Open Image", None, "Image Files *.xlsx")
        path = pathlib.PurePath(filename[0])
        file_name = path.name
        conn, cursor = DatabaseWork.open_db("demo_db.sqlite")
        DatabaseWork.setup_xls_db(cursor)
        DatabaseWork.update_db_from_xl(file_name, cursor)
        DatabaseWork.close_db(conn)
        self.task_accomplished()

    # May implement in future
    # def task_in_progress(self):
    #     completed = 0
    #     while completed < 100:
    #         completed += 0.00001
    #         self.progress.setValue(completed)

    def task_accomplished(self):
        message_box = QMessageBox(self)
        message_box.setText("Task Completed")
        message_box.setWindowTitle("Congratulations!")
        message_box.show()
