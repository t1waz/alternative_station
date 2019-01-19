import serial
import time
import threading
from settings import UC_PORT_NAME, UC_BAUD_RATE

class BarcodeScanner:
	def __init__(self):
		self.MasterModule = serial.Serial(UC_PORT_NAME, UC_BAUD_RATE)
		self.barcode_read = -2
		time.sleep(1)

	def serial_write(self, data_to_send):
		self.MasterModule.write(str(data_to_send).encode('utf-8'))
		self.MasterModule.flush()
		time.sleep(0.01)

	def serial_clear(self):
		if (self.MasterModule.inWaiting() > 0):
			try:
				self.MasterModule.read(self.MasterModule.inWaiting())
			except:
				pass
			self.MasterModule.flush()

	def serial_read(self):
		try:
			myData = self.MasterModule.read(self.MasterModule.inWaiting())
			myData = myData.decode(encoding='UTF-8', errors='ignore')
		except:
			myData = '0'
		return myData

	def ask_data(self):
		sendConfirmation = ""
		readConfirmation = ""
		self.serial_clear()
		self.serial_write('AC1E')
		readData = self.serial_read()
		if (readData[0:1] != '0'):
			sendConfirmation = 'AD' + str(readData[8:17]) + 'E'
			self.serial_clear()
			self.serial_write(sendConfirmation)
			readConfirmation = self.serial_read()
			if (readConfirmation[0:4] == 'AC2E'):
				return readData[1:17]
			else:
				return 0
		else:
			return 0

	def run_thread(self):
		while True:
			self.barcode_read = self.ask_data()


barcode_scanner = BarcodeScanner()