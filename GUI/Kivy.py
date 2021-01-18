import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.properties import ObjectProperty

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.write()


class MyApp(App):
    def build(self):
        return GUI()


class GUI(Widget):
    url = ObjectProperty(None)


if __name__ == "__main__":
    import os

    if os.path.isfile(os.path.join(os.getcwd(), "my.kv")):
        os.system("del my.kv")
    os.system("copy my my.kv")
    app = MyApp()
    app.run()
