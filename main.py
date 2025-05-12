class Employee:
    def __init__(self, name, department, hours_worked, hourly_rate):
        self.name = name
        self.department = department
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    @property
    def payout(self):
        return self.hourly_rate * self.hours_worked


class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee: Employee):
        self.employees.append(employee)

    def report(self):
        lines = ["                  name              hours   rate   payout\n", f"{self.name}\n"]
        for employee in self.employees:
            lines.append(
                f"----------------  {employee.name:<18} {employee.hours_worked:<6}  {employee.hourly_rate:<5}  ${employee.payout:<6}")
        return lines


class CSVParser:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        data = []
        with open(self.filename, 'r', encoding="utf-8") as csvfile:
            header = csvfile.readline().split(',')
            for line in csvfile:
                values = line.split(',')
                row_dict = dict(zip(header, values))
                data.append(row_dict)
        return data


class PayoutReport:
    def __init__(self):
        self.departments = []

    def add_employee(self, employee: Employee):
        if employee.department not in self.departments:
            self.departments[employee.department] = Department(employee.department)
        self.departments[employee.department].add_employee(employee)

    def generate(self):
        reports = [department.report() for department in self.departments]
        return "\n".join(reports)
