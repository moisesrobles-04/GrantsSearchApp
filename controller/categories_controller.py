from model.categories import categoryDAO

class categoryController:

    @staticmethod
    def build_category_map_dict(row):
        result = {'c_id': row[0], 'category': row[1]}
        return result

    """
    ================
           GET      
    ================
    """

    def get_all_categories(self):
        dao = categoryDAO()
        cat_list = dao.getCategories()
        cats = [self.build_category_map_dict(row) for row in cat_list]
        return cats

    def get_category_by_id(self, c_id):
        dao = categoryDAO()
        category = dao.getCategoriesbyId(c_id)

        if category == None:
            return self.build_category_map_dict([0, "Category does not exist"])

        return self.build_category_map_dict(category)

    def get_category_by_name(self, name):
        dao = categoryDAO()
        categories = dao.getCategoriesbyName(name)

        if categories == None:
            return self.build_category_map_dict([-1, "Category does not exist"])

        return self.build_category_map_dict(categories)

    """
    =====================
           CREATE      
    =====================
    """

    def create_category(self, json):
        dao = categoryDAO()
        category_exists = dao.getCategoriesbyName(json["category"])
        if category_exists != None:
            return self.build_category_map_dict([-1, f"Category {category_exists[1]} already exist"])
        dao = categoryDAO()
        c_id = dao.createCategory(json["category"])
        category= [c_id, json["category"]]
        cat_dict = self.build_category_map_dict(category)
        return cat_dict


    """
    =====================
           UPDATE      
    =====================
    """

    def update_npo(self, json):
        dao = categoryDAO()
        category_exist = dao.getCategoriesbyId(json["c_id"])
        if category_exist == None:
            return self.build_category_map_dict([-1, f"NPO {category_exist[1]} does not exist"])
        dao = categoryDAO()
        categories= [json["c_id"], json["category"]]
        dao.updateCategory(categories[0], categories[1])
        cat_dict = self.build_category_map_dict(categories)
        return cat_dict