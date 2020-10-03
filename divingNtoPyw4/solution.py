import tempfile
import os.path
import uuid

class File():
    def __init__(self, path_to_file):
        self.path = path_to_file
        self.descriptor = open(path_to_file, "a+")
    
    def read(self):
        self.descriptor.seek(0)
        return(self.descriptor.read())
    
    def write(self, string_to_write):
        self.descriptor.close()
        self.descriptor = open(self.path, "w")
        result = self.descriptor.write(string_to_write)
        self.descriptor = open(self.path, "r")
        return(result)
    
    def __add__(self, obj):
        new_file = File(os.path.join(tempfile.gettempdir(), str(uuid.uuid4())))
        new_file.write(self.read()+obj.read())
        return new_file

    def __str__(self):
        return self.path

    def __iter__(self):
        self.descriptor.seek(0)
        return self

    def __next__(self):
        result = self.descriptor.readline()
        if result == "":
            raise StopIteration
        else:
            return(result)

class Value:
	def __init__(self):
		self.amount = 0
	def __get__(self, obj, obj_type):
		return self.amount
	def __set__(self, obj, value):
		self.amount = value * (1 - obj.commission)
	
class Account:
	amount = Value()
	def __init__(self, commission):
		
		self.commission = commission