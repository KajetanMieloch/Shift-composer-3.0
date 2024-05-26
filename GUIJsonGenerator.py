import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QTabWidget, 
                             QAbstractItemView, QCalendarWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QCheckBox,
                             QMessageBox, QSizePolicy, QInputDialog, QDateEdit)
from PyQt5.QtCore import QDate, Qt

class JSONGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_dates = []  # List to track selected dates
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)  # Make the window bigger
        self.layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # First tab for adding employees
        self.createEmployeeTab()

        # Second tab for employee properties
        self.createEmployeePropertiesTab()

        # Third tab for viewing availability
        self.createAvailabilityTab()

        # Fourth tab for generating schedule properties
        self.createSchedulePropertiesTab()

        # Fifth tab for populating schedule
        self.createPopulateScheduleTab()

        self.layout.addWidget(self.tab_widget)
        self.setLayout(self.layout)
        self.setWindowTitle("JSON Generator")
        self.show()

        self.employees = []
        self.loadEmployees()
        self.updateEmployeeIds()

    def createEmployeeTab(self):
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
        self.populate_schedule_tab = QWidget()
        self.populate_schedule_layout = QVBoxLayout(self.populate_schedule_tab)

        self.populate_schedule_layout.addWidget(QLabel("Populate Schedule Work Hours"))

        self.populate_departments_list = QListWidget()
        self.populate_departments_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.populate_departments_list.addItems(["HR", "IT", "Security"])
        self.addInputField(self.populate_schedule_layout, "Departments:", self.populate_departments_list)

        self.days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        self.work_hours_inputs = {}
        for day in self.days_of_week:
            self.work_hours_inputs[day] = {}
            start_hour_input = QLineEdit()
            start_hour_input.setPlaceholderText("Start Hour (HH:MM) or None")
            end_hour_input = QLineEdit()
            end_hour_input.setPlaceholderText("End Hour (HH:MM) or None")
            self.work_hours_inputs[day]["start"] = start_hour_input
            self.work_hours_inputs[day]["end"] = end_hour_input
            self.addInputField(self.populate_schedule_layout, f"{day.capitalize()} Start Hour:", start_hour_input)
            self.addInputField(self.populate_schedule_layout, f"{day.capitalize()} End Hour:", end_hour_input)

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

    def addEmployee(self):
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        if name and surname:
            employee = {
                "id": len(self.employees) + 1,
                "name": name,
                "surname": surname,
                "departments": [item.text() for item in self.department_input.selectedItems()]
            }
            self.employees.append(employee)
            self.name_input.clear()
            self.surname_input.clear()
            self.generateJSON()  # Save changes immediately

    def generateJSON(self):
        data = {"employees": self.employees}
        with open("allemployees.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        print("JSON data saved to allemployees.json")

    def addAvailability(self):
        current_item = self.employee_id_list.currentItem()
        if not current_item:
            return
        employee_id = int(current_item.data(0).split()[0])  # Extract ID from string
        selected_dates = self.selected_dates  # Use the custom list of selected dates
        start_hour = self.start_hour_input.text() or "All"
        end_hour = self.end_hour_input.text() or "All"

        employee = next((emp for emp in self.employees if emp["id"] == employee_id), None)
        if employee:
            if "availability" not in employee:
                employee["availability"] = {}
            for date in selected_dates:
                date_str = date.toString("yyyy-MM-dd")
                employee["availability"][date_str] = {
                    "startHour": start_hour,
                    "endHour": end_hour
                }
            self.generateJSON()  # Save changes immediately

    def addSameHoursForSelectedDays(self):
        self.addAvailability()

    def selectAllDays(self):
        self.selectDates(QDate.currentDate(), 30, lambda date: True)

    def selectAllWorkdays(self):
        self.selectDates(QDate.currentDate(), 30, lambda date: date.dayOfWeek() < 6)

    def selectAllWeekends(self):
        self.selectDates(QDate.currentDate(), 30, lambda date: date.dayOfWeek() >= 6)

    def selectDates(self, start_date, days, condition):
        self.selected_dates.clear()
        for i in range(days):
            date = start_date.addDays(i)
            if condition(date):
                self.selected_dates.append(date)
        self.updateSelectedDates()

    def updateSelectedDates(self):
        self.date_calendar.setSelectedDate(QDate())  # Clear current selection
        for date in self.selected_dates:
            self.date_calendar.setSelectedDate(date)

    def toggleDateSelection(self):
        selected_date = self.date_calendar.selectedDate()
        if selected_date in self.selected_dates:
            self.selected_dates.remove(selected_date)
        else:
            self.selected_dates.append(selected_date)
        self.updateSelectedDates()

    def generatePropertiesJSON(self):
        availability_data = [
            {"id": employee["id"], "availability": employee.get("availability", {})}
            for employee in self.employees
        ]
        with open("employeesproperties.json", "w") as json_file:
            json.dump({"employeesAva": availability_data}, json_file, indent=4)
        print("JSON data saved to employeesproperties.json")

    def loadEmployees(self):
        try:
            with open("allemployees.json", "r") as json_file:
                data = json.load(json_file)
                self.employees = data.get("employees", [])
        except FileNotFoundError:
            print("No data file found.")

    def updateEmployeeIds(self):
        self.employee_id_list.clear()
        for employee in self.employees:
            departments = ", ".join(employee["departments"])
            employee_info = f'{employee["id"]} ({employee["name"]} {employee["surname"]} [{departments}])'
            self.employee_id_list.addItem(employee_info)

    def updateAvailabilityTable(self):
        selected_date = self.availability_calendar.selectedDate().toString("yyyy-MM-dd")
        self.availability_table.setRowCount(0)

        row = 0
        for employee in self.employees:
            if "availability" in employee and selected_date in employee["availability"]:
                self.availability_table.insertRow(row)
                self.availability_table.setItem(row, 0, QTableWidgetItem(str(employee["id"])))
                self.availability_table.setItem(row, 1, QTableWidgetItem(f'{employee["name"]} {employee["surname"]}'))
                availability = employee["availability"][selected_date]
                self.availability_table.setItem(row, 2, QTableWidgetItem(f'{availability["startHour"]} - {availability["endHour"]}'))

                actions_layout = QHBoxLayout()
                actions_layout.setContentsMargins(0, 0, 0, 0)
                actions_layout.setSpacing(0)
                actions_layout.setAlignment(Qt.AlignCenter)
                actions_layout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
                delete_button = QPushButton("Delete")
                delete_button.setMaximumSize(100, 30)  # Set a maximum size for the buttons
                delete_button.clicked.connect(lambda _, e=employee, d=selected_date: self.deleteAvailability(e, d))
                actions_layout.addWidget(delete_button)

                delete_all_button = QPushButton("Delete All")
                delete_all_button.setMaximumSize(100, 30)
                delete_all_button.clicked.connect(lambda _, e=employee: self.deleteAllAvailability(e))
                actions_layout.addWidget(delete_all_button)

                update_button = QPushButton("Update")
                update_button.setMaximumSize(100, 30)
                update_button.clicked.connect(lambda _, e=employee, d=selected_date: self.updateAvailability(e, d))
                actions_layout.addWidget(update_button)

                actions_widget = QWidget()
                actions_widget.setLayout(actions_layout)
                self.availability_table.setCellWidget(row, 3, actions_widget)

                row += 1

    def deleteAvailability(self, employee, date):
        if "availability" in employee and date in employee["availability"]:
            del employee["availability"][date]
            self.generateJSON()
            self.updateAvailabilityTable()

    def deleteAllAvailability(self, employee):
        confirm = QMessageBox.question(self, 'Confirm Delete',
                                       f'Are you sure you want to delete ALL records for employee {employee["id"]} {employee["name"]} {employee["surname"]}?',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            if "availability" in employee:
                employee["availability"] = {}
                self.generateJSON()
                self.updateAvailabilityTable()

    def updateAvailability(self, employee, date):
        start_hour, ok = QInputDialog.getText(self, 'Update Start Hour', 'Enter new start hour (HH:MM):')
        if ok:
            end_hour, ok = QInputDialog.getText(self, 'Update End Hour', 'Enter new end hour (HH:MM):')
            if ok:
                employee["availability"][date] = {
                    "startHour": start_hour,
                    "endHour": end_hour
                }
                self.generateJSON()
                self.updateAvailabilityTable()

    def generateScheduleJSON(self):
        start_date = self.schedule_start_date.date().toString("yyyy-MM-dd")
        end_date = self.schedule_end_date.date().toString("yyyy-MM-dd")
        departments = [item.text() for item in self.schedule_departments_list.selectedItems()]

        schedule_properties = {
            "scheduleProperties": {
                "date": {
                    "from": start_date,
                    "to": end_date
                },
                "departments": [
                    {
                        "name": department,
                        "minEmployees": 1,  # Example values
                        "maxEmployees": 3,  # Example values
                        "workHours": {day: {"from": "None", "to": "None"} for day in self.days_of_week}
                    }
                    for department in departments
                ]
            }
        }

        with open("scheduleproperties.json", "w") as json_file:
            json.dump(schedule_properties, json_file, indent=4)
        print("JSON data saved to scheduleproperties.json")

    def populateScheduleJSON(self):
        try:
            with open("scheduleproperties.json", "r") as json_file:
                schedule_properties = json.load(json_file)
        except FileNotFoundError:
            print("No scheduleproperties.json file found.")
            return

        for department in schedule_properties["scheduleProperties"]["departments"]:
            if department["name"] in [item.text() for item in self.populate_departments_list.selectedItems()]:
                for day in self.days_of_week:
                    start_hour = self.work_hours_inputs[day]["start"].text() or "None"
                    end_hour = self.work_hours_inputs[day]["end"].text() or "None"
                    department["workHours"][day] = {"from": start_hour, "to": end_hour}

        with open("scheduleproperties.json", "w") as json_file:
            json.dump(schedule_properties, json_file, indent=4)
        print("JSON data updated in scheduleproperties.json")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JSONGenerator()
    sys.exit(app.exec_())
