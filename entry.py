import datetime
from utils.text import (pretty_print,
                        pretty_input)


def _add_line(date):
    while True:
        pretty_print(f'Enter short line about {date}')
        line = pretty_input()
        if line == '':
            pretty_print('You haven\'t entered correct line.')
        elif len(line) > 300:
            pretty_print(['Line is too big for',
                          'Previous line:',
                          line])
        else:
            return line


def _add_time():
    while True:
        pretty_print('Enter productivity time')
        time = pretty_input()
        if time.isnumeric() and int(time) <= 3600 and int(time) >= 0:
            return time
        else:
            pretty_print('Try again?')


def _add_score():
    while True:
        pretty_print('Rate the day')
        score = pretty_input()
        if score.isnumeric() and int(score) <= 5 and int(score) >= 0:
            return score
        else:
            pretty_print('Try again?')


def new_entry(date):
    line = _add_line(date)
    time = _add_time()
    score = _add_score()
    return (date, line, time, score)
