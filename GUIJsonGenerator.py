import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QListWidget, QPushButton

class JSONGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.employee_layout = QVBoxLayout()
        self.employee_layout.addWidget(QLabel("Employee Details"))

        self.id_slider = QSlider()
        self.id_slider.setOrientation(1)  # Vertical slider
        self.id_slider.setRange(1, 100)
        self.employee_layout.addWidget(QLabel("ID:"))
        self.employee_layout.addWidget(self.id_slider)

        self.name_input = QListWidget()
        self.name_input.addItems(["John", "Jane", "Mike", "Alex", "Emily", "Ryan"])
        self.employee_layout.addWidget(QLabel("Name:"))
        self.employee_layout.addWidget(self.name_input)

        self.surname_input = QListWidget()
        self.surname_input.addItems(["Doe", "Smith", "Johnson", "Brown", "Davis", "Wilson"])
        self.employee_layout.addWidget(QLabel("Surname:"))
        self.employee_layout.addWidget(self.surname_input)

        self.department_input = QListWidget()
        self.department_input.addItems(["HR", "IT", "Security"])
        self.employee_layout.addWidget(QLabel("Department(s):"))
        self.employee_layout.addWidget(self.department_input)

        self.layout.addLayout(self.employee_layout)

        self.generate_button = QPushButton("Generate JSON")
        self.generate_button.clicked.connect(self.generateJSON)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)
        self.setWindowTitle("JSON Generator")
        self.show()

    def generateJSON(self):
        employees = []
        for i in range(self.name_input.count()):
            employee = {
                "id": self.id_slider.value(),
                "name": self.name_input.item(i).text(),
                "surname": self.surname_input.item(i).text(),
                "department": [item.text() for item in self.department_input.selectedItems()]
            }
            employees.append(employee)

        data = {"employees": employees}
        json_data = json.dumps(data, indent=4)
        print(json_data)  # You can replace this with saving to a file or displaying in a text box

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JSONGenerator()
    sys.exit(app.exec_())
