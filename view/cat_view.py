from kivy.uix.screenmanager import Screen

from controller.categories_controller import categoryController


class CategoryWindow(Screen):
    def press_category(self):
        name = self.ids.name_input.text
        if name != "":
            cat = categoryController().get_category_by_name(name)
            if cat["c_id"] ==-1:
                self.ids.name_labels.text = cat["category"]
            else:
                self.ids.name_labels.text = f'The #{cat["c_id"]} Category is {cat["category"]}'
            self.ids.name_input.text = ""

    def press_all_categories(self):
        c_list = categoryController().get_all_categories()
        text = "The Categories are:"
        for i in c_list:
            text += f'{i["category"]}, '

        self.ids.name_labels.text = text