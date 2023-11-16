import csv

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class MyGridLayout(GridLayout):
    #Initialize infinite keywords
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)

        #Num of columns
        self.cols = 1

        #Create second gridlayout
        self.top_grid = GridLayout()
        self.top_grid.cols = 2


        #Add widgets
        self.top_grid.add_widget(Label(text = "Name: "))
        #Add Input Box
        self.name = TextInput(multiline =False)
        self.top_grid.add_widget(self.name)

        #Add top grid to grid
        self.add_widget(self.top_grid)


        #Create a submit Button
        self.submit = Button(text = "Submit", font_size = 32)
        self.submit.bind(on_press=self.press)
        self.add_widget(self.submit)

    def press(self, instance):
        test = []
        name = self.name.text
        with open("./data/Total grants.csv", "r", encoding= "utf8") as file:
            reader = csv.reader(file)
            debug = False
            for i in reader:
                test.append(i)
                if debug:
                    break
                debug = True
            # print(f'This grant data is: \n {test[1]}')
            file.close()

        self.add_widget(Label(text=f'This grant data is: \n {test[1]}'))

        #Clear box
        self.name.text = ""

class GrantsApp(App):
    def build(self):
        return MyGridLayout()


# class GrantsButton(Button):
#     def callback(self):



if __name__ == '__main__':
    GrantsApp().run()