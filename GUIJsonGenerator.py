import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QListWidget, 
                             QPushButton, QSizePolicy, QTabWidget, QAbstractItemView, QCalendarWidget, 
                             QDateEdit, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import QDate, Qt

class JSONGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_dates_schedule = []  # List to track selected dates for schedule
        self.initUI()

    def initUI(self):
        print("Initializing UI")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        self.createEmployeeTab()
        self.createEmployeePropertiesTab()
        self.createAvailabilityTab()
        self.createSchedulePropertiesTab()
        self.createPopulateScheduleTab()

        self.layout.addWidget(self.tab_widget)
        self.setLayout(self.layout)
        self.setWindowTitle("JSON Generator")
        self.show()

        self.employees = []
        self.loadEmployees()
        self.updateEmployeeIds()

    def createEmployeeTab(self):
        print("Creating Employee Tab")
        self.employee_tab = QWidget()
        self.employee_layout = QVBoxLayout(self.employee_tab)
        self.employee_layout.addWidget(QLabel("Employee Details"))

        self.name_input = QLineEdit()
        self.addInputField(self.employee_layout, "Name:", self.name_input)

        self.surname_input = QLineEdit()
        self.addInputField(self.employee_layout, "Surname:", self.surname_input)

        self.department_input = QListWidget()
        self.department_input.setSelectionMode(QAbstractItemView.MultiSelection)
        self.department_input.addItems(["HR", "IT", "Security"])
        self.addInputField(self.employee_layout, "Department(s):", self.department_input)

        self.add_button = QPushButton("Add Employee")
        self.add_button.clicked.connect(self.addEmployee)
        self.setButtonStyle(self.add_button)
        self.employee_layout.addWidget(self.add_button)

        self.generate_button = QPushButton("Generate JSON")
        self.generate_button.clicked.connect(self.generateJSON)
        self.setButtonStyle(self.generate_button)
        self.employee_layout.addWidget(self.generate_button)

        self.tab_widget.addTab(self.employee_tab, "Employees")

    def createEmployeePropertiesTab(self):
        print("Creating Employee Properties Tab")
        self.employee_properties_tab = QWidget()
        self.employee_properties_layout = QVBoxLayout(self.employee_properties_tab)
        self.employee_properties_layout.addWidget(QLabel("Select Employee ID:"))

        self.employee_id_list = QListWidget()
        self.employee_properties_layout.addWidget(self.employee_id_list)

        self.date_calendar = QCalendarWidget()
        self.date_calendar.setGridVisible(True)
        self.date_calendar.selectionChanged.connect(self.toggleDateSelection)
        self.addInputField(self.employee_properties_layout, "Select Date:", self.date_calendar)

        self.start_hour_input = QLineEdit()
        self.start_hour_input.setPlaceholderText("Start Hour (HH:MM)")
        self.addInputField(self.employee_properties_layout, "Start Hour:", self.start_hour_input)

        self.end_hour_input = QLineEdit()
        self.end_hour_input.setPlaceholderText("End Hour (HH:MM)")
        self.addInputField(self.employee_properties_layout, "End Hour:", self.end_hour_input)

        self.add_availability_button = QPushButton("Add Availability")
        self.add_availability_button.clicked.connect(self.addAvailability)
        self.setButtonStyle(self.add_availability_button)
        self.employee_properties_layout.addWidget(self.add_availability_button)

        self.add_same_hours_button = QPushButton("Add Same Hours for Selected Days")
        self.add_same_hours_button.clicked.connect(self.addSameHoursForSelectedDays)
        self.setButtonStyle(self.add_same_hours_button)
        self.employee_properties_layout.addWidget(self.add_same_hours_button)

        self.select_all_days_button = QPushButton("Select All Days for Next 30 Days")
        self.select_all_days_button.clicked.connect(self.selectAllDays)
        self.setButtonStyle(self.select_all_days_button)
        self.employee_properties_layout.addWidget(self.select_all_days_button)

        self.select_all_workdays_button = QPushButton("Select All Workdays for Next 30 Days")
        self.select_all_workdays_button.clicked.connect(self.selectAllWorkdays)
        self.setButtonStyle(self.select_all_workdays_button)
        self.employee_properties_layout.addWidget(self.select_all_workdays_button)

        self.select_all_weekends_button = QPushButton("Select All Weekends for Next 30 Days")
        self.select_all_weekends_button.clicked.connect(self.selectAllWeekends)
        self.setButtonStyle(self.select_all_weekends_button)
        self.employee_properties_layout.addWidget(self.select_all_weekends_button)

        self.generate_properties_button = QPushButton("Generate JSON")
        self.generate_properties_button.clicked.connect(self.generatePropertiesJSON)
        self.setButtonStyle(self.generate_properties_button)
        self.employee_properties_layout.addWidget(self.generate_properties_button)

        self.tab_widget.addTab(self.employee_properties_tab, "Employee Properties")
        self.tab_widget.currentChanged.connect(self.updateEmployeeIds)

    def createAvailabilityTab(self):
        print("Creating Availability Tab")
        self.availability_tab = QWidget()
        self.availability_layout = QVBoxLayout(self.availability_tab)

        self.availability_calendar = QCalendarWidget()
        self.availability_calendar.setGridVisible(True)
        self.availability_calendar.selectionChanged.connect(self.updateAvailabilityTable)
        self.availability_layout.addWidget(self.availability_calendar)

        self.availability_table = QTableWidget()
        self.availability_table.setColumnCount(4)
        self.availability_table.setHorizontalHeaderLabels(["Employee ID", "Name", "Availability", "Actions"])
        self.availability_layout.addWidget(self.availability_table)

        self.tab_widget.addTab(self.availability_tab, "View Availability")

    def createSchedulePropertiesTab(self):
        print("Creating Schedule Properties Tab")
        self.schedule_properties_tab = QWidget()
        self.schedule_properties_layout = QVBoxLayout(self.schedule_properties_tab)

        self.schedule_properties_layout.addWidget(QLabel("Select Schedule Date Range:"))

        self.schedule_start_date = QDateEdit()
        self.schedule_start_date.setCalendarPopup(True)
        self.schedule_start_date.setDate(QDate.currentDate())
        self.addInputField(self.schedule_properties_layout, "Start Date:", self.schedule_start_date)

        self.schedule_end_date = QDateEdit()
        self.schedule_end_date.setCalendarPopup(True)
        self.schedule_end_date.setDate(QDate.currentDate().addDays(7))
        self.addInputField(self.schedule_properties_layout, "End Date:", self.schedule_end_date)

        self.schedule_departments_list = QListWidget()
        self.schedule_departments_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.schedule_departments_list.addItems(["HR", "IT", "Security"])
        self.addInputField(self.schedule_properties_layout, "Departments:", self.schedule_departments_list)

        self.generate_schedule_button = QPushButton("Generate Schedule JSON")
        self.generate_schedule_button.clicked.connect(self.generateScheduleJSON)
        self.setButtonStyle(self.generate_schedule_button)
        self.schedule_properties_layout.addWidget(self.generate_schedule_button)

        self.tab_widget.addTab(self.schedule_properties_tab, "Generate Schedule")

    def createPopulateScheduleTab(self):
        print("Creating Populate Schedule Tab")
        self.populate_schedule_tab = QWidget()
        self.populate_schedule_layout = QVBoxLayout(self.populate_schedule_tab)

        self.populate_schedule_layout.addWidget(QLabel("Populate Schedule Work Hours"))

        self.populate_departments_list = QListWidget()
        self.populate_departments_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.populate_departments_list.addItems(["HR", "IT", "Security"])
        self.addInputField(self.populate_schedule_layout, "Departments:", self.populate_departments_list)

        self.date_calendar_schedule = QCalendarWidget()
        self.date_calendar_schedule.setGridVisible(True)
        self.date_calendar_schedule.selectionChanged.connect(self.toggleDateSelectionSchedule)
        self.addInputField(self.populate_schedule_layout, "Select Date(s):", self.date_calendar_schedule)

        self.start_hour_input_schedule = QLineEdit()
        self.start_hour_input_schedule.setPlaceholderText("Start Hour (HH:MM)")
        self.addInputField(self.populate_schedule_layout, "Start Hour:", self.start_hour_input_schedule)

        self.end_hour_input_schedule = QLineEdit()
        self.end_hour_input_schedule.setPlaceholderText("End Hour (HH:MM)")
        self.addInputField(self.populate_schedule_layout, "End Hour:", self.end_hour_input_schedule)

        self.populate_schedule_button = QPushButton("Populate Schedule JSON")
        self.populate_schedule_button.clicked.connect(self.populateScheduleJSON)
        self.setButtonStyle(self.populate_schedule_button)
        self.populate_schedule_layout.addWidget(self.populate_schedule_button)

        self.tab_widget.addTab(self.populate_schedule_tab, "Populate Schedule")

    def addInputField(self, layout, label_text, widget):
        layout.addWidget(QLabel(label_text))
        layout.addWidget(widget)

    def setButtonStyle(self, button):
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setMinimumHeight(30)  # Decrease button height
        button.setMinimumWidth(100)  # Decrease button width
        button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")

    def addEmployee(self):
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        departments = [item.text() for item in self.department_input.selectedItems()]
        if name and surname and departments:
            employee_id = len(self.employees) + 1
            self.employees.append({
                "id": employee_id,
                "name": name,
                "surname": surname,
                "departments": departments
            })
            self.name_input.clear()
            self.surname_input.clear()
            self.department_input.clearSelection()
            self.updateEmployeeIds()
            self.generateJSON()

    def generateJSON(self):
        data = {"employees": self.employees}
        with open("allemployees.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        print("JSON data saved to allemployees.json")

    def addAvailability(self):
        current_item = self.employee_id_list.currentItem()
        if current_item:
            employee_id = int(current_item.text().split()[0])
            selected_date = self.date_calendar.selectedDate().toString(Qt.ISODate)
            start_hour = self.start_hour_input.text().strip()
            end_hour = self.end_hour_input.text().strip()
            if start_hour and end_hour:
                self.addAvailabilityForEmployee(employee_id, selected_date, start_hour, end_hour)
                self.generatePropertiesJSON()

    def addAvailabilityForEmployee(self, employee_id, date, start_hour, end_hour):
        for employee in self.employees:
            if employee["id"] == employee_id:
                if "availability" not in employee:
                    employee["availability"] = []
                employee["availability"].append({
                    "date": date,
                    "start_hour": start_hour,
                    "end_hour": end_hour
                })

    def addSameHoursForSelectedDays(self):
        current_item = self.employee_id_list.currentItem()
        if current_item:
            employee_id = int(current_item.text().split()[0])
            start_hour = self.start_hour_input.text().strip()
            end_hour = self.end_hour_input.text().strip()
            if start_hour and end_hour:
                for date in self.selected_dates_schedule:
                    self.addAvailabilityForEmployee(employee_id, date.toString(Qt.ISODate), start_hour, end_hour)
                self.generatePropertiesJSON()
                self.selected_dates_schedule = []

    def toggleDateSelection(self):
        selected_date = self.date_calendar.selectedDate()
        if selected_date in self.selected_dates_schedule:
            self.selected_dates_schedule.remove(selected_date)
        else:
            self.selected_dates_schedule.append(selected_date)

    def toggleDateSelectionSchedule(self):
        selected_date = self.date_calendar_schedule.selectedDate()
        if selected_date in self.selected_dates_schedule:
            self.selected_dates_schedule.remove(selected_date)
        else:
            self.selected_dates_schedule.append(selected_date)

    def updateAvailabilityTable(self):
        selected_date = self.availability_calendar.selectedDate().toString(Qt.ISODate)
        self.availability_table.setRowCount(0)  # Clear existing rows
        for employee in self.employees:
            if "availability" in employee:
                for availability in employee["availability"]:
                    if availability["date"] == selected_date:
                        row_position = self.availability_table.rowCount()
                        self.availability_table.insertRow(row_position)
                        self.availability_table.setItem(row_position, 0, QTableWidgetItem(str(employee["id"])))
                        self.availability_table.setItem(row_position, 1, QTableWidgetItem(employee["name"]))
                        self.availability_table.setItem(row_position, 2, QTableWidgetItem(f"{availability['start_hour']} - {availability['end_hour']}"))

                        delete_button = QPushButton("Delete")
                        delete_button.clicked.connect(lambda ch, row=row_position: self.deleteAvailability(row))
                        self.availability_table.setCellWidget(row_position, 3, delete_button)

    def deleteAvailability(self, row):
        employee_id = int(self.availability_table.item(row, 0).text())
        availability_date = self.availability_calendar.selectedDate().toString(Qt.ISODate)
        for employee in self.employees:
            if employee["id"] == employee_id:
                if "availability" in employee:
                    employee["availability"] = [av for av in employee["availability"] if av["date"] != availability_date]
                    self.generatePropertiesJSON()
                    self.updateAvailabilityTable()
                    break

    def generatePropertiesJSON(self):
        data = {"employees": self.employees}
        with open("allemployeeswithproperties.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        print("JSON data saved to allemployeeswithproperties.json")

    def generateScheduleJSON(self):
        start_date = self.schedule_start_date.date().toString(Qt.ISODate)
        end_date = self.schedule_end_date.date().toString(Qt.ISODate)
        departments = [item.text() for item in self.schedule_departments_list.selectedItems()]
        schedule = {
            "start_date": start_date,
            "end_date": end_date,
            "departments": departments,
            "employees": self.employees
        }
        with open("employeeschedule.json", "w") as json_file:
            json.dump(schedule, json_file, indent=4)
        print("Schedule JSON data saved to employeeschedule.json")

    def populateScheduleJSON(self):
        departments = [item.text() for item in self.populate_departments_list.selectedItems()]
        start_hour = self.start_hour_input_schedule.text().strip()
        end_hour = self.end_hour_input_schedule.text().strip()
        schedule_data = {
            "departments": departments,
            "dates": []
        }
        for date in self.selected_dates_schedule:
            schedule_data["dates"].append({
                "date": date.toString(Qt.ISODate),
                "start_hour": start_hour,
                "end_hour": end_hour
            })
        with open("populatedschedule.json", "w") as json_file:
            json.dump(schedule_data, json_file, indent=4)
        print("Populated Schedule JSON data saved to populatedschedule.json")
        self.selected_dates_schedule = []

    def selectAllDays(self):
        start_date = QDate.currentDate()
        for i in range(30):
            self.selected_dates_schedule.append(start_date.addDays(i))

    def selectAllWorkdays(self):
        start_date = QDate.currentDate()
        for i in range(30):
            day = start_date.addDays(i)
            if day.dayOfWeek() < 6:  # Monday to Friday
                self.selected_dates_schedule.append(day)

    def selectAllWeekends(self):
        start_date = QDate.currentDate()
        for i in range(30):
            day = start_date.addDays(i)
            if day.dayOfWeek() >= 6:  # Saturday and Sunday
                self.selected_dates_schedule.append(day)

    def updateEmployeeIds(self):
        self.employee_id_list.clear()
        for employee in self.employees:
            self.employee_id_list.addItem(f"{employee['id']} - {employee['name']} {employee['surname']}")

    def loadEmployees(self):
        try:
            with open("allemployees.json", "r") as json_file:
                data = json.load(json_file)
                self.employees = data.get("employees", [])
        except FileNotFoundError:
            self.employees = []

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = JSONGenerator()
    sys.exit(app.exec_())
