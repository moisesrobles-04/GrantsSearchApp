import sqlite3
import csv
import os, os.path
import shutil
import datetime

def copy_db():
    path = "./data/backups/grants_" + str(datetime.datetime.today().date()) + ".db"
    new_path = path.replace("-", "_")
    if not os.path.isfile(new_path):
        shutil.copyfile("./data/grants.db", new_path)

if __name__ == "__main__":
    l = []
    copy_db()
    conn = sqlite3.connect("./data/grants.db")
    cur = conn.cursor()

    with open("./data/test.csv", "r", encoding='windows-1252') as f:
        read = csv.reader(f)
        read.__next__()
        for i in read:
            if i == []:
                continue
            tup = tuple(i)
            try:
                query = "INSERT INTO grants (o_number, o_title, agency, status, posteddate, closeddate, instrument, category, matching, awardceiling, awardfloor) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cur.execute(query, tup)
            except:
                print(tup)

            finally:
                conn.commit()

    print("Finished")
    cur.close()
    conn.close()