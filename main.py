import readline

from logger import Logger
from viewer import Viewer
from statistics import Statistics

from sheet import (create_table_if_not_exists,
                   has_records)
from utils.terminal import clear_screen
from utils.text import (pretty_print,
                        pretty_input,
                        pretty_tables)


class Interface:
    def __init__(self):
        self.logger = Logger()
        self.viewer = Viewer()
        self.statistics = Statistics()
        create_table_if_not_exists()
        clear_screen()

    def menu(self):
        while True:
            pretty_print(['MAIN MENU',
                          ('add new log', 'Enter'),
                          ('see last logs', 'l'),
                          ('see statistics', 's'),
                          ('exit', 'q')])
            selection = pretty_input()
            clear_screen()

            if selection == '':
                self.logger.menu()
            elif selection == 'l':
                if has_records():
                    self.viewer.menu()
                else:
                    pretty_print('There is no records yet.')
            elif selection == 's':
                if has_records():
                    self.statistics.menu()
                else:
                    pretty_print('There is no records yet.')
            elif selection == 'q':
                pretty_print('SEE YOU SPACE COWBOY...')
                break
            else:
                pretty_print('Try again')


if __name__ == '__main__':
    i = Interface()
    i.menu()
