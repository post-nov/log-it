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
    size_of_vertical_bars = 5  # '|' - vertical bar
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
    centered_content = "{:^{length}}".format(content, length=length)
    return centered_content


def _head_row():
    "Creates row with column names"
    head_row = []
    columns = _get_columns()
    headers = list(columns.keys())
    widths = list(columns.values())
    for header, width in zip(headers, widths):
        cell = _cell(width, header)
        head_row.append(cell)
    return '|'.join(head_row)


def _table_row(record):
    "Creates row containing data from a record"
    table_row = []
    columns = _get_columns()
    widths = list(columns.values())
    for column, width in zip(record[1:], widths):
        cell = _cell(width, column)
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


def _get_max_length(*text):
    all_lengths = []
    for sentence in text:
        if isinstance(sentence, str):
            all_lengths.append(len(sentence))
        elif isinstance(sentence, tuple):
            all_lengths.append(len(sentence[0]))
        else:
            raise ValueError('Only strings or tuples are supported')
    return max(all_lengths)


def pretty_print(*text):
    max_length = _get_max_length(*text)
    print()
    for sentence in text:
        if isinstance(sentence, str):
            print('# ' + sentence)
        elif isinstance(sentence, tuple):
            desired_spaces = max_length - len(sentence[0])
            print('# ' + sentence[0] + desired_spaces*' ' + ' - ' + sentence[1])
    print()


def pretty_input():
    x = input(INPUT)
    print()
    return x.lower()


if __name__ == '__main__':
    pretty_print('TEXT')
    pretty_print('TEXT', 'ANOTHER TEXT')
    pretty_print('TEXT', ('WITH', 'TUPLE'))
    pretty_print('TEXT', ('WITH', 'TUPLE'), ('WITH DIFFERENT WIDTH', 'ELPUT'), ('WE', 'T'))
    pretty_print('FIRST PART', ('TUPLE WITH', 'OPTION'), 'SECOND PART')
