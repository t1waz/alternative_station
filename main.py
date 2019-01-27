from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from scanner import BarcodeScanner
import threading
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from service import AppService


Builder.load_file('graphic.kv')


class ScannerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.barcode_scanner = BarcodeScanner()
        self.app_service = AppService()
        self.last_barcode_scan = 0

    def run(self):
        self.app_service.get_workers()
        while True:
            current_barcode_scan = self.barcode_scanner.ask_data()
            self.app_service.main_handling(current_barcode_scan)
                    

class MessageWindow(Popup):
    def __init__(self, **kwargs):
        super(MessageWindow, self).__init__(**kwarg)


class MainWindow(Screen):
    main_app_name_label = StringProperty('LAGGING ROOM')
    for index in range(1,11):
        variable_name = 'barcode_label_{}'.format(index)
        exec(variable_name + '  = StringProperty()')
    last_barcode_label = StringProperty('')
    last_time_label = StringProperty('-')
    status_label = StringProperty('connected')
    worker_label = StringProperty('-')
    comment_box = StringProperty()
    worker = ''
    second_category_flag = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def exit_app(self):
        App.get_running_app().stop()

    def add_comment(self):
        self.comment_box = self.ids['comment'].text

    def add_second_category(self):
        if self.worker_label == '-':
            self.status_label = 'SCAN WORKER CARD'
            return False
        if (self.second_category_flag == False):
            self.second_category_flag = True
            self.status_label = "2TH MODE"
        else:
            self.second_category_flag = False
            self.status_label = "connected"



class ScanApp(App):
    def __init__(self, **kwargs):
        ScannerThread().start()
        super(ScanApp, self).__init__(**kwargs)

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    ScanApp().run()
