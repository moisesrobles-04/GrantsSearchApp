from model.npocat import npocatDAO
from model.npo import npoDAO
from model.categories import categoryDAO

class npocatController:

    @staticmethod
    def build_npocat_map_dict(row):
        result = {'n_id': row[0], 'c_id': row[1]}
        return result

    """
    ================
           GET      
    ================
    """

    def get_all_nposcat(self):
        dao = npocatDAO()
        npocat_list = dao.getNPOCat()
        nposcat = [self.build_npocat_map_dict(row) for row in npocat_list]
        return nposcat

    def get_npocat_by_npoid(self, n_id):
        dao = npoDAO()
        npo = dao.getNPO_byId(n_id)
        if not npo:
            return self.build_npocat_map_dict([-1, "NPO does not exist"])

        dao = npocatDAO()
        npocat = dao.getNPOCat_byNpoId(n_id)
        if not npocat:
            return self.build_npocat_map_dict([-1, "NPO has no category"])

        return self.build_npocat_map_dict(npocat)

    def get_npo_by_catId(self, c_id):
        dao = categoryDAO()
        cat = dao.getCategoriesbyId(c_id)
        if not cat:
            return self.build_npocat_map_dict([-1, "Category does not exist"])

        dao = npocatDAO()
        npocat = dao.getNPOCat_byCatId(c_id)
        if not npocat:
            return self.build_npocat_map_dict([-1, "There is no NPO with this category"])

        return self.build_npocat_map_dict(npocat)

    """
    =====================
           CREATE      
    =====================
    """

    def create_npocat(self, json):
        dao = npocatDAO()
        npocat_exist = dao.getNPOCat_byId(json["n_id"], json["c_id"])
        if npocat_exist:
            return self.build_npocat_map_dict([-1, f"NPO {npocat_exist[0]} already has category {npocat_exist[1]}"])
        dao = npocatDAO()
        dao.createNPOCat(json["n_id"], json["c_id"])
        npocat = [json["n_id"], json["c_id"]]
        npocat_dict = self.build_npocat_map_dict(npocat)
        return npocat_dict


    """
    =====================
           UPDATE      
    =====================
    """

    def update_npocat(self, json):
        dao = npocatDAO()
        npo_exist = dao.getNPOCat_byNpoId(json["n_id"])
        if not npo_exist:
            return self.build_npocat_map_dict([-1, f"NPO {npo_exist[0]} does not have the category {npo_exist[1]}"])
        dao = npocatDAO()
        npocat= [json["n_id"], json["c_id"]]
        dao.updateNPOCat(npocat[0], npocat[1])
        npocat_dict = self.build_npocat_map_dict(npocat)
        return npocat_dict