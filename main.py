import csv
from tabulate import tabulate
import argparse

class GDP_report:
    def __init__(self):
        self.avg_country_gdp = {}

    def read_csv(self, files: str) -> None:
        '''Читает CSV файл с данными о ВВП и добавляет их во внутреннюю структуру данных.
        
        Args:
            files (str): Путь к CSV файлу. Ожидается наличие колонок 'country' и 'gdp'.
        '''
        with open(files, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            for line in reader:
                try:
                    gdp_val = float(line['gdp'])
                    country = line['country'].capitalize()
                except ValueError:
                    continue
                if country in self.avg_country_gdp:
                    self.avg_country_gdp[country].append(gdp_val)
                else:
                    self.avg_country_gdp[country] = [gdp_val]
                    
    def calculate(self) -> list:
        '''Вычисляет средний ВВП для каждой страны на основе собранных данных.
        
        Returns:
            list: Отсортированный по убыванию ВВП список списков формата [[страна, средний_ВВП], ...]
        '''
        table_data = []
        for country, gdp_list in self.avg_country_gdp.items():
            avg_gdp = round(sum(gdp_list) / len(gdp_list), 2)
            table_data.append([country, avg_gdp])
        return sorted(table_data, key=lambda x: x[1], reverse=True)

    def print_report(self) -> None:
        '''Форматирует и выводит отчёт со средними значениями ВВП по странам.'''
        table_data = self.calculate()
        print(tabulate(table_data, headers=['Country', 'Avg GDP'],  tablefmt='fancy_grid'))
    
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', nargs='+', required=True)
    parser.add_argument('--report', default='average-gdp', required=False)
    args = parser.parse_args()  
    
    if args.report != 'average-gdp':
        print(f"Unknown report: {args.report}")
        return 1
    
    analyzer = GDP_report()
    for file in args.files:
        analyzer.read_csv(file)
    analyzer.print_report()
       
if __name__ == '__main__':
    main()
