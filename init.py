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
    
    def get_employee_by_id(self, id):
        for employee in self.employees:
            if employee.get_id() == id:
                return employee
        return None
    
    def get_employee_availability_by_id(self, id):
        for employee in self.availability:
            if employee["id"] == id:
                return employee["availability"]
        return None
    
    def get_employee_availability_by_date(self, id, date):
        for employee in self.availability:
            if employee["id"] == id:
                return employee["availability"][date]
        return None
    
    def get_all_employees_availability_by_date(self, date):
        employees_availability = []
        for employee in self.employees:
            employees_availability.append(self.get_employee_availability_by_date(employee.get_id(), date))
        return employees_availability

    def get_all_employees_availability_by_date_department(self, date, department):
        employees_availability = []
        for employee in self.employees:
            if department in employee.get_department():
                employees_availability.append(self.get_employee_availability_by_date(employee.get_id(), date))
        return employees_availability
                
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
    
    def get_name(self):
        return self.name
    
    def get_surname(self):
        return self.surname
    
    def get_department(self):
        return self.department
    
    def get_last_shift(self):
        return self.last_shift
    
    def get_worked_hours(self):
        return self.worked_hours
    
    def get_shifts(self):
        return self.shifts
    
    def get_availability(self):
        return self.availability


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