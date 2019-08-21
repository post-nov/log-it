import sheet
import calen
from utils.terminal import clear_screen
from utils.text import (pretty_print,
                        pretty_input,
                        pretty_tables)


class Statistics:
    def menu(self):
        clear_screen()
        while True:
            pretty_print([
                'STATISTICS MENU',
                ('Overall', 'a'),
                ('Last 30 days', 'l'),
                ('Last N days', '*NUMBER*'),
                ('Return to main menu', 'q')
            ])

            selection = pretty_input()

            if selection == 'a':
                self.menu_second()
            elif selection == 'l':
                self.menu_second(30)
            elif selection.isnumeric():
                days_ago = int(selection)
                self.menu_second(days_ago)
            elif selection == 'q':
                break
            else:
                pretty_print('Try again')

    def _average_value(self, records, type):
        if type == 'score':
            return sum([x[4] for x in records])/len(records)
        elif type == 'time':
            return sum([x[3] for x in records])/len(records)

    def _analyzer(self, records):
        average_score = self._average_value(records, 'score')
        average_time = self._average_value(records, 'time')
        total_time = sum([x[3] for x in records])
        return{'average_score': round(average_score, 2),
               'average_time': round(average_time, 2),
               'total_time': round(total_time, 2)}

    def menu_second(self, days_ago=None):
        if days_ago == None:
            records = sheet.list_all_records()
        else:
            start_index = calen.get_start_index(days_ago)
            records = sheet.list_all_records()[start_index:]
        results = self._analyzer(records)
        results_pairs = [(key, str(value)) for key, value in results.items()]
        clear_screen()
        pretty_print(["STATISTICS"]+results_pairs)
