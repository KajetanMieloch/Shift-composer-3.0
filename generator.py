import datetime

class Generator:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.days = (datetime.datetime.strptime(self.end_date, "%Y-%m-%d") - datetime.datetime.strptime(self.start_date, "%Y-%m-%d")).days

        self.weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

        self.harmonograms = []

    def dates_between(self, start_date, end_date):
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        dates = [start + datetime.timedelta(days=i) for i in range((end-start).days)]
        return dates
    
    def is_hours_after_midnight(self, hours):
        if hours["from"] > hours["to"]:
            return True
        return False

    def generate_harmonogram(self, work_data):
        dates = self.dates_between(self.start_date, self.end_date)
        indx = -1
        for date in dates:
            indx += 1

            self.harmonogramOBJ = Harmonogram(indx)
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

class Harmonogram:
    def __init__(self, indx):
        self.indx = indx
        self.start_date = 0
        self.end_date = 0
        self.start_hour = 0
        self.end_hour = 0
    
    def set_start_date(self, start_date):
        self.start_date = start_date

    def set_end_date(self, end_date):
        self.end_date = end_date

    def set_start_hour(self, start_hour):
        self.start_hour = start_hour
    
    def set_end_hour(self, end_hour):
        self.end_hour = end_hour

    def get_harmonogram(self):
        return {
            "startDate": self.start_date,
            "endDate": self.end_date,
            "startHour": self.start_hour,
            "endHour": self.end_hour
        }
    