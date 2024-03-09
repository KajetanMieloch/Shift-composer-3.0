import datetime

class Generator:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.days = (datetime.datetime.strptime(self.end_date, "%Y-%m-%d") - datetime.datetime.strptime(self.start_date, "%Y-%m-%d")).days

        self.weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

        self.harmonogram = {}

        self.harmonogram["startDate"] = {}
        self.harmonogram["startHour"] = {}
        self.harmonogram["endDate"] = {}
        self.harmonogram["endHour"] = {}

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
        for date in dates:
            hours = work_data[self.weekdays[date.weekday()]]
            if self.is_hours_after_midnight(hours):
                self.harmonogram["startDate"] = date.strftime("%Y-%m-%d")
                self.harmonogram["endDate"] = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

                self.harmonogram["startHour"] = hours["from"]
                self.harmonogram["endHour"] = hours["to"]
            
                print(self.harmonogram)
                continue

            self.harmonogram["startDate"] = date.strftime("%Y-%m-%d")
            self.harmonogram["endDate"] = date.strftime("%Y-%m-%d")

            self.harmonogram["startHour"] = hours["from"]
            self.harmonogram["endHour"] = hours["to"]
            print(self.harmonogram)