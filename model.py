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

