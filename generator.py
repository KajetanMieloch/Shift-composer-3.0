import datetime

class Generator:
    def __init__(self, employeesAndAvailability, sheduleProperties):
        self.employeesAndAvailability = employeesAndAvailability
        self.sheduleProperties = sheduleProperties
        self.start_date = self.sheduleProperties.get_start_date()
        self.end_date = self.sheduleProperties.get_end_date()
        self.days = (datetime.datetime.strptime(self.end_date, "%Y-%m-%d") - datetime.datetime.strptime(self.start_date, "%Y-%m-%d")).days

        self.weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

        self.harmonograms = []


    def generate_harmonogram_phase_0(self, work_data, department):
        """
        Generates a harmonogram based on the provided work data and department.

        Args:
            work_data (dict): A dictionary containing work data for each weekday.
            department (str): The department for which the harmonogram is generated.

        Returns:
            list: A list of Harmonogram objects representing the generated harmonogram.
        """
        dates = self.dates_between(self.start_date, self.end_date)
        indx = -1
        for date in dates:
            indx += 1

            employees = self.employeesAndAvailability.get_employees_obj_by_date_department_min_hour_req(date.strftime("%Y-%m-%d"), department)

            for emp in employees:
                print(emp.get_hours_of_availability())

            self.harmonogramOBJ = Harmonogram(indx)

            self.harmonogramOBJ.set_matched_employees(employees)

            hours = work_data[self.weekdays[date.weekday()]]
            if self.is_hours_after_midnight(hours):
                self.harmonogramOBJ.set_start_date(date.strftime("%Y-%m-%d"))
                self.harmonogramOBJ.set_end_date((date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

                self.harmonogramOBJ.set_start_hour(hours["from"])
                self.harmonogramOBJ.set_end_hour(hours["to"])
                self.harmonograms.append(self.harmonogramOBJ)
                continue

            self.harmonogramOBJ.set_start_date(date.strftime("%Y-%m-%d"))
            self.harmonogramOBJ.set_end_date(date.strftime("%Y-%m-%d"))

            self.harmonogramOBJ.set_start_hour(hours["from"])
            self.harmonogramOBJ.set_end_hour(hours["to"])

            self.harmonograms.append(self.harmonogramOBJ)
        return self.harmonograms

    def dates_between(self, start_date, end_date):
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        dates = [start + datetime.timedelta(days=i) for i in range((end-start).days)]
        return dates
    
    def is_hours_after_midnight(self, hours):
        if hours["from"] > hours["to"]:
            return True
        return False

    def generate_harmonogram_phase_1(self):
        pass

    
class Harmonogram:
    def __init__(self, indx):
        self.indx = indx
        self.start_date = 0
        self.end_date = 0
        self.start_hour = 0
        self.end_hour = 0
        self.matched_employees = []
    
    def set_start_date(self, start_date):
        self.start_date = start_date

    def set_end_date(self, end_date):
        self.end_date = end_date

    def set_start_hour(self, start_hour):
        self.start_hour = start_hour
    
    def set_end_hour(self, end_hour):
        self.end_hour = end_hour

    def set_matched_employees(self, matched_employees):
        self.matched_employees = matched_employees

    def get_harmonogram(self):
        return {
            "startDate": self.start_date,
            "endDate": self.end_date,
            "startHour": self.start_hour,
            "endHour": self.end_hour,
            "matchedEmployees": self.matched_employees
        }
    