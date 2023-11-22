from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
import csv
from controller.npo_controller import npoController
from controller.categories_controller import categoryController

Builder.load_file('grants.kv')
Window.size = (700,700)

class MyLayout(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.name_labels.text = "Which NPO are you looking for?"

    def press_npo(self):
        name = self.ids.name_input.text
        if name != "":
            npo = npoController().get_npo_by_name(name)
            if npo["n_id"] ==-1:
                self.ids.name_labels.text = npo["name"]
            else:
                self.ids.name_labels.text = f'The #{npo["n_id"]} NPO is {npo["name"]}'
            self.ids.name_input.text = ""

    def press_all_npos(self):
        n_list = npoController().get_all_npos()
        text = "The NPOs are:"
        for i in n_list:
            text += f'{i["name"]}, '

        self.ids.name_labels.text = text

    def press_categories(self):
        c_list = categoryController().get_all_categories()
        text = "The Categories are:"
        for i in c_list:
            text += f'{i["category"]}, '

        self.ids.name_labels.text = text



class GrantsApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    GrantsApp().run()