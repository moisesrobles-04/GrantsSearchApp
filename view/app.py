from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
import os.path

import csv

from view.npo_view import *


# class result():
#     with open("test.csv", "w") as file:
#         write = csv.writer(file)


class WindowManager(ScreenManager):
    pass


# Class to choose path to save information
class NpoFileWindow(Screen):
    reenter = False

    def __init__(self, **kw):
        super().__init__(**kw)
        self.clock_var = ""

    def on_pre_enter(self, *args):
        if not self.reenter:
            grants_exist = os.path.isfile("./data/grants.csv")
            exist = os.path.isfile("./data/path.csv")
            if not grants_exist:
                self.action = "grant"
            else:
                self.clock_var = Clock.schedule_interval(self.close_window, 0.1)

    def selected(self, filename):
        try:
            self.path = filename[0]
        except:
            pass

        finally:
            if self.path != "":
                if self.action == "grants":
                    path_name = "./data/path.csv"

                else:
                    path_name = "./data/grants.csv"

                with open(path_name, "w") as file:
                    w = csv.writer(file)
                    w.writerow([self.path])
                    file.close()

                self.action = ""
                self.close_window()

    def close_window(self, *args):
        if self.reenter:
            if type(self.clock_var) != str:
                self.clock_var.cancel()
        self.manager.current = "first"
        self.reenter = True


class GrantsApp(App):
    def build(self):
        return kv


kv = Builder.load_file('main.kv')

if platform == 'darwin':
    Window.size = (700, 700)

else:
    Window.size = (800, 800)

if __name__ == '__main__':
    GrantsApp().run()
