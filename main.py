from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder


Builder.load_file('graphic.kv')


class MessageWindow(Popup):
    def __init__(self, **kwargs):
        super(MessageWindow, self).__init__(**kwarg)


class InfoWindow(Popup):
    def __init__(self, **kwargs):
        super(InfoWindow, self).__init__(**kwargs)


class MainWindow(Screen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

class ScanApp(App):
    def __init__(self, **kwargs):
        super(ScanApp, self).__init__(**kwargs)

    def build(self):
        return MainWindow()


if __name__ == '__main__':
    ScanApp().run()