from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from sys import platform

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

# Class to choose path to save information
class NpoFileWindow(Screen):
    def selected(self, filename):
        try:
            self.path = filename[0]
        except:
            pass

        finally:
            if self.path != "":
                with open("./data/path.csv", "w") as file:
                    w = csv.writer(file)
                    w.writerow([self.path])
                    file.close()

                self.close_window()

    def close_window(self):
        self.manager.current = "first"


class GrantsApp(App):
    def build(self):
        return kv

kv = Builder.load_file('main.kv')
# Builder.load_file('npo.kv')

if platform == 'darwin':
    Window.size = (700,700)

else:
    Window.size = (800,800)

if __name__ == '__main__':
    GrantsApp().run()