from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from controller.npo_controller import npoController


npo_id = -1

#Defined our different Windows
class NpoUpdateWindow(Screen):

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

