import serial
import time
from settings import UC_PORT_NAME, UC_BAUD_RATE

last_barcode = -2


class BarcodeScanner:
	def __init__(self):
		self.MasterModule = serial.Serial(UC_PORT_NAME, UC_BAUD_RATE)

	def serial_write(self, data_to_send):
		self.MasterModule.write(str(data_to_send).encode('utf-8'))
		self.MasterModule.flush()

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
				return int(readData[1:17])
			else:
				return 0
		else:
			return 0
	
	def get_latest_barcode(self):
		global last_barcode

		current_read = self.ask_data()
		if current_read != last_barcode and current_read != 0:
			last_barcode = current_read

		return last_barcode
