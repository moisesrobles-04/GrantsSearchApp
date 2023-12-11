from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
import os.path

from view.npo_view import *


class WindowManager(ScreenManager):
    pass


# Class to choose path to save information
class NpoFileWindow(Screen):
    reenter = False
    path_info = False

    def __init__(self, **kw):
        super().__init__(**kw)
        self.clock_var = ""

    def on_pre_enter(self, *args):
        # If it is first time entering app check if database file path exist
        if not self.reenter:
            grants_exist = os.path.isfile("./database_loc.csv")
            if not grants_exist:
                self.action = ""

            else:
                self.clock_var = Clock.schedule_interval(self.close_window, 0.1)
        # Update label
        if self.path_info:
            self.getpath()

    def selected(self, filename):
        try:
            self.path = filename[0]

        except:
            pass

        finally:
            if self.path != "":
                if self.action != "grants":
                    path_name = "./database_loc.csv"

                else:
                    path_name = "./download_path.csv"

                with open(path_name, "w") as file:
                    w = csv.writer(file)
                    w.writerow([self.path])
                    file.close()

                # When opened for the first time download path will be the same as db path
                path_name = "./download_path.csv"
                exist = os.path.isfile(path_name)
                if not exist:
                    temp_path = self.path.split("grants.db")
                    temporary_loc = temp_path[0]
                    with open(path_name, "w") as f:
                        w = csv.writer(f)
                        w.writerow([temporary_loc])
                        f.close()

                self.action = ""
                self.close_window()

    # Name path's label
    def getpath(self):
        if self.action != "grants":
            grants_exist = os.path.isfile("./database_loc.csv")
            if not grants_exist:
                self.ids.path_id.text = "Database path has not been selected"
            else:
                with open("./database_loc.csv", 'r') as f:
                    read = csv.reader(f)
                    path = read.__next__()
                    f.close()
                    self.ids.path_id.text = f'The database path is {path[0]}'
        else:
            download_exist = os.path.isfile("./download_path.csv")
            if not download_exist:
                self.ids.path_id.text = 'No download path selected'
            else:
                with open("./download_path.csv", 'r') as f:
                    read = csv.reader(f)
                    path = read.__next__()
                    f.close()
                    self.ids.path_id.text = f'The download path is {path[0]}'

    def close_window(self, *args):
        if self.reenter:
            if type(self.clock_var) != str:
                self.clock_var.cancel()
        if os.path.isfile("./database_loc.csv"):
            self.manager.current = "first"
            self.action = ""
            self.reenter = True
            self.path_info = True


class GrantsApp(App):
    def build(self):
        return kv


kv = Builder.load_file('view/main.kv')

if platform == 'darwin':
    Window.size = (700, 700)
else:
    Window.size = (800, 800)

if __name__ == '__main__':
    GrantsApp().run()
