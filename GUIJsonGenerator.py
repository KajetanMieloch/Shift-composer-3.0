import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton

class JSONGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.employee_layout = QVBoxLayout()
        self.employee_layout.addWidget(QLabel("Employee Details"))

        self.name_input = QLineEdit()
        self.employee_layout.addWidget(QLabel("Name:"))
        self.employee_layout.addWidget(self.name_input)

        self.surname_input = QLineEdit()
        self.employee_layout.addWidget(QLabel("Surname:"))
        self.employee_layout.addWidget(self.surname_input)

        self.department_input = QListWidget()
        self.department_input.addItems(["HR", "IT", "Security"])
        self.employee_layout.addWidget(QLabel("Department(s):"))
        self.employee_layout.addWidget(self.department_input)

        self.layout.addLayout(self.employee_layout)

        self.add_button = QPushButton("Add Employee")
        self.add_button.clicked.connect(self.addEmployee)
        self.layout.addWidget(self.add_button)

        self.generate_button = QPushButton("Generate JSON")
        self.generate_button.clicked.connect(self.generateJSON)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)
        self.setWindowTitle("JSON Generator")
        self.show()

        self.employees = []
        self.loadEmployees()  # Load employees from file when the application starts

    def addEmployee(self):
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        if name and surname:  # Only add employee if name and surname are provided
            employee = {
                "id": len(self.employees) + 1 if self.employees else 1,  # Incremented ID if employees exist
                "name": name,
                "surname": surname,
                "department": [item.text() for item in self.department_input.selectedItems()]
            }
            self.employees.append(employee)
            self.name_input.clear()
            self.surname_input.clear()

    def generateJSON(self):
        data = {"employees": self.employees}
        json_data = json.dumps(data, indent=4)
        with open("allemployees.json", "w") as json_file:
            json_file.write(json_data)
        print("JSON data saved to allemployees.json")

    def loadEmployees(self):
        try:
            with open("allemployees.json", "r") as json_file:
                data = json.load(json_file)
                self.employees = data.get("employees", [])
        except FileNotFoundError:
            print("No data file found.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JSONGenerator()
    sys.exit(app.exec_())
