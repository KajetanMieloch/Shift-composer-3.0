from datetime import datetime

class EmployeesAndAvailability:
    def __init__(self, employees, employeesAva, dataForSchedule):

        self.weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

        self.employees = []
        self.availability = []
        self.dataForSchedule = dataForSchedule
        self.schedule_properties = ScheduleProperties(dataForSchedule)
        self.employee_avability_for_department = {}
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
            employeeObj = self.get_employee_obj_by_id(employee["id"])
            employeeObj.set_availability(self.get_employee_availability_by_id(employee["id"]))

        # This code is very important, it sets how many hours every employee is available
        # This number will determine priority of employee
        # The code is first geting employe then his whole availability and then it calculates how many hours he is available
        # This is not obvious, becouse is employee is avabile outside of work hours, it will not be counted
        # Also if employee is available all day, it will be counted as department work hours
        # If employee is not available at all, it will be counted as 0
        # If employee avbility is less than minimum work hours, it will be not counted

        for employee in employees:
            work_hours = 0
            employeeObj = self.get_employee_obj_by_id(employee["id"])

            # get weekday from date
            for date, emp_hours in employeeObj.get_availability().items():
                work_day = datetime.strptime(date, "%Y-%m-%d").weekday()
                for department in employeeObj.get_department():
                    min_work_hours = self.schedule_properties.get_min_employee_work_hours(department)
                    work_hours = self.schedule_properties.get_work_hours_for_department(department)
                    work_hours_by_day = work_hours.get(self.weekdays[work_day])

                    if emp_hours.get("startHour") != "None" and emp_hours.get("endHour") != "None" and work_hours_by_day.get("from") != "None" and work_hours_by_day.get("to") != "None":
                        if emp_hours.get("startHour") == "All" and emp_hours.get("endHour") == "All":
                            start_hour = work_hours_by_day["from"]
                            end_hour = work_hours_by_day["to"]
                        
                        else:

                            print(employeeObj.get_name(), emp_hours.get("startHour"), emp_hours.get("endHour"), work_hours_by_day["from"], work_hours_by_day["to"])

                            emp_start_hour = self.time_to_float(datetime.strptime(emp_hours.get("startHour"), "%H:%M").strftime("%H:%M"))
                            emp_end_hour = self.time_to_float(datetime.strptime(emp_hours.get("endHour"), "%H:%M").strftime("%H:%M"))
                            work_start_hour = self.time_to_float(datetime.strptime(work_hours_by_day["from"], "%H:%M").strftime("%H:%M"))
                            work_end_hour = self.time_to_float(datetime.strptime(work_hours_by_day["to"], "%H:%M").strftime("%H:%M"))

                            if emp_start_hour <= work_start_hour and emp_end_hour >= work_end_hour:
                                start_hour = work_hours_by_day["from"]
                            
                            elif  emp_start_hour >= work_start_hour and emp_start_hour <= work_end_hour:
                                start_hour = emp_hours.get("startHour")

                            else:
                                print("Error", emp_hours.get("startHour"), emp_hours.get("endHour"), work_hours_by_day["from"], work_hours_by_day["to"])
                                start_hour = "None"

                            if emp_end_hour <= work_start_hour and emp_end_hour >= work_end_hour:
                                end_hour = work_hours_by_day["to"]

                            elif emp_end_hour >= work_start_hour and emp_end_hour <= work_end_hour:
                                end_hour = emp_hours.get("endHour")
                            
                            elif emp_end_hour >= work_start_hour and emp_end_hour >= work_end_hour:
                                end_hour = work_hours_by_day["to"]

                            else:
                                end_hour = "None"

                            try:
                                if abs(datetime.strptime(end_hour, "%H:%M") - datetime.strptime(start_hour, "%H:%M")).seconds / 3600 < min_work_hours:
                                    end_hour = "None"
                                    start_hour = "None"
                            except:
                                pass
                    else:
                        start_hour = "None"
                        end_hour = "None"

                    #Count how many hours employee is avabile and then sum them up and set them to employee
                    if start_hour != "None" and end_hour != "None":
                        employeeObj.set_hours_of_availability(abs(self.time_to_float(end_hour) - self.time_to_float(start_hour)), department)
                        print(employeeObj.get_name(), employeeObj.get_hours_of_availability(department))

        for employee in self.employees:
            for department in employee.get_department():
                employee.set_employee_avability_for_department(department, employee.get_hours_of_availability(department))

    def time_to_float(self, time_string):
        try:
            hours, minutes = map(int, time_string.split(':'))
        except:
            hours, minutes, _ = map(int, time_string.split(':'))
        return hours + minutes / 60

###### This methods returns Object of Employee ######
    def get_employee_obj_by_id(self, id):
        for employee in self.employees:
            if employee.get_id() == id:
                return employee
        return None
    
    def get_employees_obj_by_date_department_min_hour_req(self, date, department, min_work_hours):
        employees = []
        for employee in self.employees:
            if department in employee.get_department() and self.get_employee_availability_by_date(employee.get_id(), date):
                if self.get_employee_availability_by_date(employee.get_id(), date).get("startHour") != "None" and self.get_employee_availability_by_date(employee.get_id(), date).get("endHour") != "None":
                    if employee.get_hours_of_availability(department) >= min_work_hours:
                        employees.append(employee)
        return employees

###### This methods returns Dicts of Employees availabilityes ######      

    def get_employee_availability_by_id(self, id):
        for employee in self.availability:
            if employee["id"] == id:
                return employee["availability"]
        return None
    
    def get_employee_availability_by_date(self, id, date):
        for employee in self.availability:
            if employee["id"] == id:
                return employee["availability"].get(date)
        return None

class Employee:
    def __init__(self, id, name, surname, department):
        self.id = id
        self.name = name
        self.surname = surname
        self.department = department
        self.availability = []
        self.hours_of_availability = {}
        self.last_shift = None
        self.worked_hours = 0
        self.shifts = []
        self.employee_avability_for_department = {}
    
    def set_availability(self, availability):
        self.availability = availability
    
    def get_availability(self):
        return self.availability


    def set_hours_of_availability(self, hours_of_availability, department):
        try:
            self.hours_of_availability[department] += hours_of_availability
        except:
            self.hours_of_availability[department] = hours_of_availability

    def get_hours_of_availability(self, department):
        return self.hours_of_availability.get(department, 0.0)

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
    
    def add_worked_hours(self, hours):
        self.worked_hours += hours
    
    def set_employee_avability_for_department(self, department, hours):
        self.employee_avability_for_department[department] = hours
    
    def get_employee_avability_for_department(self):
        return self.employee_avability_for_department
    
    def get_shifts(self):
        return self.shifts


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
    
    def get_min_employee_work_hours(self, department):
        for dep in self.data["departments"]:
            if dep["name"] == department:
                return dep["minEmployeeWorkHours"]
    
    def get_max_employee_work_hours(self, department):
        for dep in self.data["departments"]:
            if dep["name"] == department:
                return dep["maxEmployeeWorkHours"]
    
    def get_properties_for_department(self, department):
       for dep in self.data["departments"]:
           if dep["name"] == department:
               return dep
   
    def get_min_employees_for_department(self, department):
        for dep in self.data["departments"]:
            if dep["name"] == department:
                return dep["minEmployees"]
    
    def get_max_employees_for_department(self, department):
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