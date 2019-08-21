import getpass
import os


def get_terminal_width(fallback=(80, 24)):
    for i in range(0, 3):
        try:
            columns, rows = os.get_terminal_size(i)
        except OSError:
            continue
        break
    else:  # set default if the loop completes which means all failed
        columns, rows = fallback
    return columns


def get_user():
    return getpass.getuser()


def clear_screen(function=None):
    def wrapper(*args, **kwargs):
        import os
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        if function:
            function(*args, **kwargs)
    if function:
        return wrapper
    else:
        return wrapper()
