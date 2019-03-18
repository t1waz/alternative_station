import os
os.environ['KIVY_GL_BACKEND'] = 'gl' # DUE TO RUNNING ON RASPI
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from scanner import BarcodeScanner
from service import AppService
import threading
from kivy.properties import (
    StringProperty, 
    BooleanProperty
)


Builder.load_file('graphic.kv')


class ScannerThread(threading.Thread):
    def __init__(self, my_app):
        threading.Thread.__init__(self)
        self.barcode_scanner = BarcodeScanner()
        self.app_service = AppService(my_app)

    def run(self):
        while True:
            current_barcode_scan = self.barcode_scanner.handle_scanner()
            if current_barcode_scan != 0:
                self.app_service.main_handling(current_barcode_scan)


class MessageWindow(Popup):
    def __init__(self, **kwargs):
        super(MessageWindow, self).__init__(**kwargs)


class MainWindow(Screen):
    main_app_name_label = StringProperty('')
    last_barcode_label = StringProperty('')
    last_time_label = StringProperty('-')
    status_label = StringProperty('connected')
    worker_label = StringProperty('no worker')
    comment_box = StringProperty()
    second_category_flag = BooleanProperty(False)
    for index in range(1, 11):
        variable_name = 'barcode_label_{}'.format(index)
        exec(variable_name + '  = StringProperty()')

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def exit_app(self):
        App.get_running_app().stop()

    def add_comment(self):
        self.comment_box = self.ids['comment'].text

    def add_second_category(self):
        if self.worker_label is 'no worker':
            self.status_label = 'SCAN WORKER CARD'
            return False

        self.second_category_flag = not self.second_category_flag
        if self.second_category_flag:
            self.status_label = "2TH MODE"
        else:
            self.status_label = "connected"


class ScanApp(App):
    def __init__(self, **kwargs):
        super(ScanApp, self).__init__(**kwargs)

    def build(self):
        main_window = MainWindow()
        ScannerThread(main_window).start()
        return main_window


if __name__ == '__main__':
    ScanApp().run()
