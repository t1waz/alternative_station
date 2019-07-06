import serial
import time


class BarcodeScanner:
    def __init__(self):
        self.port = False
        self.init_connection()

    def serial_clear(self):
        if (self.MasterModule.inWaiting() > 0):
            try:
                self.MasterModule.read(self.MasterModule.inWaiting())
                time.sleep(0.05)
            except:
                pass
            self.MasterModule.flush()

    def init_connection(self):
        _ports = ['/dev/ttyUSB{}'.format(number) for number in range(0, 20)] + \
                 ['/dev/ttyACM{}'.format(number) for number in range(0, 20)]

        for port in _ports:
            try:
                self.MasterModule = serial.Serial(port, 
                                                  115200,
                                                  dsrdtr=True,
                                                  rtscts=True)
                if self.MasterModule.isOpen():
                    self.MasterModule.close()
                self.MasterModule = serial.Serial(port, 
                                                  115200,
                                                  dsrdtr=True,
                                                  rtscts=True)
                self.port = True
                time.sleep(0.5)
                self.serial_clear()
                time.sleep(0.5)
                break
            except serial.SerialException:
                pass

    def __del__(self):
        if self.port:
            self.MasterModule.close()

    def serial_write(self, data_to_send):
        self.MasterModule.write(str(data_to_send).encode('utf-8'))
        self.MasterModule.flush()

    def serial_read(self):
        try:
            return self.MasterModule.read(self.MasterModule.inWaiting()).decode(
                encoding='UTF-8', errors='ignore').rstrip()
        except:
            return '0'

    def ask_data(self):
        self.serial_clear()
        self.serial_write('AC1E')
        time.sleep(0.05)
        readed_data = self.serial_read()
        if (readed_data[0:1] != '0'):
            sended_confirmation = 'AD{}E'.format(str(readed_data[8:17]))
            self.serial_clear()
            self.serial_write(sended_confirmation)
            time.sleep(0.05)
            readed_confirmation = self.serial_read()
            if (readed_confirmation[0:4] == 'AC2E'):
                try:
                    return int(readed_data[3:16])
                except ValueError:
                    pass
                try:
                    return int(readed_data[1:13])
                except ValueError:
                    return 0
            else:
                return 0
        else:
            return 0

    def handle_scanner(self):
        if self.port:
            return self.ask_data()
        else:
            time.sleep(0.15)
            return 0
