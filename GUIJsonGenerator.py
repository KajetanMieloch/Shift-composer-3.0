import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QTabWidget, QAbstractItemView, QCalendarWidget


class JSONGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # First tab for adding employees
        self.createEmployeeTab()

        # Second tab for employee properties
        self.createEmployeePropertiesTab()

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
        self.employee_layout.addWidget(self.add_button)

        self.generate_button = QPushButton("Generate JSON")
        self.generate_button.clicked.connect(self.generateJSON)
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
        self.addInputField(self.employee_properties_layout, "Select Date:", self.date_calendar)

        self.start_hour_input = QLineEdit()
        self.start_hour_input.setPlaceholderText("Start Hour (HH:MM)")
        self.addInputField(self.employee_properties_layout, "Start Hour:", self.start_hour_input)

        self.end_hour_input = QLineEdit()
        self.end_hour_input.setPlaceholderText("End Hour (HH:MM)")
        self.addInputField(self.employee_properties_layout, "End Hour:", self.end_hour_input)

        self.add_availability_button = QPushButton("Add Availability")
        self.add_availability_button.clicked.connect(self.addAvailability)
        self.employee_properties_layout.addWidget(self.add_availability_button)

        self.generate_properties_button = QPushButton("Generate JSON")
        self.generate_properties_button.clicked.connect(self.generatePropertiesJSON)
        self.employee_properties_layout.addWidget(self.generate_properties_button)

        self.tab_widget.addTab(self.employee_properties_tab, "Employee Properties")
        self.tab_widget.currentChanged.connect(self.updateEmployeeIds)

    def addInputField(self, layout, label_text, widget):
        layout.addWidget(QLabel(label_text))
        layout.addWidget(widget)

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

    def generateJSON(self):
        data = {"employees": self.employees}
        with open("allemployees.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        print("JSON data saved to allemployees.json")

    def addAvailability(self):
        current_item = self.employee_id_list.currentItem()
        if not current_item:
            return
        employee_id = int(current_item.text())
        date = self.date_calendar.selectedDate().toString("yyyy-MM-dd")
        start_hour = self.start_hour_input.text() or "All"
        end_hour = self.end_hour_input.text() or "All"
        for employee in self.employees:
            if employee["id"] == employee_id:
                if "availability" not in employee:
                    employee["availability"] = {}
                employee["availability"][date] = {
                    "startHour": start_hour,
                    "endHour": end_hour
                }
                break

    def generatePropertiesJSON(self):
        availability_data = [
            {"id": employee["id"], "availability": employee.get("availability", {})}
            for employee in self.employees if "availability" in employee
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
            self.employee_id_list.addItem(str(employee["id"]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JSONGenerator()
    sys.exit(app.exec_())
