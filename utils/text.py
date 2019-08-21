from . import terminal

USER = terminal.get_user()
INPUT = (USER+'@logger: ')


def _get_columns():
    "Gives proper length of columns with terminal width in mind"
    columns = {'date': 10,
               'line': None,
               'time': 5,
               'score': 5}
    line_width = _get_line_width(columns)
    columns['line'] = line_width
    return columns


def _get_line_width(columns):
    terminal_width = terminal.get_terminal_width()
    size_of_vertical_bars = 5
    size_of_other_columns = sum([columns['date'],
                                 columns['time'],
                                 columns['score']])
    return terminal_width - size_of_vertical_bars - size_of_other_columns


def _cell(length, content):
    """
    Gives a line with evenly distributed spaces on both sides,
    etc. centers content.
    """
    content = str(content)[:length]
    content_length = len(content)
    gap_length = length - content_length
    first_gap = gap_length // 2
    second_gap = gap_length - first_gap
    return (first_gap*' ' + content + second_gap*' ')


def _head_row():
    "Creates row with column names"
    head_row = []
    for column in _get_columns():
        cell = _cell(_get_columns()[column], column.upper())
        head_row.append(cell)
    return '|'.join(head_row)


def _table_row(record):
    "Creates row containing data from a record"
    table_row = []
    for column, length in zip(record[1:], _get_columns().values()):
        cell = _cell(length, column)
        table_row.append(cell)
    return '|'.join(table_row)


def pretty_tables(tables):
    "Creates table as beautiful as Mona Lisa"
    if isinstance(tables, tuple):  # If there is only one record
        tables = [tables]
    width_of_table = sum(list(_get_columns().values()))+5

    print('-'*width_of_table)
    print('|' + _head_row() + '|')
    print('-'*width_of_table)
    for row in tables:
        print('|' + _table_row(row) + '|')
    print('-'*width_of_table)
    print()


def pretty_print(text):
    if isinstance(text, list):
        max_l = 0
        for sentence in text:
            if isinstance(sentence, tuple):
                if len(sentence[0]) > max_l:
                    max_l = len(sentence[0])
        for sentence in text:
            if isinstance(sentence, tuple):
                desired_spaces = max_l - len(sentence[0])
                print('# ' + sentence[0] + desired_spaces*' ' + ' - ' + sentence[1])
            else:
                print('# ' + sentence)
    else:
        print('# ' + text)
    print()


def pretty_input():
    x = input(INPUT)
    print()
    return x.lower()
