'''	Name: 	Kuteesa Kiyaga
	Date: June 30, 2019
	Function:	Concurrently append values to an array
'''

# import modules
from multiprocessing import Process, Manager

# function used to concurrently append a value to an array
def append_to_list(manager_list, i):  
	# add a value to 
	manager_list.append(i)

if __name__ == "__main__":
	# can be shared between processes
	manager_list = Manager().list()  
	
	# array containing processes
	processes = []
	
	# loop
	for i in range(5):
		# passing the list
		p = Process(target=append_to_list, args=(manager_list,i))
		p.start()
		# append process to process array
		processes.append(p)
		
	for p in processes:
		p.join()
	
	# print list
	print(manager_list)