from kivy.uix.screenmanager import Screen
from controller.grant_controller import grantController

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
