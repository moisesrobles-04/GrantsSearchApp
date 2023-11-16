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
            return user_list

    def getNPO_byName(self, names):
            cur = self.db.connection.cursor()
            query = """Select * From NPO where name =? """
            ex = (names,)
            cur.execute(query,ex)
            user_list = cur.fetchone()
            return user_list
    # def create_npo(self, name):


