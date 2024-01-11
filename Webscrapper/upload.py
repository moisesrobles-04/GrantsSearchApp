import sqlite3
import csv
import os, os.path
import shutil
import datetime


def copy_db():
    conn = sqlite3.connect("C:\\Users\\Moises_Robles04\\PycharmProjects\\grantsWebScrapper\\data\\grants.db")
    path = "C:\\Users\\Moises_Robles04\\PycharmProjects\\grantsWebScrapper\\data\\backups\\grants_" + str(
        datetime.datetime.today().date()) + ".db"
    new_path = path.replace("-", "_")
    if not os.path.isfile(new_path):
        shutil.copyfile("C:\\Users\\Moises_Robles04\\PycharmProjects\\grantsWebScrapper\\data\\grants.db", new_path)


def remove_old_data():
    conn = sqlite3.connect("C:\\Users\\Moises_Robles04\\PycharmProjects\\grantsWebScrapper\\data\\grants.db")
    cur = conn.cursor()
    query = "DELETE FROM grants WHERE closeddate<Date(current_date)"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    print("==============================")
    print("Delete old data was successful")


if __name__ == "__main__":
    l = []
    copy_db()
    conn = sqlite3.connect("C:\\Users\\Moises_Robles04\\PycharmProjects\\grantsWebScrapper\\data\\grants.db")
    cur = conn.cursor()

    with open("Grants_data_2024-01-10.csv", "r", encoding='windows-1252') as f:
        read = csv.reader(f)
        read.__next__()
        for i in read:
            if i == []:
                continue

            # Format date correctly
            date_format = str(datetime.datetime.strptime(i[4], '%m/%d/%Y'))
            date_split = date_format.split(' ')
            i[4] = date_split[0]

            date_format = str(datetime.datetime.strptime(i[5], '%m/%d/%Y'))
            date_split = date_format.split(' ')
            i[5] = date_split[0]

            tup = tuple(i)
            try:
                query = "INSERT INTO grants (o_number, o_title, agency, status, posteddate, closeddate, instrument, category, matching, awardceiling, awardfloor) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cur.execute(query, tup)
            except:
                print(tup)

            finally:
                conn.commit()

    print("Finished copying")
    cur.close()
    conn.close()

    remove_old_data()
