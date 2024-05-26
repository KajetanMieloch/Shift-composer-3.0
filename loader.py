import os
import json
from init import *

class Loader:
    def __init__(self):
        self.folder_path = ''
        self.file_names = ['allemployees.json', 'employeesproperties.json', 'scheduleproperties.json']
        self.data = {}

        for file_name in self.file_names:
            file_path = os.path.join(self.folder_path, file_name)
            with open(file_path) as file:
                self.data[file_name] = json.load(file)

        # Access the loaded JSON data
        self.all_employeesloyees_data = self.data['allemployees.json']
        self.employees_properties_data = self.data['employeesproperties.json']
        self.schedule_properties_data = self.data['scheduleproperties.json']

    def get_all_employeesloyees_data(self):
        return self.all_employeesloyees_data.get('employees')

    def get_employees_properties_data(self):
        return self.employees_properties_data.get("employeesAva")

    def get_schedule_properties_data(self):
        return self.schedule_properties_data.get("scheduleProperties")


