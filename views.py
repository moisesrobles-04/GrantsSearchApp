import sqlite3 as sql3
from model.npo import npoDAO

def test():
    a = sql3.connect("./data/grants.db")
    b = a.cursor().execute("SELECT * FROM categories")

    print(b.fetchall())
    a.close()

if __name__ == "__main__":
    npoDAO().getNPO()
