from model.db import Database
import sqlite3


class npocatDAO():

    def __init__(self):
        self.db = Database()

    def createNPOCat(self, n_id, c_id):
        try:
            cur = self.db.connection.cursor()
            query = """Insert into npocategory (n_id, c_id) values (?, ?)"""
            ex = (n_id, c_id)
            cur.execute(query, ex)
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing createNPOCat operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.rowcount
                cur.close()
                self.db.close()
                return result

    def updateNPOCat(self, n_id, c_id):
        try:
            cur = self.db.connection.cursor()
            query = """Update npocategory (n_id, c_id) set c_id = ?
                        where n_id = ?"""
            ex = (c_id, n_id)
            cur.execute(query, ex)
            cur.close()
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing updateNPOCat operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                self.db.close()

    def getNPOCat(self):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From npocategory"""
            cur.execute(query)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getNPOCat operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                self.db.close()
                return result

    def getNPOCat_byNpoId(self, n_id):
        try:
            cur = self.db.connection.cursor()
            query = """Select n_id, c_id, category From npocategory Natural inner join categories where n_id =? """
            ex = (n_id,)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getNPOCat_byNpoId operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                self.db.close()
                return result


    def getNPOCat_byCatId(self, c_id):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From npocategory where c_id = ?"""
            ex = (c_id,)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getNPOCat_byCatId operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def getNPOCat_byId(self, n_id, c_id):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From npocategory where n_id = ? and c_id = ?"""
            ex = (n_id, c_id)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getNPOCat_byId operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def delete_NPOCat(self, n_id, c_id):
        try:
            cur = self.db.connection.cursor()
            query = """Delete From npocategory where n_id = ? and c_id = ?"""
            ex = (n_id, c_id)
            result = cur.execute(query, ex)
            cur.close()
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing deleteNPOCat operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                self.db.close()
                return result


    def delete_allNPOCat(self, n_id):
        try:
            cur = self.db.connection.cursor()
            query = """Delete From npocategory where n_id = ?"""
            ex = (n_id, )
            result = cur.execute(query, ex)
            cur.close()
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing deleteAllNPOCat operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                self.db.close()
                return result