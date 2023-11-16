import sqlite3 as sql3


def test():
    a = sql3.connect("./data/grants.db")
    b = a.cursor().execute("SELECT * FROM categories")

    print(b)
    a.close()

if __name__ == "__main__":
    test()
