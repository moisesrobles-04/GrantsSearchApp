from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

import csv
from sys import platform

from controller.npo_controller import npoController
from controller.npocat_controller import npocatController
from controller.categories_controller import categoryController
from controller.grant_controller import grantController
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
            self.reset_data()

    # Activate reset; on_enter fails when opening app
    def on_leave(self, *args):
        self.reset_value = True

    # Reset values
    def reset_data(self):
        self.ids.name_labels.text = "Which NPO are you looking for?"
        self.ids.NPO_dropdown.text = "Select NPOs"
        self.ids.NPO_dropdown.values = self.dropdown()

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

            # If the name is in the database enter page
            else:
                global npo_id
                npo_id = npo["n_id"]

                # Select name and change screen
                self.manager.get_screen("update_npo").ids.name_labels.text = npo["name"]
                self.manager.current = "update_npo"

        else:
            self.ids.name_labels.text = "No NPO selected"

    def get_grants(self):
        name = self.ids.NPO_dropdown.text
        g = grantController().get_grant_by_NPOname(name)
        # g = grantController().get_all_grants()
        if type(g) == dict:
            return f'No result found'

        else:
            with open("./data/Test.csv", "w") as file:
                w = csv.writer(file)
                w.writerow(g[0].keys())
                for elem in g:
                    print(elem)
                    w.writerow(elem.values())


# Update Window
class NpoUpdateWindow(Screen):

    # When entering page clear widget and create labels and checklist
    def on_pre_enter(self, *args):
        if not self.reenter:
            self.reset_data()

        elements = self.ids.boxes
        global npo_id
        self.npocat = npocatController().get_npocat_by_npoid(npo_id)
        self.widgets_creation()

        self.reenter = True

    # If there is no data in the database, skip activate
        if type(self.npocat) != dict:
            for i in range(0, len(elements.children) - 1, 2):
                labels = elements.children[i + 1]
                if isinstance(labels, Label) and any(
                        dictionary.get('category') == labels.text for dictionary in self.npocat):
                    if isinstance(elements.children[i], CheckBox):
                        elements.children[i].active = True

    # Reset labels and checkboxes and update npocat table
    def on_leave(self, *args):
        self.reenter = False
        self.check_list()
        self.ids.boxes.clear_widgets()

    # Create labels and checkboxes
    def widgets_creation(self):
        cat_list = categoryController().get_all_categories()
        if platform == "darwin":
            font_size = 23
            width = 550
            height = 50
            padding = 35
            text_size = (450,0)
        else:
            font_size = 14
            width = 455
            height = 35
            padding = 15
            text_size = (310,0)

        for cat in cat_list:
            l_name = cat['category']
            self.label = Label(text=l_name,
                               font_size=font_size,
                               halign="left",
                               valign="center",
                               text_size=text_size,
                               size_hint=(5, None),
                               padding=padding,
                               width=width,
                               height=height,
                               pos=(0, 0))

            c_name = "check_" + cat['category']
            self.check = CheckBox(color= [0.1,0.1,0.1,1])

            self.ids["box_" + l_name] = self.label
            self.ids[c_name] = self.check
            self.ids.boxes.add_widget(self.label)
            self.ids.boxes.add_widget(self.check)

    # Verify all checkboxes and save marked or deleted data
    def check_list(self):
        global npo_id
        temp = self.ids.boxes

        for i in range(0, len(temp.children) - 1, 2):
            box = temp.children[i]
            l = temp.children[i + 1]
            if isinstance(l, Label) and isinstance(box, CheckBox):

                cat = categoryController().get_category_by_name(l.text)
                npo_dict = {"n_id": npo_id, "c_id": cat['c_id']}

                if type(self.npocat) == dict:
                    if box.active:
                        npocatController().create_npocat(npo_dict)
                else:
                    if box.active and not any(dictionary.get('category') == l.text for dictionary in self.npocat):
                        npocatController().create_npocat(npo_dict)
                    elif not box.active and any(dictionary.get('category') == l.text for dictionary in self.npocat):
                        npocatController().delete_npocat(npo_dict)


    # Reset values
    def reset_data(self):
        self.ids.name_input.text = ""
        self.ids.boxes.clear_widgets()

    # Update the name of the NPO
    def change_name(self):
        name = self.ids.name_labels.text
        if name != "":
            npo = npoController().get_npo_by_name(name)
            if npo["n_id"] == -1:
                self.ids.name_labels.text = npo["name"]
            else:
                new_name = self.ids.name_input.text
                npo["name"] = new_name
                NpoPop(npo, "Update", name).open_pop()


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
        self.popup.dismiss(force=True)

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
