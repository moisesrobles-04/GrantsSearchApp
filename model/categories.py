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
            result = cur.fetchone()
            cur.close()
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing createCategory operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                self.db.close()
                return result

    def updateCategory(self, c_id, category):
        try:
            cur = self.db.connection.cursor()
            query = """Update categories (category) set category = ?
                    where c_id = ?"""
            ex = (category,c_id)
            cur.execute(query, ex)
            cur.close()
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing updateCategory operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                self.db.close()

    def getCategories(self):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From categories"""
            cur.execute(query)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getCategories operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                return result

    def getCategoriesbyId(self, c_id):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From categories where c_id = ?"""
            ex = (c_id,)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getCategoriesbyId operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                return result

    def getCategoriesbyName(self, category):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From categories where category = ?"""
            ex = (category,)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getCategoriesbyName operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                return result

