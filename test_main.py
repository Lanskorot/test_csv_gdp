import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from main import GDP_report

@pytest.fixture
def temp_csv_file():
    """Создает временный CSV файл для тестов."""
    csv_content = """country,year,gdp,gdp_growth
Россия,2023,25462,2.1
Россия,2022,23315,2.1
Беларусь,2023,17963,5.2
"""
    fd, path = tempfile.mkstemp(suffix='.csv')
    with os.fdopen(fd, 'w') as f:
        f.write(csv_content)
    yield path
    os.unlink(path)

def test_read_csv_valid_data(temp_csv_file):
    """Тест чтения корректных CSV данных."""
    analyzer = GDP_report()
    analyzer.read_csv(temp_csv_file)
    
    assert 'Россия' in analyzer.avg_country_gdp
    assert 'Беларусь' in analyzer.avg_country_gdp
    assert len(analyzer.avg_country_gdp['Россия']) == 2

def test_read_csv_invalid_gdp(temp_csv_file):
    """Тест обработки некорректных GDP значений."""
    # Модифицируем файл, добавив некорректную строку
    with open(temp_csv_file, 'a') as f:
        f.write("Казахстан,2023,invalid,1.0\n")
    
    analyzer = GDP_report()
    analyzer.read_csv(temp_csv_file)
    
    assert 'Казахстан' not in analyzer.avg_country_gdp  # Пропущена из-за ошибки

def test_calculate_single_country():
    """Тест расчета для одной страны."""
    analyzer = GDP_report()
    analyzer.avg_country_gdp = {'Россия': [1000, 2000]}
    
    result = analyzer.calculate()
    
    assert len(result) == 1
    assert result[0][0] == 'Россия'
    assert result[0][1] == 1500.0

def test_calculate_multiple_countries():
    """Тест расчета и сортировки для нескольких стран."""
    analyzer = GDP_report()
    analyzer.avg_country_gdp = {
        'Россия': [25000, 23000],
        'Беларусь': [17000, 18000],
        'Казахстан': [4000]
    }
    
    result = analyzer.calculate()
    
    assert result[0][0] == 'Россия'      # Самый высокий ВВП
    assert result[1][0] == 'Беларусь'
    assert result[2][0] == 'Казахстан'
    assert result[0][1] == 24000.0    # (25000+23000)/2

def test_print_report_captures_output(temp_csv_file, capsys):
    """Тест вывода отчета (без проверки точного формата tabulate)."""
    analyzer = GDP_report()
    analyzer.read_csv(temp_csv_file)
    
    analyzer.print_report()
    captured = capsys.readouterr()
    
    assert 'Country' in captured.out
    assert 'Avg GDP' in captured.out
    assert 'Россия' in captured.out

def test_integration_files(temp_csv_file):
    """Интеграционный тест: чтение + расчет."""
    analyzer = GDP_report()
    analyzer.read_csv(temp_csv_file)
    
    result = analyzer.calculate()
    
    russia_avg = round((25462 + 23315) / 2, 2)
    belarus_avg = 17963.0
    
    assert result[0][1] == russia_avg   # Россия сверху
    assert result[1][1] == belarus_avg
