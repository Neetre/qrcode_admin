import sqlite3


class DataManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS codes (id INTEGER PRIMARY KEY, data TEXT, used INTEGER DEFAULT 0)'''
        )
        self.conn.commit()

    def insert_code(self, data):
        self.cursor.execute('''INSERT INTO codes (data) VALUES (?)''', (data,))
        self.conn.commit()

    def get_codes(self):
        self.cursor.execute('''SELECT * FROM codes''')
        return self.cursor.fetchall()
    
    def get_single_code(self, data):
        self.cursor.execute('''SELECT * FROM codes WHERE data = ?''', (data,))
        return self.cursor.fetchone()
    
    def close(self):
        self.conn.close()
