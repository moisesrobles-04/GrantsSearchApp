from model.db import Database
import sqlite3

class categoryDAO():

    def __init__(self):
        self.db = Database()

    def createCategory(self, category):
        try:
            cur = self.db.connection.cursor()
            query = """Insert into categories (category) values (?)
                    returning c_id"""
            ex = (category,)
            cur.execute(query, ex)
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing createCategory operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def getCategories(self):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From Category"""
            cur.execute(query)
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing getCategories operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                self.db.close()
                return result