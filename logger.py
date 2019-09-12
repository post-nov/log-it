import sheet
import entry
from utils import calen
from utils.terminal import clear_screen
from utils.text import (pretty_print,
                        pretty_input,
                        pretty_tables)


class Logger:
    def menu(self):
        while True:
            pretty_print(['LOG MENU',
                          ('Add today\'s log', 'Enter'),
                          ('Add yesterday\'s log', 'y'),
                          ('Add specific day', 'DD-MM-YY'),
                          ('Return to main menu', 'q')])
            selection = pretty_input()

            if selection == '':
                date = calen.today()
                self.add_log_menu(date)
            elif selection == 'y':
                date = calen.yesterday()
                self.add_log_menu(date)
            elif calen.is_correct_date(selection):
                date = calen.str_to_dt(selection)
                self.add_log_menu(date)
            elif selection == 'q':
                break
            else:
                pretty_print('Try again')
                clear_screen()

    def _rewrite_log(self, date):
        # Saving ID of record to rewrite
        date_of_record_to_delete = calen.dt_to_str(date, 'uni')
        id_of_record_to_delete = sheet.get_record(value=date_of_record_to_delete)[0]
        # Adding new record
        record = entry.new_entry(date)
        sheet.add_record(*record)
        # Deleting previous record
        sheet.delete_record('id', id_of_record_to_delete)

    def _rewrite_log_menu(self, date):
        while True:
            pretty_print([f'There is already an entry for {date}',
                          ('Rewrite it?', 'y'),
                          ('Back to log menu', 'q')])
            selection = pretty_input()

            if selection == 'y':
                self._rewrite_log(date)
                break
            elif selection == 'q':
                break
            else:
                pretty_print('Try again')

    def _show_added_record(self, date):
        clear_screen()
        pretty_print('Record successfully added!')
        date_of_record = calen.dt_to_str(date, 'uni')
        added_record = sheet.get_record(value=date_of_record)
        pretty_tables(added_record)

    @clear_screen
    def add_log_menu(self, date):
        if calen.check_existence(date):
            self._rewrite_log_menu(date)
        else:
            record = entry.new_entry(date)
            sheet.add_record(*record)
        self._show_added_record(date)
