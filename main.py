import argparse


class Employee:
    def __init__(self, emp_id, email, name, department, hours_worked, hourly_rate):
        self.id = emp_id
        self.email = email
        self.name = name
        self.department = department
        self.hours_worked = int(hours_worked)
        self.hourly_rate = int(hourly_rate)

    @property
    def payout(self):
        return self.hourly_rate * self.hours_worked


class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee: Employee):
        self.employees.append(employee)

    def total_hours_worked(self):
        return sum(employee.hours_worked for employee in self.employees)

    def total_payout(self):
        return sum(employee.payout for employee in self.employees)

    def report(self):
        lines = [f"{self.name}"]
        for employee in self.employees:
            lines.append(
                f"----------------  {employee.name:<18} {employee.hours_worked:<6}  {employee.hourly_rate:<5}  ${employee.payout:<6}")
        lines.append(f"                                     {self.total_hours_worked():<6}         ${self.total_payout():<6}")
        return lines


class CSVParser:
    def __init__(self, filename):
        self.filename = filename

    def parse_employees(self):
        employees = []
        with open(self.filename, 'r', encoding="utf-8") as csvfile:
            header = csvfile.readline().strip().split(',')
            for line in csvfile:
                if not line.strip():
                    continue
                values = line.strip().split(',')
                row_dict = dict(zip(header, values))
                row_dict['emp_id'] = row_dict.pop('id')
                rate_key = next(k for k in row_dict if k in ['hourly_rate', 'rate', 'salary'])
                row_dict['hourly_rate'] = row_dict.pop(rate_key)
                employees.append(Employee(**row_dict))
        return employees


class PayoutReport:
    def __init__(self):
        self.departments = {}

    def add_employee(self, employee: Employee):
        if employee.department not in self.departments:
            self.departments[employee.department] = Department(employee.department)
        self.departments[employee.department].add_employee(employee)

    def generate(self):
        all_lines = ["                  name              hours   rate   payout"]
        for department in self.departments.values():
            all_lines.extend(department.report())
        return "\n".join(all_lines)


def main():
    parser = argparse.ArgumentParser(description="Скрипт подсчёта зарплаты сотрудников.")
    parser.add_argument('files', type=str, nargs='+', help="CSV файлы с данными сотрудников")
    parser.add_argument('--report', required=True, choices=['payout'], help="Тип отчета")
    args = parser.parse_args()

    report = PayoutReport()

    for filename in args.files:
        parser = CSVParser(filename)
        employees = parser.parse_employees()
        for employee in employees:
            report.add_employee(employee)

    print(report.generate())


if __name__ == '__main__':
    main()
