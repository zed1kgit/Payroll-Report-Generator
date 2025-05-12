import pytest

from main import CSVParser, PayoutReport, JSONFormat, OutputFormat, Report
import json


def test_csv_parser_1(csv_file_1):
    parser = CSVParser(csv_file_1)
    employees = parser.parse_employees()

    assert len(employees) > 0
    assert employees[0].name == "Alice Johnson"
    assert employees[1].payout == 6000
    assert employees[2].hourly_rate == 60


def test_csv_parser_2(csv_file_2):
    parser = CSVParser(csv_file_2)
    employees = parser.parse_employees()

    assert len(employees) > 0
    assert employees[0].name == "Grace Lee"
    assert employees[1].payout == 5250
    assert employees[2].hourly_rate == 38


def test_csv_parser_3(csv_file_3):
    parser = CSVParser(csv_file_3)
    employees = parser.parse_employees()

    assert len(employees) > 0
    assert employees[0].name == "Karen White"
    assert employees[1].payout == 6510
    assert employees[2].hourly_rate == 37


def test_payout_report(csv_file_1):
    parser = CSVParser(csv_file_1)
    employees = parser.parse_employees()

    report = PayoutReport()
    for employee in employees:
        report.add_employee(employee)

    data = report.get_data()

    assert "Marketing" in data
    assert "Design" in data

    assert data["Marketing"]["total_payout"] == 8000
    assert data["Design"]["total_payout"] == 16200


def test_payout_report_generate(csv_file_1, csv_file_2, csv_file_3):
    report = PayoutReport()
    for filename in [csv_file_1, csv_file_2, csv_file_3]:
        parser = CSVParser(filename)
        employees = parser.parse_employees()
        for employee in employees:
            report.add_employee(employee)

    generated_report = report.generate()

    assert generated_report == ('                  name              hours   rate   payout\n'
                                'Marketing\n'
                                '----------------  Alice Johnson      160     50     $8000  \n'
                                '----------------  Henry Martin       150     35     $5250  \n'
                                '                                     310            $13250 \n'
                                'Design\n'
                                '----------------  Bob Smith          150     40     $6000  \n'
                                '----------------  Carol Williams     170     60     $10200 \n'
                                '                                     320            $16200 \n'
                                'HR\n'
                                '----------------  Grace Lee          160     45     $7200  \n'
                                '----------------  Ivy Clark          158     38     $6004  \n'
                                '----------------  Liam Harris        155     42     $6510  \n'
                                '                                     473            $19714 \n'
                                'Sales\n'
                                '----------------  Karen White        165     50     $8250  \n'
                                '----------------  Mia Young          160     37     $5920  \n'
                                '                                     325            $14170 ')


def test_json_format(csv_file_1):
    parser = CSVParser(csv_file_1)
    employees = parser.parse_employees()

    report = PayoutReport()
    for employee in employees:
        report.add_employee(employee)

    data = report.get_data()

    file_name = "report.json"

    json_format = JSONFormat()
    json_format.save(file_name, data)

    with open(file_name, 'r', encoding='utf-8') as file:
        loaded = json.load(file)

    assert "Design" in loaded
    assert loaded["Design"]["total_payout"] == 16200


def test_format_error():
    with pytest.raises(ValueError):
        OutputFormat.from_filename("test.txt")


def test_csvparser_errors():
    with pytest.raises(ValueError):
        CSVParser("test.txt")

    with pytest.raises(FileNotFoundError):
        parser = CSVParser("test.csv")
        parser.parse_employees()


def test_report(csv_file_1):
    reports = Report.all_reports()
    report = list(reports.keys())

    assert report[0] == "payout"

