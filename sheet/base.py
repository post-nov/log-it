import sqlite3


class SQLQuery:

    def __init__(self, database='./sheet.db'):
        self.database = database
        self.conn = sqlite3.connect(database)  # connection
        self.cur = self.conn.cursor()  # cursor

        self._enable_fk()

    def _enable_fk(self):
        # Because sqlite is a bitch and foreign_keys are disabled by default
        self.conn.execute('PRAGMA foreign_keys = True')
        self.conn.commit()
