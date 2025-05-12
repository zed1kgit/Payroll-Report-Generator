class Employee:
    def __init__(self, name, department, hours_worked, hourly_rate):
        self.name = name
        self.department = department
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    @property
    def payout(self):
        return self.hourly_rate * self.hours_worked
