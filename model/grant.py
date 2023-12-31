from model.db import Database
import sqlite3


class grantDAO():

    def __init__(self):
        self.db = Database()

    def createGrant(self, number, title, agency, status, posted, closed, instrument, category, matching, ceiling, floor):
        try:
            cur = self.db.connection.cursor()
            query = """Insert into grants (o_number, o_title, agency, status, posteddate, closeddate
                        instrument, category, matching, awardceiling, awardfloor) 
                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    returning n_id"""
            ex = (number, title, agency, status, posted, closed, instrument, category, matching, ceiling, floor)
            cur.execute(query, ex)
            result = cur.fetchone()[0]
            cur.close()
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing createGrant operation", error)
            self.db.connection = None
        finally:
            if self.db.connection is not None:
                self.db.close()
                return result

    def updateGrant(self, g_id, number, title, agency, status, posted, closed, instrument, category, matching, ceiling, floor):
        try:
            cur = self.db.connection.cursor()
            query = """Update grants (o_number, o_title, agency, status, posteddate, closeddate
                        instrument, category, matching, awardceiling, awardfloor)  set o_number = ?, o_title = ?,
                        agency = ?, status = ?, posteddate = ?, closeddate = ?, instrument = ?, category = ?, matching = ?,
                        awardceiling = ?, awardfloor = ? 
                        where n_id = ?"""
            ex = (number, title, agency, status, posted, closed, instrument, category, matching, ceiling, floor, g_id)
            cur.execute(query, ex)
            cur.close()
            self.db.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print("Error executing updateGrant operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                self.db.close()

    def getGrants(self):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From grants"""
            cur.execute(query)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getGrants operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                self.db.close()
                return result

    def getGrants_byId(self, g_id):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From grants where g_id =?"""
            ex = (g_id,)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getGrants_byId operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def getGrants_byNumber(self, o_number):
        try:
            cur = self.db.connection.cursor()
            query = """Select * From grants where o_number =?"""
            ex = (o_number,)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getGrants_byNumber operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result


    def getGrants_byNPOname(self, name):
        try:
            cur = self.db.connection.cursor()
            query = """Select distinct g_id, o_number, o_title, agency, status, posteddate,
                        closeddate, instrument, g.category, matching, awardceiling, awardfloor
                        From (NPO Natural inner join npocategory natural inner join categories) as N,
                            grants as g
                        where (status = 'Posted' or status = 'Forecasted')
                        and (g.category Like ('%' || N.category || '%') or g.category like '%Category of Funding Activity:%')
                        and agency not Like '%USAID%' and agency not Like '%DOD%'
                        and agency not Like '%DOS%' and N.name Like ('%' || ? || '%')
                        and ((g.closeddate < Date(current_date, '6 months')
                        and g.closeddate > Date(current_date, '1 months')) or g.closeddate= '2099-01-01')
                        COLLATE NOCASE order by status desc, matching, g_id
                        """
            ex = (name,)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getGrants_byNPOname operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                self.db.close()
                return result


    def getGrants_byNPOId(self, n_id):
        try:
            cur = self.db.connection.cursor()
            query = """Select distinct g_id, o_number, o_title, agency, status, posteddate,
                        closeddate, instrument, g.category, matching, awardceiling, awardfloor
                        From (NPO Natural inner join npocategory natural inner join categories) as N,
                            grants as g
                        where (status = 'Posted' or status = 'Forecasted')
                        and (g.category Like ('%' || N.category || '%') or g.category like '%Category of Funding Activity:%')
                        and agency not Like '%USAID%' and agency not Like '%DOD%'
                        and agency not Like '%DOS%' and N.n_id = ?
                        and ((g.closeddate < Date(current_date, '6 months')
                        and g.closeddate > Date(current_date, '1 months')) or g.closeddate= '2099-01-01')
                        COLLATE NOCASE order by status desc, matching, g_id
                        """
            ex = (n_id,)
            cur.execute(query, ex)

        except(Exception, sqlite3.Error) as error:
            print("Error executing getGrants_byNPOId operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result
