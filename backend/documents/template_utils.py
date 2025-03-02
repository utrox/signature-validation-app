import datetime

class TemplateUtils:
    @property
    def todays_date(self):
        return datetime.datetime.now().strftime("%Y.%m.%d")
    