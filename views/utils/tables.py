from . import terminal


def _cell(size, content):
    """
    Gives a line with evenly distributed spaces on both sides,
    etc. centers content.
    """
    content = str(content)[:size]
    centered_content = "{:^{size}}".format(content, size=size)
    return centered_content


def _table_row(sizes, record):
    "Creates row containing data from a record"
    table_row = []
    for size, column in zip(sizes, record[1:]):
        cell = _cell(size, column)
        table_row.append(cell)
    return '|'.join(table_row)


def _get_columns_sizes(columns):

    terminal_width = terminal.get_terminal_width()
    size_of_vertical_bars = len(columns) + 1  # '|' - vertical bar
    size_of_other_columns = sum(columns)

    # Main column should be single and it's size should be ZERO
    main_column = terminal_width - size_of_vertical_bars - size_of_other_columns
    return tuple([col if col else main_column for col in columns])


def pretty_tables(column_sizes, records, heads):
    '''
    Not ideal but pretty robust variant of table visualization in CLI
    There are few restrictions, such as:
    1. User must provide all 3 arguments
    2. Column sizes must contain one and only one 0

    '''
    column_sizes = _get_columns_sizes(column_sizes)
    if isinstance(records, tuple):  # If there is only
        records = [records]         # one record in records
    table_size = sum(column_sizes) + len(column_sizes) + 1
    # It's all about modularity
    table_head_top = ('-'*table_size)
    table_head_titles = ('|' + _table_row(column_sizes, heads) + '|')
    table_head_bot = ('-'*table_size)
    table_core = '\n'.join([('|' + _table_row(column_sizes, row) + '|') for row in records])
    table_bottom = ('-'*table_size)

    pretty_table = '\n'.join([
        table_head_top,
        table_head_titles,
        table_head_bot,
        table_core,
        table_bottom
    ])
    return pretty_table


if __name__ == '__main__':
    pretty_tables(
        (6, 0, 5, 4),
        # [
        (1, '320-23', 'GOOOOOOOD MOOORNIIING AMERICA', '11', 'BOOMOOOO'),
        # (2, '321-73', 'Whats up, bro?', '22', 'MO'),
        # ],
        ('id', 'INCX', 'TITLE', 'NT', 'CODE')
    )
