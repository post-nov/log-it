from .base import View
from utils import calen


class LoggerView(View):
    def main(self):
        self.menu_name = 'LOG MENU'
        self.menu_options = {
            'add_today':
            {
                'name': 'Add today\'s log',
                'key': 'Enter',
                'command': self.add_log_today
            },
            # ('Add yesterday\'s log', 'y'),
            # ('Add specific day', 'DD-MM-YY'),
            # ('Return to main menu', 'q')
        }

    def add_log_today(self):
        today = calen.today()
        add_log_menu(today)

    def add_log_menu(self, date):
        if calen.check_existence(date):
            self._rewrite_log_menu(date)
        else:
            record = entry.new_entry(date)
            sheet.add_record(*record)
        self.text = self._show_added_record(date)

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

            self.execute_selection('y', self._rewrite_log)

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
