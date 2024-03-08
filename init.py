from datetime import datetime

class EmployeesAndAvailability:
    def __init__(self, employees, employeesAva):
        self.employees = []
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
        
        # Create employees list
        for employee in employees:
            self.employees.append(Employee(employee["id"], employee["name"], employee["surname"], employee["department"]))
    
    def get_name_by_id(self, id):
        for employee in self.employees:
            if employee.get_id() == id:
                return employee.name
        return None
    
    def get_schedule_by_id(self, id):
        for employee in self.employees:
            if employee.get_id() == id:
                return employee.shifts
        return None

class Employee:
    def __init__(self, id, name, surname, department):
        self.id = id
        self.name = name
        self.surname = surname
        self.department = department
        self.last_shift = None
        self.worked_hours = 0
        self.shifts = []
        self.availability = []
    
    def get_id(self):
        return self.id
    
    def get_all_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "department": self.department
        }

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