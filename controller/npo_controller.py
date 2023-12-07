from model.npo import npoDAO
from model.npocat import npocatDAO

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
        if type(npo_list)!= list:
            return None
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
            return self.build_npo_map_dict([-1, f"NPO {npo_exist[1]} already exist"])
        dao = npoDAO()
        row = dao.createNPO(json["name"])
        if row<1:
            return f'NPO {json["name"]} was not created'
        dao = npoDAO()
        npo = dao.getNPO_byName(json['name'])
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
        dao.updateNPO(npo[0], npo[1])
        npo_dict = self.build_npo_map_dict(npo)
        return npo_dict

    """
    =====================
           Delete      
    =====================
    """

    def delete_npo(self, json):
        dao = npoDAO()
        npo_exist = dao.getNPO_byName(json["name"])
        if npo_exist == None:
            return self.build_npo_map_dict([-1, f"NPO {npo_exist[1]} already exist"])
        npo_exist = self.build_npo_map_dict(npo_exist)
        dao = npocatDAO()

        dao.delete_allNPOCat(npo_exist["n_id"])

        get_dao = npocatDAO()
        valid = get_dao.getNPOCat_byNpoId(npo_exist["n_id"])

        if len(valid) == 0 or valid == None:
            dao = npoDAO()
            row = dao.deleteNPO(npo_exist["n_id"])

            if row.rowcount>0:
                return f'{json["name"]} was delete from the database'

            else:
                return f'NPO {json["name"]} did not delete correctly, try again'
        else:
            return f'NPO still have categories'