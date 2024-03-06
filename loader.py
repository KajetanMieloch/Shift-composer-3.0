import os
import json

folder_path = 'userData'
file_names = ['allEmp.json', 'empProp.json', 'scheduleProp.json']

data = {}

for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path) as file:
        data[file_name] = json.load(file)

# Access the loaded JSON data
all_emp_data = data['allEmp.json']
emp_prop_data = data['empProp.json']
schedule_prop_data = data['scheduleProp.json']