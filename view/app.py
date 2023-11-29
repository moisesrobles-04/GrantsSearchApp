from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

import csv
from controller.npo_controller import npoController
from controller.categories_controller import categoryController
from controller.npocat_controller import npocatController
from controller.grant_controller import grantController

npo_id = -1


#Defined our different Windows
class NpoUpdateWindow(Screen):
    # def on_enter(self, *args):
    #     print("hello")
    #     self.clear_widgets()

    def npo_selected(self):
        pass


    def update_npo(self):
        name = self.ids.NPO_dropdown.text
        if name != "":
            npo = npoController().get_npo_by_name(name)
            if npo["n_id"] == -1:
                self.ids.name_labels.text = npo["name"]
            else:
                global npo_id
                npo_id = npo["n_id"]
                self.ids.name_labels.text = f'The #{npo["n_id"]} NPO is {npo["name"]}'


class NpoWindow(Screen):
    def on_pre_enter(self, *args):
        self.dropdown()

    def dropdown(self):
        n_list = npoController().get_all_npos()
        npos = []
        for elem in n_list:
            npos.append(elem["name"])
        return npos

    def press_npo(self):
        name = self.ids.NPO_dropdown.text
        if name != "":
            npo = npoController().get_npo_by_name(name)
            if npo["n_id"] ==-1:
                self.ids.name_labels.text = npo["name"]
            else:
                global npo_id
                npo_id = npo["n_id"]
                index = 0
                for i in self.manager.screens:
                    if i.name == "update_npo":
                        break
                    index +=1
                self.parent.screens[index].ids.name_labels.text = npo["name"]
                return "update_npo"

    def press_all_npos(self):
        n_list = npoController().get_all_npos()
        text = "The NPOs are:"
        for i in n_list:
            text += f'{i["name"]}, '

        self.ids.name_labels.text = text


class NpoCreateWindow(Screen):
    def add_npo(self):
        name = self.ids.name_input.text
        npo_exists = npoController().get_npo_by_name(name)
        if npo_exists["n_id"] == -1:
            npo_exists["name"] = name
            NpoCreatePop(npo_exists).open_pop()
        else:
            NpoCreatePop(npo_exists).open_pop()

class NpoCreatePop(FloatLayout):
    def __init__(self, npo):
        super().__init__()
        self.npo_id = npo["n_id"]
        self.npo_name = npo["name"]

    def open_pop(self):
        if self.npo_id == -1:
            self.message(self.npo_name)
            self.popup = Popup(title= "PopupWindow", content=self, size_hint= (None, None), size=(700,700))
        else:
            self.error(self.npo_name)
            self.popup = Popup(title= "PopupWindow", content= self, size_hint= (None, None), size=(700,700))

        self.popup.open()

    def close_pop(self):
        self.popup.dismiss()

    def message(self, name):
        self.ids.name_label.text = f'Are you sure you want to create the NPO {name}?'
        self.ids.button_name.text = "Confirm"


    def create(self, name):
        dict = {"name": name}
        create = npoController().create_npo(dict)
        return create

    def error(self, name):
        self.ids.name_label.text = f'NPO {name} already exist, cannot create'
        self.npo_name = "None"
        self.ids.button_name.text = "Return"


class NpoDeleteWindow(Screen):
    pass


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

class GrantWindow(Screen):
    # page = 0

    def press_grant(self):
        name = self.ids.name_input.text
        if name != "":
            grant = grantController().get_grant_by_NPOname(name)
            if type(grant) == dict:
                self.ids.name_labels.text = grant["message"]
            else:
                text = ''
                for elem in grant:
                    text += f'The #{elem["g_id"]} grant is {elem["o_number"]}, '
                self.ids.name_labels.text = text
            self.ids.name_input.text = ""

    def press_all_grants(self):
        g_list = grantController().get_all_grants(self.page)
        text = "The Grants are:"
        for i in g_list:
            text += f'{i["o_number"]}, '
        self.page += 1
        print(self.page)
        self.ids.name_labels.text = text

# class result():
#     with open("test.csv", "w") as file:
#         write = csv.writer(file)



class WindowManager(ScreenManager):
    pass

class GrantsApp(App):
    def build(self):
        return kv

kv = Builder.load_file('main.kv')
# Builder.load_file('npo.kv')
Window.size = (700,700)

if __name__ == '__main__':
    GrantsApp().run()