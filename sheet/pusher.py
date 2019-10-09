from base import SQLQuery


class SQLQueryPusher(SQLQuery):

    def add_record(self, date, name_of_group):
        query = """
        INSERT INTO records (date, name_of_group)
        VALUES (?, ?)
        """
        self.cur.execute(query, (date, name_of_group))
        self.conn.commit()
        return self.cur.lastrowid

    def _add_answer_tags(self, id_of_answer, tags):
        query = """
        INSERT INTO answers_tags (id_of_answer, id_of_tag)
        VALUES (?, ?)
        """
        for id_of_tag in tags:
            self.cur.execute(query, (id_of_answer, id_of_tag))
            self.conn.commit()

    def _add_answer_int(self, id_of_answer, value):
        query = """
        INSERT INTO answers_int (id_of_answer, value)
        VALUES (?, ?)
        """
        self.cur.execute(query, (id_of_answer, value))

    def _add_answer_str(self, id_of_answer, value):
        query = """
        INSERT INTO answers_str (id_of_answer, value)
        VALUES (?, ?)
        """
        self.cur.execute(query, (id_of_answer, value))

    def add_answer(self, id_of_record, id_of_question, value):
        query = """
        INSERT INTO answers (id_of_record, id_of_question)
        VALUES (?, ?)
        """
        self.cur.execute(query, (id_of_record, id_of_question))
        last_id = self.cur.lastrowid
        if isinstance(value, int):
            self._add_answer_int(last_id, value)
        elif isinstance(value, str):
            self._add_answer_str(last_id, value)
        elif isinstance(value, list):
            self._add_answer_tags(last_id, value)
        self.conn.commit()
