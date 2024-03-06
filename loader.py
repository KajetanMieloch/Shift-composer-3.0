import os
import json

class Loader:
    def __init__(self):
        self.folder_path = 'userData'
        self.file_names = ['allEmp.json', 'empProp.json', 'scheduleProp.json']
        self.data = {}

        for file_name in self.file_names:
            file_path = os.path.join(self.folder_path, file_name)
            with open(file_path) as file:
                self.data[file_name] = json.load(file)

        # Access the loaded JSON data
        self.all_emp_data = self.data['allEmp.json']
        self.emp_prop_data = self.data['empProp.json']
        self.schedule_prop_data = self.data['scheduleProp.json']

    def get_all_emp_data(self):
        return self.all_emp_data

    def get_emp_prop_data(self):
        return self.emp_prop_data

    def get_schedule_prop_data(self):
        return self.schedule_prop_data
