
from smbus2 import SMBus 
import time
import socket 
ADDR1 = 8
ADDR2 = 9 
bus = SMBus(1) 
time.sleep(1) #letting bus settle.
#bus.write_byte_data(addr, 0xA5, 0x5A) 
#bus.write_byte(addr,0x0)
#counter = 10  
#while True: 
#	time.sleep(1)
#	print(counter) 
#	bus.write_byte(addr, counter)
#	counter += 1 
#	counter %= 255
#	
#bus.close() 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host_port = 5005 

sock.bind(("", host_port))

moving_forward = False
moving_backward = False
turning_left = False
turning_right = False

def main():
	print("Starting: \n")
	run = True
	robot = Robot(); 
	
	while(run):
		data, addr = sock.recvfrom(1024)
		# print(data, " " , addr)
		decode(data,robot)	 

class Robot: 
	def __init__(self):
		self.movement_vector = [0 for _ in range(4)] #x axis, y axis 
		print("hello world")
	def move_forward(self): 
		self.movement_vector[3] = 1
		print("Move Foward")
		bus.write_byte(ADDR1, 1)
	#	bus.write_byte(ADDR2, 3)

	def stop_forward(self): 
		self.movement_vector[3] = 0
		print("Stop Foward")
		bus.write_byte(ADDR1, 2)
	#	bus.write_byte(ADDR2, 4) 

	def move_backward(self):
		self.movement_vector[2] = 1
		print("Move Backward")

	def stop_backward(self):
		self.movement_vector[2] = 0
		print("Stop Backward")

	def turn_left(self): 
		self.movement_vector[0] = 1
		print("Turn Left")
	def stop_left(self): 
		self.movement_vector[0] = 0
		print("Stop Left") 

	def turn_right(self): 
		self.movement_vector[1] = 1
		print("Turn Right")

	def stop_right(self): 
		self.movement_vector[1] = 0
		print("Stop Right") 
		
def decode(data,robot): 	
	int_data = int.from_bytes(data, "big")
	# A or Left
	if int_data%2 == 1:
		robot.turn_left()
	elif robot.movement_vector[0] == 1:
		robot.stop_left()

	int_data /= 2
	# D or Right
	if int_data%2 == 1:
		robot.turn_right()
	elif robot.movement_vector[1] == 1:
		robot.stop_right()
	int_data /=2 
	# S or Down
	if int_data%2 == 1:
		robot.move_backward()
	elif robot.movement_vector[2] == 1:
		robot.stop_backward()
	int_data /= 2	
	# W or Up
	if int_data%2 == 1:
		robot.move_forward()
	elif robot.movement_vector[3] == 1:
		robot.stop_forward()	
	




def move_backward(bus): 
	print("Move Backward") 

def stop_backward(bus): 
	print("Stop Backward")
main()
