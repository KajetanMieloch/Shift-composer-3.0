from datetime import datetime

class Employee:
    def __init__(self, id, name, surname, department):
        self.id = id
        self.name = name
        self.surname = surname
        self.department = department

class EmployeeAvailability:
    def __init__(self, id, availability):
        self.id = id
        self.availability = availability

class ScheduleProperties:
    def __init__(self, date, departments):
        self.date_from = datetime.strptime(date["from"], "%Y-%m-%d").date()
        self.date_to = datetime.strptime(date["to"], "%Y-%m-%d").date()
        self.departments = []
        for dept in departments:
            department = {
                "name": dept["name"],
                "minEmployees": dept["minEmployees"],
                "maxEmployees": dept["maxEmployees"],
                "workHours": {
                    "from": dept["workHours"]["from"],
                    "to": dept["workHours"]["to"]
                },
                "priorityHours": dept["priorityHours"],
                "minEmployeeWorkHours": dept["minEmployeeWorkHours"],
                "maxEmployeeWorkHours": dept["maxEmployeeWorkHours"],
                "shifts": dept["shifts"]
            }
            self.departments.append(department)