from model.npo import npoDAO

class npoController:

    @staticmethod
    def build_npo_map_dict(row):
        result = {'n_id': row[0], 'name': row[1]}
        return result

    def get_all_npos(self):
        dao = npoDAO()
        npo_list = dao.getNPO()
        npos = [self.build_npo_map_dict(row) for row in npo_list]
        return npos

    def get_npo_by_name(self, name):
        dao = npoDAO()
        npo = dao.getNPO_byName(name)

        if npo == None:
            return self.build_npo_map_dict([0, "NPO does not exist"])

        return self.build_npo_map_dict(npo)