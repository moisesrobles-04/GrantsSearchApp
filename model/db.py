import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("./data/grants.db")

    def close(self):
        self.connection.close()