from datetime import datetime



class Employee:
    def __init__(self, id, name, surname, department):
        self.id = id
        self.name = name
        self.surname = surname
        self.department = department
    
    def get_id(self):
        return self.id
    
    def get_all_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "department": self.department
        }

class EmployeeAvailability:
    def __init__(self, id, employeesAva):
        self.id = id
        self.availability = []
        for employee in employeesAva:
            employee_availability = {
                "id": employee["id"],
                "availability": {}
            }
            for date, hours in employee["availability"].items():
                employee_availability["availability"][date] = {
                    "startHour": hours["startHour"],
                    "endHour": hours["endHour"]
                }
            self.availability.append(employee_availability)

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