import psycopg2

if __name__ == "__main__":

    conn = psycopg2.connect("dbname=test1 user=user1 password=user1 host=localhost")
    cur = conn.cursor()
    with open("Total Grants.csv", "r") as f:
        cur.copy_from(f, "Grants", sep=",")

    conn.commit()
    cur.close()
    conn.close()