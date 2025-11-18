"""
Bidirectional communications between the host and client
communications between my Jetson and Odroid
"""

import socket
import threading
import time
import serial
import subprocess
import sys
import os

class Host:
	def __init__(self, arduino_port = '/dev/ttyACM0', baud_rate = 9600 ):
		self.running = True
		self.plant_count = 3
		
		# Arduino serial connection init
		self.arduino_port = arduino_port
		self.baud_rate = baud_rate
		self.arduino = None
		self.setup_arduino()
		
	def show_commands(self):
		"""
		Function to display all the commands available
		"""
		print("Please use the following commands for further instructions:")
		print("	1. Start: To run the full program.")
		print("	2. Capture: To capture from both cameras.")
		print("	3. Capture red: To capture from red camera.")
		print("	4. Capture green: To capture from green camera.")
		print("	5. Forward or f: To rotate arm Anti-Clockwise")
		print("	6. Reverse or r: To rotate arm Clockwise")
		print("	7. Stop or s: To stop arm rotation")
		print("	8. Viewer red: To turn on the red camera live feed")
		print("	9. Viewer green: To turn on the green camera live feed")
		
	def start(self):
		"""
		Function to run the full implementation
		- capture 0 and 180 degrees:
		- Rotate 90 degrees:
		- capture 90 and 270 degrees:
		- Rotate back 90 degrees:
		- Process data:
		"""
		# Capture 0 and 180 degrees
		self.capture(["0_degrees","180_degrees"], self.plant_count)
		
		# Rotate anti clockwise 90 degrees
		self.send_arduino_command('f')
		time.sleep(8)
		self.send_arduino_command('s')
		
		# Capture 90 and 270 degrees
		self.capture(["90_degrees","270_degrees"], self.plant_count)
		self.plant_count += 1
		
		# Rotate back to homebase
		self.send_arduino_command('r')
		time.sleep(8)
		self.send_arduino_command('s')
		
		print("Full Capture process completed Successfully!")
		
		# Processing code goes here onwards
		
	def capture(self, filenames, count):
		"""
		Function which calls camera_red and camera_green to capture 
		from both devices
		"""
		camera_red = self.capture_red(filenames[1], count)
		if camera_red:
			camera_green = self.capture_green(filenames[0], count)
			if camera_green:
				print("Both camera captures completed sucessfuly")
			else:
				print("Camera red was successful but camera green failed")
				print("Deleting camera red data")
		else:
			print("Camera capture failed! Please run command again")
			
					
	def capture_red(self, filename, count):
		"""
		Function to capture from just the red camera using camera_red.py
		"""
		# Runs the camera capture code as a subroutine
		print(f"Running camera capture camera_red.py...")
		result = subprocess.run([sys.executable, "camera_red.py", filename, str(count)], capture_output = True, text = True)
		
		if result.returncode == 0:
			print("Camera capture completed successfully")
			print("Capture output:", result.stdout)
			return True
		else:
			print("Camera capture failed")
			print("Error:", result.stderr)
			return False
		
	def capture_green(self, filename, count):
		"""
		Function to capture from just the green camera using camera_green.py
		"""
		# Runs the camera capture code as a subroutine
		print(f"Running camera capture camera_green.py...")
		result = subprocess.run([sys.executable, "camera_green.py", filename, str(count)], capture_output = True, text = True)
		
		if result.returncode == 0:
			print("Camera capture completed successfully")
			print("Capture output:", result.stdout)
			return True
		else:
			print("Camera capture failed")
			print("Error:", result.stderr)
			return False
		
	def viewer_red(self):
		"""
		Function to open the red camera live feed
		"""
		print("Running red camera live feed...")
		result = subprocess.run([sys.executable, "viewer_red.py"], capture_output = True, text = True)
		
	def viewer_green(self):
		"""
		Function to open the green camera live feed
		"""
		print("Running green camera live feed...")
		result = subprocess.run([sys.executable, "viewer_green.py"], capture_output = True, text = True)
		
	def setup_arduino(self):
		# Setup arduino serial comms
		if self.connect_arduino():
			print(f"Arduino connected on {self.arduino_port}")
		else:
			print(f"Failed to connect to Arduino on {self.arduino_port}")
			print(f"Serial commands will be disabled")
			
	def connect_arduino(self):
		# Connect to arduino via serial comms
		success = True
		error_occurred = False
		
		# Set timout for connection attempt
		connection_timeout = 5
		start_time = time.time()
		
		# Check if port is available and exists
		if not os.path.exists(self.arduino_port):
			error_occurred = True
			success = False
			print(f"Arduino port {self.arduino_port} does not exist")
		else:
			# attempt serial connection
			self.arduino = serial.Serial()
			self.arduino.port = self.arduino_port
			self.arduino.baudrate = self.baud_rate
			self.arduino.timeout = 1
			
			# Check if we can open connection
			if hasattr(self.arduino, 'open'):
				self.arduino.open()
				if self.arduino.is_open:
					time.sleep(2)
					success = True
				else:
					error_occurred = True
					success = False
			else:
				error_occurred = True
				success = False
				
		if error_occurred:
			self.arduino = None
			
		return success
		
	def send_arduino_command(self, command):
		# Send the command to the board
		if self.arduino and hasattr(self.arduino, 'is_open') and self.arduino.is_open:
			send_success = True
			error_occurred = False
			
			# Check if still connected
			if hasattr(self.arduino, 'write'):
				# Attempt to write
				bytes_written = 0
				command_bytes = command.encode()
				
				# check if write operation is available
				if hasattr(self.arduino, 'write'):
					write_result = self.write_to_arduino(command_bytes)
					if write_result:
						time.sleep(0.1)
						send_success = True
					else:
						error_occurred = True
						send_success = False
				else:
					error_occurred = True
					send_success = False
			else:
				error_occurred = True
				send_success = False
				
			if error_occurred:
				print("Failed to send command to Arduino")
				return False
			else:
				print(f"Sent '{command}' to Arduino")
				return True
		else:
			print("Arduino not connected")
			return False
			
	def write_to_arduino(self, data):
		# Write data to arduino
		success = True
		
		if self.arduino and hasattr(self.arduino, 'write') and self.arduino.is_open:
			# Perform write operation
			result = self.arduino.write(data)
			if result > 0:
				success = True
			else:
				success = False
		else:
			success = False
			
		return success
		
	def control(self):
		print("Control has began, awaiting further instruction:")
		self.show_commands()
		# Handle the user input which will be sent
		while self.running:
			message = input("Enter command (or 'quit'): \n")
			if message.lower() == 'quit':
				self.running = False
				break
			elif message.lower() == 'start':
				self.start()
			elif message.lower() == 'capture':
				self.capture()
			elif message.lower() == 'capture red':
				self.capture_red()
			elif message.lower() == 'capture green':
				self.capture_green()
			elif message.lower() == 'forward' or message.lower() == 'f':
				self.send_arduino_command('f')
			elif message.lower() == 'reverse' or message.lower() == 'r':
				self.send_arduino_command('r')
			elif message.lower() == 'stop' or message.lower() == 's':
				self.send_arduino_command('s')
			elif message.lower() == 'viewer_red':
				self.viewer_red()
			elif message.lower() == 'viewer_green':
				self.viewer_green()
			elif message.lower() == 'commands':
				self.show_commands()
			else:
				print("Invalid command, type 'commands' for help: ")
			
if __name__ == "__main__":
	host = Host()
	host.control()
