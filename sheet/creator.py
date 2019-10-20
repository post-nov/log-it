from .base import SQLQuery


class SQLQueryCreator(SQLQuery):

    def create_table_if_not_exists(self):
        "Initial creation of tables"

        query_questions_groups = """
        CREATE TABLE IF NOT EXISTS questions_groups
        (
        name TEXT PRIMARY KEY NOT NULL UNIQUE
        );
        """

        query_questions = """
        CREATE TABLE IF NOT EXISTS questions
        (
        id            INTEGER PRIMARY KEY,
        name_of_group TEXT,
        text          TEXT NOT NULL,
        type          TEXT NOT NULL,
        max_value     INTEGER,

        CHECK (type IN ('integer', 'string', 'tags')),

        FOREIGN KEY (name_of_group)
        REFERENCES questions_groups (name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
        );
        """

        query_answers = """
        CREATE TABLE IF NOT EXISTS answers
        (
        id             INTEGER PRIMARY KEY,
        id_of_question INTEGER,
        id_of_record   INTEGER,

        FOREIGN KEY (id_of_record)
        REFERENCES records (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

        FOREIGN KEY (id_of_question)
        REFERENCES questions (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
        );
        """

        query_answers_int = """
        CREATE TABLE IF NOT EXISTS answers_int
        (
        id_of_answer INTEGER,
        value        INTEGER,

        FOREIGN KEY (id_of_answer)
        REFERENCES answers (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
        );
        """

        query_answers_str = """
        CREATE TABLE IF NOT EXISTS answers_str
        (
        id_of_answer INTEGER,
        value        TEXT,

        FOREIGN KEY (id_of_answer)
        REFERENCES answers (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
        );
        """

        query_answers_tags = """
        CREATE TABLE IF NOT EXISTS answers_tags
        (
        id_of_tag    INTEGER,
        id_of_answer INTEGER,

        FOREIGN KEY (id_of_tag)
        REFERENCES tags (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

        FOREIGN KEY (id_of_answer)
        REFERENCES answers (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
        );
        """

        query_tags = """
        CREATE TABLE IF NOT EXISTS tags
        (
        id             INTEGER PRIMARY KEY,
        id_of_question INTEGER,
        name           STRING,

        FOREIGN KEY (id_of_question)
        REFERENCES questions (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
        );
        """

        query_records = """
        CREATE TABLE IF NOT EXISTS records
        (
        id            INTEGER PRIMARY KEY,
        name_of_group TEXT,
        date          TEXT,

        FOREIGN KEY (name_of_group)
        REFERENCES questions_groups (name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
        );
        """

        queries = [
            query_questions_groups,
            query_questions,
            query_answers,
            query_answers_int,
            query_answers_str,
            query_answers_tags,
            query_tags,
            query_records
        ]

        for query in queries:
            self.cur.execute(query)
            self.conn.commit()
