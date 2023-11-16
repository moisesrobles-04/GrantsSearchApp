from model.db import Database
import sqlite3


class npoDAO():

    def __init__(self):
        self.db = Database()

    def getNPO(self):
            cur = self.db.connection.cursor()
            query = """Select * From NPO"""
            cur.execute(query)
            user_list = [row for row in cur]
            print(user_list)
    # def create_npo(self, name):


