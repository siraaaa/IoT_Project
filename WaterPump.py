﻿##made 김정규
''' 2018. 01. 18  15:00  class WaterPump'''
##가습기제어 라즈베리에서 실행 SERVER RASPBERRY
import RPi.GPIO as GPIO
import bluetooth

class WaterPump :
	
	def __init__(self, state=False):
		
		WaterPump.gpioNum = 2 ##SDA1 pin  3번자리
		self.state = state
		self.server_sock = None
		self.client_sock = None
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(WaterPump.gpioNum, GPIO.OUT)
		GPIO.output(WaterPump.gpioNum, state)
		self.off()
		self.blueServerInit()
	
	def  blueServerInit(self):
		self.server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		port =3
		self.server_sock.bind(("",port))
		self.server_sock.listen(1)
		print("가습기 블루투스 접속 대기 ...")
		self.client_sock,address = self.server_sock.accept()
		print ("Accepted connection from ",address)
		print("클라이언트 접속 완료")
	
	def recvCommandAction(self):
		data =  WaterPump.binToUtf8(self.client_sock.recv(1024))
		if data == "ON":
			self.on()
		elif data == "OFF":
			self.off()
			
		elif data == "EXIT":
			self.blueConnectExit()
			return False
			
		return True
		
		
	def __del__(self):
		self.blueConnectExit()
	
	def setState(self, state):
		self.state = state
		GPIO.output(WaterPump.gpioNum, state)
	
	def on(self):
		print("가습기 ON")
		self.state = True
		GPIO.output(WaterPump.gpioNum, True)
		
	def off(self):
		print("가습기 OFF")
		self.state = False
		GPIO.output(WaterPump.gpioNum, False)
		
	def blueConnectExit(self):
		print("가습기 제어 종료")
		self.off()
		self.server_sock.close()
		self.client_sock.close()
		
	def isState(self):
		return self.state
		
	## 바이너리 to utf8	
	def binToUtf8(data):
		# 바이너리 데이터를 utf-16으로 디코딩한다
		# 수직 탭을 삭제한다
		return data.decode("utf-8").replace(u"\u000B", u"")
		
import time	
##테스트코드
if __name__ == "__main__" :
	wp = WaterPump()
	while wp.recvCommandAction():
		pass
		
		
		
	'''	
	wp = WaterPump()
	wp.on()
	print(wp.isState())
	time.sleep(3)
	wp.off()
	print(wp.isState())
	time.sleep(3)
	'''
