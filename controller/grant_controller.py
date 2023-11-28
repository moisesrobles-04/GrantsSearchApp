from model.grant import grantDAO

class grantController:

    @staticmethod
    def build_grant_map_dict(row):
        result = {'g_id': row[0], 'o_number': row[1], 'o_title': row[2], 'agency': row[3],
                  'status': row[4], 'posteddate': row[5], 'closeddate': row[6],
                  'instrument': row[7], 'category': row[8], 'matching': row[9],
                  'awardceiling': row[10], 'awardfloor': row[11]}
        return result

    @staticmethod
    def build_error_map_dict(row):
        result = {'g_id': row[0], 'message': row[1]}
        return result

    """
    ================
           GET      
    ================
    """

    def get_all_grants(self, page):
        dao = grantDAO()
        cat_list = dao.getGrants(page)
        cats = [self.build_grant_map_dict(row) for row in cat_list]
        return cats

    def get_grant_by_id(self, g_id):
        dao = grantDAO()
        grant = dao.getGrants_byId(g_id)

        if grant == None:
            return self.build_error_map_dict([-1, "Grant does not exist"])

        return self.build_grant_map_dict(grant)

    def get_grant_by_NPOname(self, name):
        dao = grantDAO()
        grant = dao.getGrants_byNPOname(name)

        if len(grant)==0:
            return self.build_error_map_dict([-1, "Grant does not exist"])

        g_dict = [self.build_grant_map_dict(row) for row in grant]

        return g_dict

    def get_grant_by_NPOId(self, n_id):
        dao = grantDAO()
        grant = dao.getGrants_byNPOname(n_id)

        if grant == None:
            return self.build_error_map_dict([-1, "Grant does not exist"])

        return self.build_grant_map_dict(grant)


    """
    =====================
           CREATE      
    =====================
    """

    def create_grant(self, json):
        dao = grantDAO()
        grant_exists = dao.getGrants_byNumber(json["o_number"])
        if grant_exists != None:
            return self.build_error_map_dict([-1, f"Category {grant_exists[1]} already exist"])
        dao = grantDAO()
        c_id = dao.createGrant(json["o_number"], json["o_title"], json["agency"],
                               json["status"], json["posteddate"], json["closeddate"],
                               json["instrument"],json["category"], json["matching"],
                               json["awardceiling"], json["awardfloor"])
        grant= [c_id, json["category"]]
        g_dict = self.build_grant_map_dict(grant)
        return g_dict


    """
    =====================
           UPDATE      
    =====================
    """

    def update_grant(self, json):
        dao = grantDAO()
        grant_exist = dao.getGrants_byId(json["g_id"])
        if grant_exist == None:
            return self.build_error_map_dict([-1, f"NPO {grant_exist[1]} does not exist"])
        dao = grantDAO()
        grant = [json["c_id"], json["category"]]
        dao.updateGrant(grant[0], grant[1])
        g_dict = self.build_grant_map_dict(grant)
        return g_dict