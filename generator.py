import datetime

class Generator:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.days = (datetime.datetime.strptime(self.end_date, "%Y-%m-%d") - datetime.datetime.strptime(self.start_date, "%Y-%m-%d")).days

        print(self.dates_between(self.start_date, self.end_date))


    def dates_between(self, start_date, end_date):
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        dates = [start + datetime.timedelta(days=i) for i in range((end-start).days)]
        return dates