import csv

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from controller.npo_controller import npoController

class MyGridLayout(GridLayout):
    #Initialize infinite keywords
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)

        #Num of columns
        self.cols = 1

        #Create second gridlayout
        self.top_grid = GridLayout()
        self.top_grid.cols = 3


        #Add widgets
        self.top_grid.add_widget(Label(text = "Name: "))
        #Add Input Box
        self.name = TextInput(multiline =False)
        self.top_grid.add_widget(self.name)

        #Create a submit Button
        self.submit = Button(text = "Search specific NPO", font_size = 32)
        self.submit.bind(on_press=self.press_npos)
        self.top_grid.add_widget(self.submit)

        #Add top grid to grid
        self.add_widget(self.top_grid)


        #Create a submit Button
        self.submit = Button(text = "Search NPOs", font_size = 32)
        self.submit.bind(on_press=self.press_all_npos)
        self.add_widget(self.submit)


    def press_npos(self, instance):
        name = self.name.text
        dao = npoController().get_npo_by_name(name)
        self.label = Label(text=f'The NPO {dao.get("name")} exists', size_hint=(1.0, 1.0), halign="left", valign= "middle")
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)

        #Clear box
        self.name.text = ""

    #Search for all NPOs
    def press_all_npos(self, instance):
        handler = npoController().get_all_npos()
        for i in handler:
            self.label = Label(text=f'The NPO #{i.get("n_id")} is {i.get("name")}', size_hint=(1.0, 1.0), halign="left", valign= "middle")
            self.label.bind(size=self.label.setter('text_size'))
            self.add_widget(self.label)

class GrantsApp(App):
    def build(self):
        return MyGridLayout()


# class GrantsButton(Button):
#     def callback(self):



if __name__ == '__main__':
    GrantsApp().run()