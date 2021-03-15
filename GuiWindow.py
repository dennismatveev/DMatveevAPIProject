from PySide2.QtWidgets import QMainWindow, QAction, QMenu, QFileDialog, QMessageBox, QProgressBar, QListWidget, \
    QListWidgetItem
import DatabaseWork
import ApiData
import pathlib
import OrganizeComparisonData


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.progress = QProgressBar(self)
        self.setWindowTitle("Gui Interaction")
        self.setGeometry(300, 200, 900, 500)
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

        self.progress.setGeometry(1, 22, 175, 20)
        self.progress.setTextVisible(False)

    def visualize_actions(self, choice, category: str):
        visualize_text_file = QMenu("Visualize TXT File", self)  # Make menubar with extended options

        visualize_ascending_order = QAction("Ascending Order", visualize_text_file)
        choice.addMenu(visualize_text_file)
        visualize_text_file.addAction(visualize_ascending_order)
        if category == "grads":
            visualize_ascending_order.triggered.connect(self.colored_text_ascending_grads)
        elif category == "cohort":
            visualize_ascending_order.triggered.connect(self.colored_text_ascending_cohort())

        visualize_descending_order = QAction("Descending Order", visualize_text_file)
        visualize_text_file.addAction(visualize_descending_order)
        if category == "grads":
            visualize_descending_order.triggered.connect(self.colored_text_descending_grads)
        # elif category == "cohort":
        #     visualize_descending_order.triggered.connect(self.colored_text_descending_cohort())

        visualize_map = QAction("Visualize Map", choice)
        choice.addAction(visualize_map)
        visualize_map.triggered.connect(self.close)  # Still need to add function

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
        OrganizeComparisonData.compare_graduates_vs_num_jobs()
        dictionary = OrganizeComparisonData.sort_ascending_order()
        self.display_list(dictionary)

    def colored_text_descending_grads(self):
        OrganizeComparisonData.compare_graduates_vs_num_jobs()
        dictionary = OrganizeComparisonData.sort_descending_order()
        self.display_list(dictionary)

    def colored_text_ascending_cohort(self):
        OrganizeComparisonData.compare_graduates_vs_num_jobs()
        dictionary = OrganizeComparisonData.sort_ascending_order()
        self.display_list(dictionary)

    def colored_text_descending_cohort(self):
        OrganizeComparisonData.compare_graduates_vs_num_jobs()
        dictionary = OrganizeComparisonData.sort_descending_order()
        self.display_list(dictionary)

    def create_map(self):
        pass

    def display_list(self, dictionary):
        list_control = None
        my_list = [(k, v) for k, v in dictionary.items()]
        display_list = QListWidget(self)
        self.list_control = display_list
        for item in my_list:
            display_text = f"{item[0]}\t\t{item[1]}"
            list_item = QListWidgetItem(display_text, listview=self.list_control)
        display_list.resize(400, 350)
        display_list.move(100, 100)
        display_list.show()


    # May implem   ent in future       Label show and label close, and change cursor
    # shape
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
    no parameter can go to organizecomparison data
    differentiate between the two kinds of data to visualize
    
    need to display dictionary on pyside window
    
    need to create map to visualize data on web see previous proj
'''
