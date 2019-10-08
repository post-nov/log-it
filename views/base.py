from .utils.text import pretty_print, pretty_input
from .utils.terminal import clear_screen


class View:
    def __init__(self):
        self.text = None
        self._quit = False

    def execute_option(self, selection, options):
        self.text = None
        for option in options.values():
            if selection == option['key']:
                return option['command']()
            elif selection == '' and option['key'] == 'Enter':
                return option['command']()

        self.text = 'Wrong key. Try again'

    def _options_as_tuple(self, options_as_dict):
        options = tuple((option['name'], option['key']) for option in options_as_dict.values())
        return options

    def _add_exit_option(self, options):
        options['exit'] = {'name': 'quit', 'key': 'q', 'command': self.quit}
        return options

    def menu(self, menu_name, menu_options):
        menu_options = self._add_exit_option(menu_options)
        while True:
            clear_screen()
            if self.text:
                pretty_print(self.text)
            pretty_print(menu_name, with_spaces=False)
            pretty_print(*self._options_as_tuple(menu_options))
            selection = pretty_input()
            self.execute_option(selection, menu_options)
            if self._quit == True:
                self._quit = False
                break

    def main(self):
        self.menu(self.menu_name, self.menu_options)

    def quit(self):
        self._quit = True
        return
