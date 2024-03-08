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
    
    def get_all_employees_availability_by_department(self, department):
        employees_availability = []
        for employee in self.employees:
            if department in employee.get_department():
                employees_availability.append(self.get_employee_availability_by_id(employee.get_id()))
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
    def __init__(self, data):
        self.data = data

    def get_properties(self):
        return self.data
    
    def get_date(self):
        return self.data["date"]

    def get_start_date(self):
        return self.data["date"]["from"]

    def get_end_date(self):
        return self.data["date"]["to"]
    
    def get_properties_for_department(self, department):
       for dep in self.data["departments"]:
           if dep["name"] == department:
               return dep
   
    def get_minEmployees_for_department(self, department):
        for dep in self.data["departments"]:
            if dep["name"] == department:
                return dep["minEmployees"]
    
    def get_maxEmployees_for_department(self, department):
        for dep in self.data["departments"]:
            if dep["name"] == department:
                return dep["maxEmployees"]
        
    def get_max_consecutive_work_days_for_department(self, department):
        for dep in self.data["departments"]:
            if dep["name"] == department:
                return dep["maxConsecutiveWorkDays"]
    
    def get_work_hours_for_department(self, department):
        for dep in self.data["departments"]:
            if dep["name"] == department:
                return dep["workHours"]
        
    def get_priority_hours_for_department(self, department):
        for dep in self.data["departments"]:
            if dep["name"] == department:
                return dep["priorityHours"]
    
    def get_shifts_for_department(self, department):
        for dep in self.data["departments"]:
            if dep["name"] == department:
                return dep["shifts"]