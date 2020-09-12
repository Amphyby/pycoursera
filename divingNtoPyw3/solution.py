import csv
import os

class FileReader:
	def __init__(self, filename):
		self._filename = filename
	def read(self):
		try:
			self._desc = open(self._filename, "r")
			result = self._desc.read()
			return (result)
		except FileNotFoundError:
			return ("")

# if __name__ == '__main__':
# 	reader = FileReader('sometrashhere')
# 	print(reader.read())
class CarBase:
	def __init__(self, brand, photo_file_name, carrying):
		self.brand = brand
		if brand == "" :
			raise ValueError
		self.photo_file_name = photo_file_name
		self.carrying = float(carrying)
	
	def get_photo_file_ext(self):
		return (os.path.splitext(self.photo_file_name)[1])

class Car(CarBase):
	def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
		super().__init__(brand, photo_file_name, carrying)
		self.passenger_seats_count = int(passenger_seats_count)
		self.car_type = "car"

class Truck(CarBase):
	def __init__(self, brand, photo_file_name, carrying, body_whl):
		super().__init__(brand, photo_file_name, carrying)
		try:
			whl = body_whl.split('x')
			if len(whl) > 3:
				raise ValueError
			(self.body_length, self.body_width, self.body_height) = (float(whl[0]), float(whl[1]), float(whl[2]))
		except ValueError:
			self.body_length = 0.0
			self.body_width = 0.0
			self.body_height = 0.0
		self.car_type = "truck"
	
	def get_body_volume(self):
		return (self.body_length * self.body_width * self.body_height)
	

class SpecMachine(CarBase):
	def __init__(self, brand, photo_file_name, carrying, extra):
		super().__init__(brand, photo_file_name, carrying)
		self.extra = extra
		if extra == "" :
			raise ValueError
		self.car_type = "spec_machine"


def get_car_list(csv_filename):
	car_list = []
	with open(csv_filename) as csv_fd:
		reader = csv.reader(csv_fd, delimiter=';')
		next(reader)
		for row in reader:
			element = None
			if len(row) < 4 or os.path.splitext(row[3])[1] != ".jpg" and os.path.splitext(row[3])[1] != ".jpeg" and os.path.splitext(row[3])[1] != ".gif" and os.path.splitext(row[3])[1] != ".png":
				continue
			try:
				if row[0] == "car":
					element = Car(row[1], row[3], row[5], row[2])
				elif row[0] == "truck":
					if len(row) < 6:
						continue
					element = Truck(row[1], row[3], row[5], row[4])
				elif row[0] == "spec_machine":
					if len(row) < 7:
						continue
					element = SpecMachine(row[1], row[3], row[5], row[6])
				else:
					continue
			except ValueError:
				continue
			car_list.append(element)
	return car_list

if __name__ == '__main__' :
	# car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
	# print(car.car_type, car.brand, car.photo_file_name, car.carrying, car.passenger_seats_count, sep='\n')
	# truck = Truck('Nissan', 'nissan.jpeg', '1.5', '3.92x2.09x1.87')
	# print(truck.car_type, truck.brand, truck.photo_file_name, truck.body_length, truck.body_width, truck.body_height, sep='\n')
	# spec_machine = SpecMachine('Komatsu-D355', 'd355.jpg', '93', 'pipelayer specs')
	# print(spec_machine.car_type, spec_machine.brand, spec_machine.carrying, spec_machine.photo_file_name, spec_machine.extra, spec_machine.get_photo_file_ext(), sep='\n')
	cars = get_car_list('test_cars.csv')
	print(len(cars))
	