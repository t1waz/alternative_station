from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from settings import LabelNames
from scanner import BarcodeScanner
import threading
from kivy.properties import StringProperty


Builder.load_file('graphic.kv')

current_barcode_scan = -5
last_barcode_scan = -5

worker = ""



class MessageWindow(Popup):
    def __init__(self, **kwargs):
        super(MessageWindow, self).__init__(**kwarg)


class MainWindow(Screen):
    main_app_name_label = StringProperty()
    barcode_label = [StringProperty(' ')] * 10
    last_barcode_label = StringProperty('dupa')
    last_time_label = StringProperty()
    status_label = StringProperty('connected')
    worker_label = StringProperty()

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)


class ScannerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.barcode_scanner = BarcodeScanner()

    def run(self):
        global current_barcode_scan

        while True:
            current_barcode_scan = self.barcode_scanner.get_latest_barcode()
            app = App.get_running_app()
            if hasattr(app.root,'last_barcode_label'):
                app.root.last_barcode_label = str(current_barcode_scan)

class ScanApp(App):
    def __init__(self, **kwargs):
        ScannerThread().start()
        super(ScanApp, self).__init__(**kwargs)

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    ScanApp().run()
