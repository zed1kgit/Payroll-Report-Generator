import argparse
import json


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
        lines.append(
            f"                                     {self.total_hours_worked():<6}         ${self.total_payout():<6}")
        return lines


class CSVParser:
    def __init__(self, filename):
        if not filename.endswith('.csv'):
            raise ValueError('Файл должен быть в формате .csv')
        self.filename = filename

    def parse_employees(self):
        employees = []
        try:
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
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.filename} не найден.")
        return employees


class Report:
    name: str = ""

    @classmethod
    def all_reports(cls):
        return {subclass.name: subclass for subclass in cls.__subclasses__()}

    def save(self, filename, data, output_format):
        output_format.save(filename, data)


class PayoutReport(Report):
    name = 'payout'

    def __init__(self):
        self.departments = {}

    def add_employee(self, employee: Employee):
        if employee.department not in self.departments:
            self.departments[employee.department] = Department(employee.department)
        self.departments[employee.department].add_employee(employee)

    def get_data(self):
        return {
            department.name: {
                "employees": [
                    {
                        "id": employee.id,
                        "name": employee.name,
                        "email": employee.email,
                        "hours_worked": employee.hours_worked,
                        "hourly_rate": employee.hourly_rate,
                        "payout": employee.payout
                    }
                    for employee in department.employees
                ],
                "total_hours_worked": department.total_hours_worked(),
                "total_payout": department.total_payout()
            }
            for department in self.departments.values()
        }

    def generate(self):
        all_lines = ["                  name              hours   rate   payout"]
        for department in self.departments.values():
            all_lines.extend(department.report())
        return "\n".join(all_lines)


class OutputFormat:
    extension: str = ""

    @classmethod
    def all_formats(cls):
        return {subclass.extension: subclass for subclass in cls.__subclasses__()}

    @classmethod
    def from_filename(cls, filename):
        ext = filename.rsplit('.', 1)[-1].lower()
        formats = cls.all_formats()
        format_cls = formats.get(ext)
        if not format_cls:
            raise ValueError(f"Формат .{ext} не поддерживается. Поддерживаемые форматы: {', '.join(formats)}")
        return format_cls()

    def save(self, filename, data):
        raise NotImplementedError


class JSONFormat(OutputFormat):
    extension = 'json'

    def save(self, filename, data):
        with open(f"{filename}", 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


def main():  # pragma: no cover
    reports = Report.all_reports()

    parser = argparse.ArgumentParser(description="Скрипт подсчёта зарплаты сотрудников.")
    parser.add_argument('files', type=str, nargs='+', help="CSV файлы с данными сотрудников")
    parser.add_argument('--report', required=True, choices=list(reports.keys()), help="Тип отчета")
    parser.add_argument('--save', type=str, help="Название файла для сохранения отчета (например, report.json)")
    args = parser.parse_args()

    report_cls = reports.get(args.report)
    report = report_cls()

    for filename in args.files:
        parser = CSVParser(filename)
        employees = parser.parse_employees()
        for employee in employees:
            report.add_employee(employee)

    print(report.generate())

    if args.save:
        try:
            output_format = OutputFormat.from_filename(args.save)
            report.save(args.save, report.get_data(), output_format)
            print(f"Отчет успешно сохранен в файл: {args.save}")
        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == '__main__':
    main()
