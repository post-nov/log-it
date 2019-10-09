from base import SQLQuery


class SQLQueryPuller(SQLQuery):

    def get_all_questions_by_group(self, name_of_group):
        query = """
        SELECT id, text, type, max_value
        FROM questions
        WHERE name_of_group = ?
        """
        self.cur.execute(query, (name_of_group,))
        questions = self.cur.fetchall()
        return questions

    def get_all_tags_by_question(self, id_of_question):
        query = """
        SELECT T.id, T.id_of_question, T.name
        FROM tags T
        INNER JOIN questions Q
        ON T.id_of_question = Q.id
        WHERE T.id_of_question = ?
        """
        self.cur.execute(query, (id_of_question,))
        tags = self.cur.fetchall()
        return tags

    def get_column_names(self, table_name):
        query = 'PRAGMA table_info(?)'
        self.cur.execute(query, (table_name,))
        columns = self.cur.fetchall()
        column_names = [col[1] for col in columns]
        return column_names

    def get_answers_by_question(self, id_of_question):
        query = """
        WITH Aid AS (
        SELECT A.id, Q.type FROM answers A
        INNER JOIN questions Q
        ON A.id_of_question = Q.id
        ),
        CASE Aid.type
            WHEN 'integer'
                THEN
                    SELECT Aint.id, Aint.value
                    FROM answers_int Aint
                    INNER JOIN Aid
                    ON Aint.id_of_answer = Aid.id
            WHEN 'string'
                THEN
                    SELECT Astr.id, Astr.value
                    FROM answers_str Astr
                    INNER JOIN Aid
                    ON Astr.id_of_answer = Aid.id
            WHEN 'tags'
                THEN
                    SELECT Atags.id_of_answer, T.name
                    FROM answers_tags Atags
                    INNER JOIN Aid
                    ON Atags.id_of_answer = Aid.id,
                    INNER JOIN tags T
                    ON Atags.id_of_tag = T.id
        """
        query_type_of_question = """
        SELECT type
        FROM questions
        WHERE id = ?
        """
        self.cur.execute(query_type_of_question, (id_of_question,))
        type = self.cur.fetchone()[0]
        if type == 'integer':
            query = """
            SELECT A.id,
                   Aint.id,
                   Aint.value
            FROM   answers_int Aint
                   INNER JOIN answers A
                           ON Aint.id_of_answer = A.id
            WHERE A.id_of_question = ?
            """
            self.cur.execute(query, (id_of_question,))
            answers = self.cur.fetchall()
            return answers
        elif type == 'string':
            query = """
            SELECT A.id,
                   Astr.id,
                   Astr.value
            FROM   answers_str Astr
                   INNER JOIN answers A
                           ON Astr.id_of_answer = A.id
            WHERE A.id_of_question = ?
            """
            self.cur.execute(query, (id_of_question,))
            answers = self.cur.fetchall()
            return answers
        elif type == 'tags':
            query = """
            SELECT A.id,
                   T.name
            FROM   tags T
                   INNER JOIN answers_tags AT
                           ON T.id = AT.id_of_tag
                   INNER JOIN answers A
                           ON AT.id_of_answer = A.id
            WHERE  A.id_of_question = ?
            """
            self.cur.execute(query, (id_of_question,))
            answers = self.cur.fetchall()
            return answers
