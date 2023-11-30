from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from controller.npo_controller import npoController

npo_id = -1

"""

NPO Window Hierarchy:
    NpoWindow
            |
            |---- NpoUpdateWindow
            |                   |
            |                   |---- NpoUpdatePop
            |
            |---- NpoCreateWindow
            |                   |
            |                   |---- NpoCreatePop
            |
            |---- NpoDeleteWindow
                                |
                                |---- NpoDeletePop
"""


# Defined our main window
class NpoWindow(Screen):
    reset_value = False

    # Update dropdown each time you enter the screen. After creating a new value
    def on_pre_enter(self, *args):
        if self.reset_value:
            self.ids.name_labels.text = "Which NPO are you looking for?"
            self.ids.NPO_dropdown.values = self.dropdown()

    # Activate reset; on_enter fails when opening app
    def on_leave(self, *args):
        self.reset_value = True

    # Get all NPOs and update dropdown
    def dropdown(self):
        n_list = npoController().get_all_npos()
        npos = []
        for elem in n_list:
            npos.append(elem["name"])
        return npos

    def press_npo(self):

        # Select dropdown value and check if its empty
        name = self.ids.NPO_dropdown.text
        self.ids.NPO_dropdown.values = self.dropdown()

        if name != "Select NPOs":
            npo = npoController().get_npo_by_name(name)

            # Check if name is in the database
            if npo["n_id"] == -1:
                self.ids.name_labels.text = npo["name"]

            else:
                # If the name is in the database enter page
                global npo_id
                npo_id = npo["n_id"]

                # Select name and change screen
                self.manager.get_screen("update_npo").ids.name_labels.text = npo["name"]
                self.manager.current = "update_npo"

        else:
            self.ids.name_labels.text = "No NPO selected"

    # Not in use
    def press_all_npos(self):
        n_list = npoController().get_all_npos()
        text = "The NPOs are:"
        for i in n_list:
            text += f'{i["name"]}, '

        self.ids.name_labels.text = text


# Update Window
class NpoUpdateWindow(Screen):

    def change_name(self):
        name = self.ids.input_name.text
        if name != "":
            npo = npoController().get_npo_by_name(name)
            if npo["n_id"] == -1:
                self.ids.name_labels.text = npo["name"]
            else:
                print(f'Are you sure you want to change {self.ids.name_labels.text} name to {name}')
                return

    # MUST FINISH FUNCTION (Update NPO's name and npocat)
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


# Create Window
class NpoCreateWindow(Screen):

    # Create NPO entry in the database. Open Popup to confirm value.
    def add_npo(self):
        name = self.ids.name_input.text
        npo_exists = npoController().get_npo_by_name(name)
        if npo_exists["n_id"] == -1:
            npo_exists["name"] = name

        NpoCreatePop(npo_exists).open_pop()


# Create Popup Window
class NpoCreatePop(FloatLayout):
    def __init__(self, npo):
        super().__init__()
        self.npo_id = npo["n_id"]
        self.npo_name = npo["name"]

    # Create popup with message
    def open_pop(self):
        self.message(self.npo_name)
        self.popup = Popup(title="PopupWindow", content=self, size_hint=(None, None), size=(700, 700))
        self.popup.open()

    def close_pop(self):
        self.popup.dismiss()

    def message(self, name):
        # If no NPO, add message to confirm
        if self.npo_id == -1:
            self.ids.name_label.text = f'Are you sure you want to create the NPO {name}?'
            self.ids.button_name.text = "Confirm"

        # If a NPO exist, throw exist message
        else:
            self.ids.name_label.text = f'NPO {name} already exist, cannot create'
            self.npo_name = "None"
            self.ids.button_name.text = "Return"

    def create(self, name):
        dict = {"name": name}
        create = npoController().create_npo(dict)
        return create


# Delete Window
class NpoDeleteWindow(Screen):
    # Delete NPO entry in the database. Open Popup to confirm value.
    def remove_npo(self):
        name = self.ids.name_input.text
        npo_exists = npoController().get_npo_by_name(name)
        if npo_exists["n_id"] == -1:
            npo_exists["name"] = name

        NpoCreatePop(npo_exists).open_pop()

# Delete Window
class NpoDeletePop(Screen):
    # Delete NPO entry in the database. Open Popup to confirm value.
    def __init__(self, npo):
        super().__init__()
        self.npo_id = npo["n_id"]
        self.npo_name = npo["name"]

    # Create popup with message
    def open_pop(self):
        self.message(self.npo_name)
        self.popup = Popup(title="PopupWindow", content=self, size_hint=(None, None), size=(700, 700))
        self.popup.open()

    def close_pop(self):
        self.popup.dismiss()

    def message(self, name):
        # If a NPO exist, add message to confirm delete
        if self.npo_id == -1:
            self.ids.name_label.text = f'Are you sure you want to delete the NPO {name}?'
            self.ids.button_name.text = "Confirm"

        # If a NPO does not exist, throw not found message
        else:
            self.ids.name_label.text = f'NPO {name} was not found'
            self.npo_name = "None"
            self.ids.button_name.text = "Return"

    def delete(self, name):
        dict = {"name": name}
        create = npoController().delete_npo(dict)
        return create