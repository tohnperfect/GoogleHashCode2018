import sys
from operator import itemgetter
import random
from hyperopt import hp, fmin, tpe, STATUS_OK

def distance(a,b):
	return abs(a[0]-b[0])+abs(a[1]-b[1])
def output(cars):
	with open('advanced_besthyperopt_int_{}.txt'.format(infile),'w') as write_file:
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
		else:
			inf_list=map(int,line.replace('\n','').split())
			inf_list.append(line_num-1)
			rides.append(inf_list)

def obj_func(A,B,C):
	sorted_rides = sorted(rides, key=itemgetter(4))
	cars = []
	cars_info = []
	cars_list = []
	finalscore = 0
	for car in range(info['ve']):
		cars.append([])
		cars_info.append({'car':car,'pos':(0,0),'avail':0})
	for this_step in range(info['steps']):
		for car in cars_info:
			if car['avail'] <= this_step:
				remove_index = None
				best_ride = -1
				best_step = float('inf')
				best_pos = (-1,-1)
				max_score = float('-inf')
				best_real_now = float('-inf')
				for ride_index,ride in enumerate(sorted_rides):
					pre_score = distance((ride[2],ride[3]),(ride[0],ride[1]))
					starting_step = max(ride[4],this_step+distance(car['pos'],(ride[0],ride[1])))
					expected_step =  starting_step + pre_score
					expected_score = (A*pre_score) - ((B*ride[5]) + (C*starting_step))
					real_score = pre_score + (info['bo'] if starting_step == ride[4] else 0)
					if expected_step < ride[5] and ride[5] > this_step:
						if expected_score > max_score:
							best_ride = ride[-1]
							best_step = expected_step
							best_pos = (ride[2],ride[3])
							remove_index = ride_index
							max_score = expected_score
							best_real_now = real_score
						elif expected_score == max_score and best_real_now < real_score:
							best_ride = ride[-1]
							best_step = expected_step
							best_pos = (ride[2],ride[3])
							remove_index = ride_index
							best_real_now = real_score
				if remove_index is not None:
					del sorted_rides[remove_index]
					cars[car['car']].append(best_ride)
					car['avail'] = best_step
					car['pos'] = best_pos
					finalscore += best_real_now

	return finalscore,cars

max_so_far = 0
space = {'A':hp.quniform('A', 0, 100,1),'B':hp.quniform('B', 0, 100,1),'C':hp.quniform('C', 0, 100,1)}
def objective(space):
	global max_so_far
	#print space
	score,ans = obj_func(**space)
	print space,score
	if score > max_so_far:
		output(ans)
		max_so_far = score
	return {'loss': -1*score, 'status':STATUS_OK}

best = fmin(objective, space, algo=tpe.suggest, max_evals=200)

print best, max_so_far


