from .base import View
from .utils.tables import pretty_tables
from modules import viewer


class ViewerView(View):
    def __init__(self):
        super().__init__()
        self.menu_name = 'VIEWER MENU'
        self.menu_options = {
            'show_all':
            {'name': 'Show all', 'key': 'a', 'command': self.show_all},
            # 'show_last_n':
            # {'name': 'Show last N', 'key': 'n', 'command': self.show_last_n},
            # 'show_with_time':
            # {'name': 'Show with specific time', 'key': 't', 'command': self.show_with_time},
            # 'show_with_score':
            # {'name': 'Show with specific score', 'key': 's', 'command': self.show_with_score}
        }

    def show_all(self):
        table_sizes, table_records, table_heads = viewer.get_sizes_records_heads('records')
        self.text = pretty_tables(table_sizes,
                                  table_records,
                                  table_heads)

    # @clear_screen
    # def show_last_n(self):
    #     pretty_print([
    #         'How much would you like to see?',
    #         ('Last 5', 'Enter'),
    #         ('Last n', '*NUMBER*'),
    #         ('Return to VIEWER MENU', 'q')
    #     ])
    #     selection = pretty_input()
    #
    #     all_records = sheet.list_all_records()
    #     if selection == '':
    #         clear_screen()
    #         pretty_tables(all_records[-5:])
    #     elif selection.isnumeric():
    #         n = int(selection)
    #         clear_screen()
    #         pretty_tables(all_records[-n:])
    #     elif selection == 'q':
    #         clear_screen()
    #         pass
    #     else:
    #         pretty_print('Try again')
    #         self.show_last_n()
    #
    # def _find_index(self, records, point, type):
    #     if type == 'time':
    #         values = [value[3] for value in records]
    #     elif type == 'score':
    #         values = [value[4] for value in records]
    #     target_point = 0
    #     for index in range(len(values)):
    #         if values[index] <= point:
    #             target_point = index
    #         else:
    #             break
    #     return target_point
    #
    # @clear_screen
    # def _show_lesser_time(self, value, records):
    #     if value < records[0][3]:
    #         pretty_print(f'There is no records with time lesser than {value}')
    #     else:
    #         index = self._find_index(records, value, 'time')
    #         index += 1  # Because of logic of list slicing
    #         pretty_tables(records[:index])
    #
    # @clear_screen
    # def _show_bigger_time(self, value, records):
    #     if value > records[-1][3]:
    #         pretty_print(f'There is no records with time bigger than {value}')
    #     else:
    #         index = self._find_index(records, value, 'time')
    #         pretty_tables(records[index:])
    #
    # @clear_screen
    # def show_with_time(self):
    #     pretty_print([
    #         'What time you want to see?',
    #         ('Bigger or equal to N', '>*NUMBER*'),
    #         ('Lesser or equal to N', '<*LESSER*'),
    #         ('Bigest', 'b'),
    #         ('Smallest', 's'),
    #         ('Return to VIEWER MENU', 'q')
    #     ])
    #     selection = pretty_input()
    #
    #     all_records = sheet.list_all_records('time')
    #     if selection[0] == '<' and selection[1:].isnumeric():
    #         value = int(selection[1:])
    #         self._show_lesser_time(value, all_records)
    #     elif selection[0] == '>' and selection[1:].isnumeric():
    #         value = int(selection[1:])
    #         self._show_bigger_time(value, all_records)
    #     elif selection == 'b':
    #         biggest_record = all_records[-1]
    #         clear_screen()
    #         pretty_tables(biggest_record)
    #     elif selection == 's':
    #         smallest_record = all_records[0]
    #         clear_screen()
    #         pretty_tables(smallest_record)
    #     elif selection == 'q':
    #         clear_screen()
    #         pass
    #     else:
    #         pretty_print('Try again')
    #
    # @clear_screen
    # def _show_lesser_score(self, value, records):
    #     if value < records[0][4]:
    #         pretty_print(f'There is no records with score lesser than {value}')
    #     else:
    #         index = self._find_index(records, value, 'score')
    #         index += 1  # Because of logic of list slicing
    #         pretty_tables(records[:index])
    #
    # @clear_screen
    # def _show_bigger_score(self, value, records):
    #     if value > records[-1][4]:
    #         pretty_print(f'There is no records with score bigger than {value}')
    #     else:
    #         index = self._find_index(records, value-1, 'score')
    #         index += 1
    #         pretty_tables(records[index:])
    #
    # @clear_screen
    # def _show_equal_score(self, value, records):
    #     start_index = 0
    #     end_index = len(records)
    #     for index in range(len(records)):
    #         if value > records[index][4]:
    #             start_index = index + 1
    #         elif value < records[index][4]:
    #             end_index = index
    #             break
    #     if len(records[start_index:end_index]) == 0:
    #         pretty_print(f'There is no values this ({value}) score')
    #     else:
    #         pretty_tables(records[start_index:end_index])
    #
    # def _is_correct_score(self, score):
    #     if score[0] in ['>', '<']:
    #         score = score[1:]
    #     if score.isnumeric():
    #         if int(score) > 1 and int(score) < 5:
    #             return True
    #     else:
    #         return False
    #
    # @clear_screen
    # def show_with_score(self):
    #     pretty_print([
    #         'What time you want to see?',
    #         'Available numbers: from 1 to 5',
    #         ('Bigger or equal to N', '>*NUMBER*'),
    #         ('Lesser or equal to N', '<*LESSER*'),
    #         ('Equal to N', '*NUMBER*'),
    #         ('Return to VIEWER MENU', 'q')
    #     ])
    #     selection = pretty_input()
    #
    #     all_records = sheet.list_all_records('score')
    #     if selection[0] == '<' and self._is_correct_score(selection):
    #         value = int(selection[1])
    #         self._show_lesser_score(value, all_records)
    #     elif selection[0] == '>' and self._is_correct_score(selection):
    #         value = int(selection[1])
    #         self._show_bigger_score(value, all_records)
    #     elif selection.isnumeric():
    #         value = int(selection)
    #         self._show_equal_score(value, all_records)
    #     elif selection == 'q':
    #         clear_screen()
    #         pass
    #     else:
    #         pretty_print('Try again')
