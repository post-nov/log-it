import sqlite3


class SQLQuery:
    database = 'sheet.db'
    conn = sqlite3.connect(database)  # connection
    cur = conn.cursor()  # cursor

    def close_after_finish(method):
        def wrapper_function(*args, **kwargs):
            # Because sqlite is a bitch and foreign_keys are disabled by default
            SQLQuery.conn.execute('PRAGMA foreign_keys = True')
            meth = method(*args, **kwargs)
            if 'commit' in kwargs.keys() and kwargs['commit'] == True:
                SQLQuery.cur.commit()
            SQLQuery.conn.close()
            return meth
        return wrapper_function

    @classmethod
    @close_after_finish
    def create_table_if_not_exists(cls):
        "Initial creation of tables"

        query_questions_groups = """
        CREATE TABLE IF NOT EXISTS questions_groups
        (
        id   INTEGER PRIMARY KEY,
        name TEXT
        );
        """

        query_questions = """
        CREATE TABLE IF NOT EXISTS questions
        (
        id          INTEGER PRIMARY KEY,
        id_of_group INTEGER,
        name        TEXT,
        type        TEXT CHECK (type IN ('integer', 'string', 'array')),
        max_value   INTEGER,
        FOREIGN KEY (id_of_group)
        REFERENCES groups_of_questions (id)
        );
        """
        query_records = """
        CREATE TABLE IF NOT EXISTS records
        (
        id                       INTEGER PRIMARY KEY,
        id_of_group              INTEGER,
        date                     TEXT,
        FOREIGN KEY (id_of_group)
        REFERENCES groups_of_questions (id)
        );
        """

        query_answers = """
        CREATE TABLE IF NOT EXISTS answers
        (
        id           INTEGER PRIMARY KEY,
        id_of_record INTEGER,
        value        TEXT,
        FOREIGN KEY (id_of_record)
        REFERENCES records(id)
        );
        """

        queries = [
            query_questions_groups,
            query_questions,
            query_records,
            query_answers
        ]

        for query in queries:
            SQLQuery.cur.execute(query)

    @classmethod
    @close_after_finish
    def create_group_of_questions(cls, name):
        query = """
        INSERT INTO groups_of_questions (name)
        VALUES (?)
        """
        SQLQuery.cur.execute(query, (name,))

    @classmethod
    @close_after_finish
    def get_column_names(cls, table_name):
        query = 'PRAGMA table_info({})'
        SQLQuery.cur.execute(query.format(table_name))
        columns = SQLQuery.cur.fetchall()
        column_names = [col[1] for col in columns]
        return column_names

    @classmethod
    @close_after_finish
    def get_questions_by_group(cls, id_of_group):
        query = """
        SELECT groups_of_questions.name, questions.name, questions.type
        FROM groups_of_questions
        INNER JOIN questions
        ON groups_of_questions.id = questions.id_of_group
        WHERE groups_of_questions.id = ?
        """
        SQLQuery.cur.execute(query, (id_of_group,))
        columns = SQLQuery.cur.fetchall()
        column_names = [col[1] for col in columns]
        return column_names


if __name__ == '__main__':
    SQLQuery.create_table_if_not_exists()
    #
    # questions = SQLQuery.get_questions_by_group(1)
    # print(questions)
