import csv
import sqlite3

class Database:
    def __init__(self):
        try:
            with open("./data/grants.csv", "r") as f:
                r = csv.reader(f)
                path = r.__next__()
                f.close()

            self.connection = sqlite3.connect(path[0])

        except:
            print("failure")

        finally:
            pass

    def close(self):
        self.connection.close()