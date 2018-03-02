import numpy
import sys
from operator import itemgetter

def distance(a,b):
	#a,b should be a tuple with (x,y) as coordinate
	return abs(a[0]-b[0])+abs(a[1]-b[1])
	
def output(cars):
	with open('advanced_bestassignment_{}.txt'.format(infile),'w') as write_file:
		for car in cars:

			write_file.write('{} '.format(len(car)))
			for r in car:
				write_file.write('{} '.format(r))
			
			write_file.write('\n')

infile = sys.argv[1]

info = {}
rides = []

with open(infile,'r') as input_file:

	for line_num,line in enumerate(input_file):
		if line_num == 0:
			
			linesp = line.split()
			info['ro'] = int(linesp[0])
			info['co'] = int(linesp[1])
			info['ve'] = int(linesp[2])
			info['rides'] = int(linesp[3])
			info['bo'] = int(linesp[4])
			info['steps'] = int(linesp[5])

			town = numpy.zeros((info['ro'],info['co']))
		else:
			inf_list=map(int,line.replace('\n','').split())
			inf_list.append(inf_list[4]+distance((inf_list[0],inf_list[1]),(inf_list[2],inf_list[3])))
			inf_list.append(line_num-1)
			rides.append(inf_list)

sorted_rides = sorted(rides, key=itemgetter(4))

cars = []
cars_info = []
cars_list = []
for car in range(info['ve']):
	cars.append([])
	cars_info.append({'car':car,'pos':(0,0),'avail':0})

for this_step in range(info['steps']):
	if this_step%10000 == 0:
		print '{}/{}'.format(this_step,info['steps'])
	for car in cars_info:
		if car['avail'] <= this_step:
			remove_index = None
			best_ride = -1
			best_step = float('inf')
			best_pos = (-1,-1)

			for ride_index,ride in enumerate(sorted_rides):
				expected_step =  max(ride[4],this_step+distance(car['pos'],(ride[0],ride[1]))) + distance((ride[2],ride[3]),(ride[0],ride[1]))
				
				if expected_step < ride[5] and ride[5] > this_step:
					if expected_step < best_step:
						best_ride = ride[-1]
						best_step = expected_step
						best_pos = (ride[2],ride[3])
						remove_index = ride_index

			if remove_index is not None:
				del sorted_rides[remove_index]
				cars[car['car']].append(best_ride)
				car['avail'] = best_step
				car['pos'] = best_pos


output(cars)
