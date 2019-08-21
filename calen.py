import datetime
import sheet


def _dates():
    records = sheet.list_all_records()
    dates = [str_to_dt(record[1], 'uni') for record in records]
    return dates


def _n_days_ago(n):
    tday = today()
    return (tday - datetime.timedelta(days=n))


def get_start_index(n):
    n_day_ago = _n_days_ago(n)
    start_index = 0
    for index, date in enumerate(_dates()):
        if date >= n_day_ago:
            start_index = index
            break
    return start_index


def check_existence(date):
    if date in _dates():
        return True
    else:
        return False


def str_to_dt(str, format='simple'):
    if format == 'simple':
        format = '%d-%m-%y'
    if format == 'uni':
        format = '%Y-%m-%d'
    return datetime.datetime.strptime(str, format).date()


def dt_to_str(dt, format='simple'):
    if format == 'simple':
        format = '%d-%m-%y'
    if format == 'uni':
        format = '%Y-%m-%d'
    return dt.strftime(format)


def last_date(dates):
    try:
        return dates[-1]
    except:
        return False


def today():
    return datetime.datetime.today().date()


def yesterday():
    today = datetime.datetime.today().date()
    yesterday = (today - datetime.timedelta(days=1))
    return yesterday


def is_correct_date(date):
    try:
        datetime.datetime.strptime(date, '%d-%m-%y').date()
        return True
    except:
        return False
