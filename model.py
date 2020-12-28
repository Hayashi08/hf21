import mysql.connector

class MySQL:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='',
            database='hf21_db',
            charset='utf8'
        )
        self.cur = self.conn.cursor()
    
    def close(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def signup(self, user_name, password):
        self.cur.execute('SELECT user_name, password FROM user_tbl WHERE user_name = %s', (user_name,))
        row = self.cur.fetchone()
        
        if (row == None):
            self.cur.execute('INSERT INTO user_tbl (user_name, password) VALUES (%s, %s)', (user_name, password))
        else:
            return False

        return True

    def login(self, user_name, password):
        self.cur.execute('SELECT user_id, user_name, password FROM user_tbl where user_name = %s AND password = %s', (user_name, password))
        row = self.cur.fetchone()

        if (row == None):
            return False, None
        else:
            return True, row[0]

    def user_loader(self, user_id):
        self.cur.execute('SELECT user_name FROM user_tbl WHERE user_id = %s', (user_id,))
        row = self.cur.fetchone()

        if (row == None):
            return None
        else:
            return row[0]

    def insert_session(self, user_id, company_name, company_stage):
        self.cur.execute('INSERT INTO session_tbl (user_id, company_name, company_stage) VALUES (%s, %s, %s)', (user_id, company_name, company_stage))

        self.cur.execute('SELECT MAX(session_id), session_timestamp from session_tbl WHERE user_id = %s', (user_id,))
        row = self.cur.fetchone()

        return row[0], row[1]

    def insert_result(self, session_id, result_start_time, result_end_time):
        self.cur.execute('INSERT INTO result_tbl (session_id, result_start_time, result_end_time) VALUES (%s, %s, %s)', (session_id, result_start_time, result_end_time))

        self.cur.execute('SELECT MAX(result_id) FROM result_tbl WHERE session_id = %s', (session_id,))
        row = self.cur.fetchone()

        return row[0]

    def insert_sentence(self, result_id, sentence_time, sentence_str, sentence_wasoku):
        self.cur.execute('INSERT INTO sentence_tbl (result_id, sentence_time, sentence_str, sentence_wasoku) VALUES (%s, %s, %s, %s)', (result_id, sentence_time, sentence_str, sentence_wasoku))

    def insert_image(self, result_id, image_time, image_path, image_judge):
        self.cur.execute('INSERT INTO image_tbl (result_id, image_time, image_path, image_judge) VALUES (%s, %s, %s, %s)', (result_id, image_time, image_path, image_judge))

    def archive(self, user_id):
        self.cur.execute('SELECT session_id, session_timestamp, company_name, company_stage FROM session_tbl WHERE user_id = %s', (user_id,))
        rows = self.cur.fetchall()
        return rows

    def archive_detail(self, session_id):
        self.cur.execute('SELECT session_timestamp, company_name, company_stage FROM session_tbl WHERE session_id = %s', (session_id,))
        row_session = self.cur.fetchone()

        self.cur.execute('SELECT result_id, result_start_time, result_end_time FROM result_tbl WHERE session_id = %s', (session_id,))
        row_result = self.cur.fetchone()

        self.cur.execute('SELECT sentence_time, sentence_str, sentence_wasoku FROM sentence_tbl WHERE result_id = %s', (row_result[0],))
        rows_sentence = self.cur.fetchall()

        self.cur.execute('SELECT image_time, image_path, image_judge FROM image_tbl WHERE result_id = %s', (row_result[0],))
        rows_image = self.cur.fetchall()

        log_list = []
        for row_sentence in rows_sentence:
            log_list.append({'time': row_sentence[0], 'type': 'text', 'score': str(row_sentence[2]), 'content': row_sentence[1]})
        for row_image in rows_image:
            log_list.append({'time': row_image[0], 'type': 'image', 'score': row_image[2], 'content': row_sentence[1]})
        log_list = sorted(log_list, key = lambda x: x['time'])

        return row_session, row_result, log_list


