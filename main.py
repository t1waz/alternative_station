from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from settings import LabelNames
from scanner import BarcodeScanner
import threading


Builder.load_file('graphic.kv')

current_barcode = -5
last_barcode = -5

worker = ""



class MessageWindow(Popup):
    def __init__(self, **kwargs):
        super(MessageWindow, self).__init__(**kwarg)



class ScannerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.barcode_scanner = BarcodeScanner()

    def run(self):
        global current_barcode_scan

        while True:
            current_barcode = BarcodeScanner().get_latest_barcode()

class MainWindow(Screen, LabelNames):

    def __init__(self, **kwargs):
        LabelNames.__init__(self)
        super(MainWindow, self).__init__(**kwargs)
        ScannerThread().start()
        self.current_code_label = self.ids['last_code']

    def current_code_label_setter(self, value):
        self.current_code_label.text =  str(value)
        print(self.current_code_label.text)

    def current_code_label_getter(self):
        return self.current_code_label.text

    xxx = property(current_code_label_getter, current_code_label_setter)


class ScanApp(App):
    def __init__(self, **kwargs):
        global current_barcode_scan
        super(ScanApp, self).__init__(**kwargs)

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    ScanApp().run()
