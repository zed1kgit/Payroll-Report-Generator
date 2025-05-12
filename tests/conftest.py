import pytest
from pathlib import Path

# Указываем директорию с тестовыми данными
TEST_DATA_DIR = Path(__file__).parent / "data"


# Фикстуры для файлов
@pytest.fixture
def csv_file_1():
    return str(TEST_DATA_DIR / "data1.csv")


@pytest.fixture
def csv_file_2():
    return str(TEST_DATA_DIR / "data2.csv")


@pytest.fixture
def csv_file_3():
    return str(TEST_DATA_DIR / "data3.csv")
