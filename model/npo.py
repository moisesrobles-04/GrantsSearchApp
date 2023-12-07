from model.db import Database
import sqlite3


class npoDAO():

    def __init__(self):
        self.db = Database()

    def createNPO(self, name):
        try:
            cur = self.db.connection.cursor()
            query = """Insert into NPO (name) values (?)"""
            ex = (name,)
            cur.execute(query, ex)
            self.db.connection.commit()
        except(Exception, sqlite3.Error) as error:
            print("Error executing createNPO operation", error)
            self.db.connection = None
        finally:
            if self.db.connection is not None:
                result = cur.rowcount
                cur.close()
                self.db.close()
                return result

    def updateNPO(self, n_id, name):
        try:
            cur = self.db.connection.cursor()
            query = """Update NPO set name = ?
                        where n_id = ?"""
            ex = (name, n_id)
            cur.execute(query, ex)
            cur.close()
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing updateNPO operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                self.db.close()

    def getNPO(self):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From NPO order by name"""
            cur.execute(query)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getNPO operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                self.db.close()
                return result

    def getNPO_byId(self, n_id):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From NPO where n_id =? """
            ex = (n_id,)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getNPO_byId operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result


    def getNPO_byName(self, name):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From NPO where name =? COLLATE NOCASE"""
            ex = (name,)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getNPO_byName operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def deleteNPO(self, n_id):
        try:
            cur = self.db.connection.cursor()
            query = """Delete From NPO where n_id = ?"""
            ex = (n_id,)
            result = cur.execute(query, ex)
            cur.close()
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing deleteNPO operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                self.db.close()
                return result