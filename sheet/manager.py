from .base import SQLQuery


class SQLQueryManager(SQLQuery):

    # CREATE

    def create_questions_group(self, name):
        query = """
        INSERT INTO questions_groups (name)
        VALUES (?)
        """
        self.cur.execute(query, (name,))
        self.conn.commit()

    def create_question(self, name_of_group, text, type, max_value=None):
        query = """
        INSERT INTO questions (name_of_group, text, type, max_value)
        VALUES (?, ?, ?, ?)
        """
        self.cur.execute(query, (name_of_group, text, type, max_value))
        self.conn.commit()

    def create_tag(self, id_of_question, *tags):
        query = """
        INSERT INTO tags (id_of_question, name)
        VALUES (?, ?)
        """
        for tag in tags:
            self.cur.execute(query, (id_of_question, tag))
            self.conn.commit()

    # DESTROY

    # MODIFY
