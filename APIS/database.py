# database.py
import mysql.connector


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            user='root',
            password='root',
            host='localhost',
            database='mydb',
            port=3306,
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def execute_query(self, query, data=None):
        self.cursor.execute(query, data)
        return self.cursor.fetchall()

    def execute_insert_query(self, query, data):
        self.cursor.execute(query, data)
        self.conn.commit()
        return self.cursor.lastrowid

    def close(self):
        self.cursor.close()
        self.conn.close()
