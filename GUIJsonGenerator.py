import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QTabWidget, QAbstractItemView, QCalendarWidget

class JSONGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Tab widget to manage multiple tabs
        self.tab_widget = QTabWidget()

        # First tab for adding employees
        self.employee_tab = QWidget()
        self.employee_layout = QVBoxLayout(self.employee_tab)
        self.employee_layout.addWidget(QLabel("Employee Details"))
        self.name_input = QLineEdit()
        self.employee_layout.addWidget(QLabel("Name:"))
        self.employee_layout.addWidget(self.name_input)
        self.surname_input = QLineEdit()
        self.employee_layout.addWidget(QLabel("Surname:"))
        self.employee_layout.addWidget(self.surname_input)
        self.department_input = QListWidget()
        self.department_input.setSelectionMode(QAbstractItemView.MultiSelection)  # Set selection mode to allow multiple selections
        self.department_input.addItems(["HR", "IT", "Security"])
        self.employee_layout.addWidget(QLabel("Department(s):"))
        self.employee_layout.addWidget(self.department_input)
        self.add_button = QPushButton("Add Employee")
        self.add_button.clicked.connect(self.addEmployee)
        self.employee_layout.addWidget(self.add_button)
        self.generate_button = QPushButton("Generate JSON")
        self.generate_button.clicked.connect(self.generateJSON)
        self.employee_layout.addWidget(self.generate_button)
        self.tab_widget.addTab(self.employee_tab, "Employees")

        # Second tab for employee properties
        self.employee_properties_tab = QWidget()
        self.employee_properties_layout = QVBoxLayout(self.employee_properties_tab)
        self.employee_properties_layout.addWidget(QLabel("Select Employee ID:"))
        self.employee_id_list = QListWidget()
        self.employee_properties_layout.addWidget(self.employee_id_list)

        self.date_calendar = QCalendarWidget()
        self.date_calendar.setGridVisible(True)
        self.employee_properties_layout.addWidget(QLabel("Select Date:"))
        self.employee_properties_layout.addWidget(self.date_calendar)

        self.start_hour_input = QLineEdit()
        self.start_hour_input.setPlaceholderText("Start Hour (HH:MM)")
        self.employee_properties_layout.addWidget(QLabel("Start Hour:"))
        self.employee_properties_layout.addWidget(self.start_hour_input)

        self.end_hour_input = QLineEdit()
        self.end_hour_input.setPlaceholderText("End Hour (HH:MM)")
        self.employee_properties_layout.addWidget(QLabel("End Hour:"))
        self.employee_properties_layout.addWidget(self.end_hour_input)

        self.add_availability_button = QPushButton("Add Availability")
        self.add_availability_button.clicked.connect(self.addAvailability)
        self.employee_properties_layout.addWidget(self.add_availability_button)

        self.generate_properties_button = QPushButton("Generate JSON")
        self.generate_properties_button.clicked.connect(self.generatePropertiesJSON)
        self.employee_properties_layout.addWidget(self.generate_properties_button)

        self.tab_widget.addTab(self.employee_properties_tab, "Employee Properties")
        self.tab_widget.currentChanged.connect(self.updateEmployeeIds)  # Connect tab change event to update employee IDs

        self.layout.addWidget(self.tab_widget)

        self.setLayout(self.layout)
        self.setWindowTitle("JSON Generator")
        self.show()

        self.employees = []
        self.loadEmployees()  # Load employees from file when the application starts
        self.updateEmployeeIds()  # Update employee IDs when the application starts

    def addEmployee(self):
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        if name and surname:  # Only add employee if name and surname are provided
            employee = {
                "id": len(self.employees) + 1 if self.employees else 1,  # Incremented ID if employees exist
                "name": name,
                "surname": surname,
                "departments": [item.text() for item in self.department_input.selectedItems()]
            }
            self.employees.append(employee)
            self.name_input.clear()
            self.surname_input.clear()

    def generateJSON(self):
        start_date = self.start_date_calendar.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_date_calendar.selectedDate().toString("yyyy-MM-dd")
        data = {
            "employees": self.employees,
            "start_date": start_date,
            "end_date": end_date
        }
        json_data = json.dumps(data, indent=4)
        with open("allemployees.json", "w") as json_file:
            json_file.write(json_data)
        print("JSON data saved to allemployees.json")

    def addAvailability(self):
        employee_id = int(self.employee_id_list.currentItem().text())
        date = self.date_calendar.selectedDate().toString("yyyy-MM-dd")
        start_hour = self.start_hour_input.text()
        end_hour = self.end_hour_input.text()
        for employee in self.employees:
            if employee["id"] == employee_id:
                if "availability" not in employee:
                    employee["availability"] = {}
                if date in employee["availability"]:
                    employee["availability"][date]["startHour"] = start_hour if start_hour else "All"
                    employee["availability"][date]["endHour"] = end_hour if end_hour else "All"
                else:
                    employee["availability"][date] = {
                        "startHour": start_hour if start_hour else "All",
                        "endHour": end_hour if end_hour else "All"
                    }

    def generatePropertiesJSON(self):
        availability_data = []
        for employee in self.employees:
            if "availability" in employee:
                availability = {
                    "id": employee["id"],
                    "availability": employee["availability"]
                }
                availability_data.append(availability)

        json_data = json.dumps({"employeesAva": availability_data}, indent=4)
        with open("employeesproperties.json", "w") as json_file:
            json_file.write(json_data)
        print("JSON data saved to employeesproperties.json")

    def loadEmployees(self):
        try:
            with open("allemployees.json", "r") as json_file:
                data = json.load(json_file)
                self.employees = data.get("employees", [])
        except FileNotFoundError:
            print("No data file found.")

    def updateEmployeeIds(self):
        # Clear previous IDs
        self.employee_id_list.clear()
        # Add available employee IDs
        for employee in self.employees:
            self.employee_id_list.addItem(str(employee["id"]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JSONGenerator()
    sys.exit(app.exec_())
