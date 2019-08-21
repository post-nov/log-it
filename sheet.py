import sqlite3

dbfilename = 'sheet.db'


def create_table_if_not_exists():
    db = sqlite3.connect(dbfilename)
    c = db.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS records\
        ( id INTEGER PRIMARY KEY, \
          date     TEXT, \
          line     TEXT, \
          time   INTEGER, \
          score INTEGER \
          )"
    )
    db.commit()
    c.close()


def add_record(date='', line='', time='', score=''):
    db = sqlite3.connect(dbfilename)
    c = db.cursor()
    c.execute('INSERT INTO records(date, line, time, score) \
                VALUES(?,?,?,?)', (date, line, time, score))
    db.commit()
    c.close()


def update_record(id, date='', line='', time='', score=''):
    db = sqlite3.connect(dbfilename)
    c = db.cursor()
    c.execute('UPDATE records set date=?, line=?, time=?, score=? \
                WHERE id=?', (date, line, time, score, id))
    db.commit()
    c.close()


def delete_record(column='date', value=''):
    db = sqlite3.connect(dbfilename)
    c = db.cursor()
    c.execute(f'DELETE FROM records where {column}=?', (value,))
    db.commit()
    c.close()


def list_all_records(order='date'):
    db = sqlite3.connect(dbfilename)
    c = db.cursor()
    c.execute(f'SELECT * FROM records ORDER BY {order}')
    records = c.fetchall()
    c.close()
    return records


def get_record(column='date', value=''):
    db = sqlite3.connect(dbfilename)
    c = db.cursor()
    c.execute(f'SELECT * from records WHERE {column}=?', (value,))
    records = c.fetchall()
    c.close()
    return records[0]


def has_records():
    db = sqlite3.connect(dbfilename)
    c = db.cursor()
    c.execute('SELECT count(*) FROM records')
    counter = c.fetchone()[0]
    c.close()
    if counter > 0:
        return True
    else:
        return False


if __name__ == '__main__':
    print(has_records())
