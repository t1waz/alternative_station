from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from settings import LabelNames
from scanner import barcode_scanner

import threading

from kivy.logger import Logger




Builder.load_file('graphic.kv')


class MessageWindow(Popup):
    def __init__(self, **kwargs):
        super(MessageWindow, self).__init__(**kwarg)


class InfoWindow(Popup):
    def __init__(self, **kwargs):
        super(InfoWindow, self).__init__(**kwargs)


class MainWindow(Screen, LabelNames):

    def __init__(self, **kwargs):
        LabelNames.__init__(self)
        self.aaa_label = ""
        super(MainWindow, self).__init__(**kwargs)
        threading.Thread(target = barcode_scanner.run_thread()).start()

    def start_thread(self):
        print(barcode_scanner.barcode_scan)



class ScanApp(App):
    def __init__(self, **kwargs):
        super(ScanApp, self).__init__(**kwargs)

    def build(self):
        return MainWindow()



if __name__ == '__main__':
    ScanApp().run()
