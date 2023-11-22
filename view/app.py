import csv

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

from controller.npo_controller import npoController
from controller.categories_controller import categoryController

class MyGridLayout(Widget):

    name = ObjectProperty(None)

    def press(self):
        name= self.name.text

        # self.add_widget(Label(text=f'Hello {name} this is a test'))
        print(f'Hello {name} this is a test')
        self.name.text= ""


class GrantsApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    GrantsApp().run()