from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

import csv
from controller.npocat_controller import npocatController

from view.npo_view import *
from view.cat_view import *
from view.grant_view import *

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