from model.npo import npoDAO

class npoController:

    @staticmethod
    def build_npo_map_dict(row):
        result = {'n_id': row[0], 'name': row[1]}
        return result

    """
    ================
           GET      
    ================
    """

    def get_all_npos(self):
        dao = npoDAO()
        npo_list = dao.getNPO()
        npos = [self.build_npo_map_dict(row) for row in npo_list]
        return npos

    def get_npo_by_id(self, n_id):
        dao = npoDAO()
        npo = dao.getNPO_byId(n_id)

        if npo == None:
            return self.build_npo_map_dict([0, "NPO does not exist"])

        return self.build_npo_map_dict(npo)

    def get_npo_by_name(self, name):
        dao = npoDAO()
        npo = dao.getNPO_byName(name)

        if npo == None:
            return self.build_npo_map_dict([-1, "NPO does not exist"])

        return self.build_npo_map_dict(npo)


    """
    =====================
           CREATE      
    =====================
    """

    def create_npo(self, json):
        dao = npoDAO()
        npo_exist = dao.getNPO_byName(json["name"])
        if npo_exist != None:
            return self.build_npo_map_dict([-1, "NPO already exists"])
        dao = npoDAO()
        n_id = dao.createNPO(json["name"])
        npo= [n_id, json["name"]]
        npo_dict = self.build_npo_map_dict(npo)
        return npo_dict

    """
    =====================
           CREATE      
    =====================
    """

    def create_npo(self, json):
        dao = npoDAO()
        npo_exist = dao.getNPO_byName(json["name"])
        if npo_exist != None:
            return self.build_npo_map_dict([-1, f"NPO {npo_exist[1]} already exist"])
        dao = npoDAO()
        n_id = dao.createNPO(json["name"])
        npo= [n_id, json["name"]]
        npo_dict = self.build_npo_map_dict(npo)
        return npo_dict


    """
    =====================
           UPDATE      
    =====================
    """

    def update_npo(self, json):
        dao = npoDAO()
        npo_exist = dao.getNPO_byId(json["n_id"])
        if npo_exist == None:
            return self.build_npo_map_dict([-1, f"NPO {npo_exist[1]} does not exist"])
        dao = npoDAO()
        npo= [json["n_id"], json["name"]]
        dao.updateNPO(npo)
        npo_dict = self.build_npo_map_dict(npo)
        return npo_dict