import csv

import psycopg2

if __name__ == "__main__":
    l = []
    conn = psycopg2.connect("dbname=test1 user=user1 password=user1 host=localhost")
    cur = conn.cursor()

    with open("grants.csv", "r", encoding='windows-1252') as f:
        read = csv.reader(f)
        for i in read:
            tup = tuple(i)
            try:
                cur.execute("INSERT INTO newGrants(g_id, number, title, agency, status, posteddate, closedate, instrumenttype, category, matching, awardceiling, awardfloor)"
                            "Values (default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tup)
            except:
                print(tup)

            finally:
                conn.commit()

    cur.close()
    conn.close()