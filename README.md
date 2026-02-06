markdown
# GDP Analyzer

Утилита для анализа данных о ВВП стран из CSV файлов.

## Использование

```bash
python main.py -f data.csv
python main.py -f data1.csv data2.csv --report average-gdp
CSV файлы должны содержать колонки country и gdp. Некорректные значения ВВП автоматически пропускаются. Результат выводится в виде отсортированной таблицы средних значений.

Пример добавления медианного значения:

python
def calculate_median(self):
    for country, values in self.avg_country_gdp.items():
        median = sorted(values)[len(values)//2]
        # ... логика отчета
Тестирование
bash
pytest -m
Тесты проверяют чтение CSV, обработку ошибок парсинга, корректность расчетов и форматирование вывода.

text

## Добавление нового отчета
```python
if args.report == 'median-gdp':
    analyzer = MedianGDP_report()  # новый класс
elif args.report == 'average-gdp':
    analyzer = GDP_report()#
