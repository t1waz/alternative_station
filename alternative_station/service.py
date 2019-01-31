from kivy.app import App
from datetime import datetime
from api_service import ApiService
import json
import settings


class AppService:
    def __init__(self, my_app):
        self.api_service = ApiService()
        self.current_worker = ''
        self.workers = {}
        self.station_name = ''
        self.my_app = my_app
        self.get_workers()

    def get_workers(self):
        workers_raw_data = self.api_service.get_endpoint_data('workers')

        self.station_name = self.api_service.get_endpoint_data('stations/{}'.
            format(settings.STATION_NUMBER)).get('name','')

        self.my_app.main_app_name_label = '{} ROOM'.format(self.station_name)
        self.my_app.status_label = 'connected'

        self.workers = {worker['barcode']: worker['username'] for 
                        worker in workers_raw_data}

    def update_worker(self, _barcode):
        if _barcode in self.workers:
            if self.current_worker is '':
                self.current_worker = self.workers[_barcode]
                self.my_app.worker_label = self.current_worker
                self.my_app.status_label = 'welcome'
            else:
                self.current_worker = ''
                self.my_app.worker_label = 'no worker'
                self.my_app.status_label = '-'
            self.my_app.second_category_flag = False
            return True
        return False

    def update_barcode_list(self, _data):
        current_last_barcode_label = self.my_app.last_barcode_label
        self.my_app.last_barcode_label = str(_data)

        for index in range(10, 1, -1):
            up_label = getattr(self.my_app, 'barcode_label_{}'.format(index-1))
            setattr(self.my_app, 'barcode_label_{}'.format(index),up_label)

        if current_last_barcode_label != '':
            first_history_label = '{} {}'.format(datetime.now().strftime('%H:%M:%S'),
                                                 current_last_barcode_label)
        else:
            first_history_label = ''

        self.my_app.barcode_label_1 = first_history_label
        self.my_app.last_time_label = datetime.now().strftime('%H:%M:%S')

    def add_barcode(self, _barcode):
        data_to_send = {
            "barcode": _barcode,
            "worker": self.current_worker,
            "station": self.station_name,
        }

        comment = self.my_app.comment_box
        if comment:
            data_to_send['comment'] = comment

        is_sended, message = self.api_service.send_endpoint_data(_endpoint='add_scan',
                                                                 _data_dict=data_to_send)
        self.my_app.status_label = message
        self.my_app.comment_box = ''

    def add_second_category(self, _barcode):
        data_to_send = {
            "barcode": _barcode,
            "second_category": True
        }

        is_sended, message = self.api_service.send_endpoint_data(_endpoint='add_second_category',
                                                                 _data_dict=data_to_send)
        if is_sended:
            message = 'ADDED 2th'
        else:
            message = 'NOT ADDED 2th'
        self.my_app.status_label = message

    def main_handling(self, _barcode):
        if _barcode != 0:
            if not self.update_worker(_barcode):
                if not self.current_worker == "":
                    if self.my_app.second_category_flag is True:
                        self.add_second_category(_barcode)
                        self.my_app.second_category_flag = False
                    else:
                        self.add_barcode(_barcode)
                else:
                    self.my_app.status_label = 'SCAN WORKER CARD'
            self.update_barcode_list(_barcode)
