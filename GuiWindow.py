from PySide2.QtWidgets import QMainWindow, QAction, QMenu, QFileDialog, QMessageBox, QProgressBar, QListWidget, \
    QListWidgetItem, QVBoxLayout, QLabel
#from Pyside2.QtGui import QColor
import DatabaseWork
import ApiData
import pathlib
import ComparisonDataGradsvsNumJobs
import ComparisonDataCohortvsSalary



class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gui Interaction")
        self.setGeometry(300, 200, 800, 500)
        self.list_control = None

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

        grads_vs_num_jobs = visualize_menu.addMenu("Compare NumCollegeGrads vs NumJobs per state")
        self.visualize_actions(grads_vs_num_jobs, "grads")

        cohort_bal_vs_25_percentile__salary = \
            visualize_menu.addMenu("Compare 3YearCohortBal vs 25PercentileSalary per state")
        self.visualize_actions(cohort_bal_vs_25_percentile__salary, "cohort")

        exit_action = QAction('Exit', self)
        exit_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close)

    def visualize_actions(self, choice, category: str):
        visualize_text_file = QMenu("Visualize TXT File", self)  # Make menubar with extended options

        visualize_ascending_order = QAction("Ascending Order", visualize_text_file)
        choice.addMenu(visualize_text_file)
        visualize_text_file.addAction(visualize_ascending_order)
        if category == "grads":
            visualize_ascending_order.triggered.connect(self.colored_text_ascending_grads)
        elif category == "cohort":
            visualize_ascending_order.triggered.connect(self.colored_text_ascending_cohort)

        visualize_descending_order = QAction("Descending Order", visualize_text_file)
        visualize_text_file.addAction(visualize_descending_order)
        if category == "grads":
            visualize_descending_order.triggered.connect(self.colored_text_descending_grads)
        elif category == "cohort":
            visualize_descending_order.triggered.connect(self.colored_text_descending_cohort)

        visualize_map = QAction("Visualize Map", choice)
        choice.addAction(visualize_map)
        if category == "grads":
            visualize_map.triggered.connect(self.create_map_grads)
        elif category == "cohort":
            visualize_map.triggered.connect(self.create_map_cohort)

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

    def colored_text_ascending_grads(self):
        ComparisonDataGradsvsNumJobs.compare_graduates_vs_num_jobs()
        dictionary = ComparisonDataGradsvsNumJobs.sort_ascending_order()
        self.display_list(dictionary)
        self.task_accomplished()

    def colored_text_descending_grads(self):
        ComparisonDataGradsvsNumJobs.compare_graduates_vs_num_jobs()
        dictionary = ComparisonDataGradsvsNumJobs.sort_descending_order()
        self.display_list(dictionary)
        self.task_accomplished()

    def create_map_grads(self):
        ComparisonDataGradsvsNumJobs.compare_graduates_vs_num_jobs()
        ComparisonDataGradsvsNumJobs.open_map_grads()
        self.task_accomplished()

    def colored_text_ascending_cohort(self):
        ComparisonDataCohortvsSalary.compare_cohort_decline_vs_percentile_salary()
        dictionary = ComparisonDataCohortvsSalary.sort_ascending_order()
        self.display_list(dictionary)
        self.task_accomplished()

    def colored_text_descending_cohort(self):
        ComparisonDataCohortvsSalary.compare_cohort_decline_vs_percentile_salary()
        dictionary = ComparisonDataCohortvsSalary.sort_descending_order()
        self.display_list(dictionary)
        self.task_accomplished()

    def create_map_cohort(self):
        ComparisonDataCohortvsSalary.compare_cohort_decline_vs_percentile_salary()
        ComparisonDataCohortvsSalary.open_map_cohort()
        self.task_accomplished()

    def display_list(self, dictionary):
        my_list = [(k, v) for k, v in dictionary.items()]
        display_list = QListWidget(self)
        label = QLabel(self)
        self.list_control = display_list
        for item in my_list:
            display_text = f"{item[0]}\t\t{item[1]}"
            text = QListWidgetItem(display_text, listview=self.list_control)
            #text.setForeground(QColor(255,0,0))


        display_list.resize(400, 350)
        display_list.move(100, 100)
        display_list.show()
        label.setText("State Abbrev:\t\t       Ratio:")
        label.setGeometry(100, 85, 300, 10)
        label.show()


    # May implem   ent in future       Label show and label close, and change cursor
    # shape
    #       self.progress.setGeometry(1, 22, 175, 20)
    #     self.progress.setTextVisible(False)
    # def task_in_progress(self):
    #     completed = 0
    #     while completed < 1000:
    #         completed += 1
    #         self.progress.setValue(completed)
    #         if completed == 999:
    #             completed = 0

    def task_accomplished(self):
        message_box = QMessageBox(self)
        message_box.setText("Task Completed")
        message_box.setWindowTitle("Congratulations!")
        message_box.show()


''' TO DO
    make some tests
'''
