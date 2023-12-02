from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.clock import Clock
import time

from controller.npo_controller import npoController
from controller.npocat_controller import npocatController

npo_id = -1

"""

NPO Window Hierarchy:
    NpoWindow
            |
            |---- NpoUpdateWindow
            |           |
            |           |---- NpoPop
            |
            |---- NpoCreateWindow
            |           |            
            |           |---- NpoPop
            |
            |---- NpoDeleteWindow
                        |
                        |---- NpoPop
"""


# Defined our main window
class NpoWindow(Screen):
    reset_value = False

    # Update dropdown each time you enter the screen. After creating a new value
    def on_pre_enter(self, *args):
        if self.reset_value:
            self.ids.name_labels.text = "Which NPO are you looking for?"
            self.ids.NPO_dropdown.text = "Select NPOs"
            self.ids.NPO_dropdown.values = self.dropdown()
            self.manager.get_screen("update_npo").remove_widget(self.manager.get_screen("update_npo").btn)


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


# Update Window
class NpoUpdateWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        global npo_id
        self.npocat = npocatController().get_npocat_by_npoid(npo_id)

    def switch(self):
        self.ids.check_health.active = True

    def on_leave(self, *args):

        for elem in self.npocat:
            update = npocatController().update_npocat(elem)

    # def on_pre_enter(self, *args):
    #     time.sleep(1)
        # Must create checklist independently, cannot use for loop :/
        # for i in range(5):
        #     pos = 0.1 * i
        #     self.btn = Button(text='My first button',
        #                       size_hint_x= None,
        #                       width= 500,
        #                       size_hint_y = None,
        #                       height= 50,
        #                       padding = 20,
        #                       pos_hint={'top': pos, 'right': 0.4})
        #     self.add_widget(self.btn)

    # Verify all checkboxes and mark them (code partially working)
    def check_list(self):
        global npo_id
        temp = self.ids.boxes
        check_list = npocatController().get_npocat_by_npoid(npo_id)
        temp_label = ""
        for i in range(0, len(temp.children)-1, 2):
            box = temp.children[i]
            l = temp.children[i+1]
            if isinstance(l, Label):
                temp_label = l.text

            if isinstance(box, CheckBox):
                l.text = "Temporary " + str(i)
                if temp_label in check_list:
                    print(box)

    def on_pre_leave(self, *args):
        self.remove_widget(self.btn)

    #Update the name of the NPO
    def change_name(self):
        name = self.ids.name_labels.text
        if name != "":
            npo = npoController().get_npo_by_name(name)
            if npo["n_id"] == -1:
                self.ids.name_labels.text = npo["name"]
            else:
                new_name = self.ids.input_label.text
                npo["name"] = new_name
                NpoPop(npo, "Update", name).open_pop()


    # MUST FINISH FUNCTION (Update NPO's npocat)
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
    def on_pre_enter(self, *args):
        self.ids.name_input.text = ""

    # Create NPO entry in the database. Open Popup to confirm value.
    def add_npo(self):
        name = self.ids.name_input.text
        if name != "":
            npo_exists = npoController().get_npo_by_name(name)
            if npo_exists["n_id"] == -1:
                npo_exists["name"] = name

            NpoPop(npo_exists, "Create").open_pop()


# Delete Window
class NpoDeleteWindow(Screen):

    def on_pre_enter(self, *args):
        self.ids.NPO_dropdown.text = "NPOs"
        self.ids.NPO_dropdown.values = self.manager.get_screen("first").ids.NPO_dropdown.values

    # Delete NPO entry in the database. Open Popup to confirm value.
    def remove_npo(self):
        name = self.ids.NPO_dropdown.text
        if name != "NPOs":
            npo_exists = npoController().get_npo_by_name(name)
            if npo_exists["n_id"] == -1:
                npo_exists["name"] = name

            NpoPop(npo_exists, "Delete").open_pop()


# Create Popup Window
class NpoPop(FloatLayout):
    def __init__(self, npo, action, old_name=None):
        super().__init__()
        self.npo_id = npo["n_id"]
        self.npo_name = npo["name"]
        self.action = action
        self.old_name = old_name

    # Create popup with message
    def open_pop(self):
        self.message(self.npo_name)
        self.popup = Popup(title="PopupWindow", content=self, size_hint=(None, None), size=(668, 700))
        self.popup.open()

    def close_pop(self):
        self.popup.dismiss()

    def message(self, name):
        # Create Messages
        if self.action == "Create":
            # If no NPO, add message to confirm
            if self.npo_id == -1:
                self.ids.name_label.text = f'Are you sure you want to create the NPO {name}?'
                self.ids.confirm_button.text = "Confirm"

            # If a NPO exist, throw exist message
            else:
                self.ids.name_label.text = f'NPO {name} already exist, cannot create'
                self.npo_name = "None"
                self.ids.confirm_button.text = "Return"

        # Delete Messages
        elif self.action == "Delete":
            # If a NPO exist, add message to confirm delete
            if self.npo_id != -1:
                self.ids.name_label.text = f'Are you sure you want to delete the NPO {name}?'
                self.ids.confirm_button.text = "Confirm"

            # If a NPO does not exist, throw not found message
            else:
                self.ids.name_label.text = f'NPO {name} was not found'
                self.npo_name = "None"
                self.ids.confirm_button.text = "Return"

        # Update Messages
        elif self.action == "Update":
            # If a NPO exist, add message to confirm delete
            if self.npo_id != -1:
                self.ids.name_label.text = f'Are you sure you want to change' \
                                           f' {self.old_name}\'s name to {name}?'
                self.ids.confirm_button.text = "Confirm"

            # If a NPO does not exist, throw not found message
            else:
                self.ids.name_label.text = f'NPO {name} was not found'
                self.npo_name = "None"
                self.ids.confirm_button.text = "Return"

    # Crud operations for the pop-up window
    def crud_action(self, name):
        if self.action == "Create":
            dict = {"name": name}
            create = npoController().create_npo(dict)
            return create

        elif self.action == "Delete":
            dict = {"name": name}
            delete = npoController().delete_npo(dict)
            return delete

        elif self.action == "Update":
            global npo_id
            dict = {"n_id": npo_id, "name": name}
            update = npoController().update_npo(dict)
            return update


