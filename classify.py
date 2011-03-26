import numpy as np
import mlpy
import random

def classify(observList):
	toxtr=list()
	toytr = list()
	#10 samples for chill party
	for i in range(10):
		tempxtr=list()
		tempxtr=[75+random.triangular(-2, 3),17+random.triangular(-2,3), 580+random.triangular(-10,20)]
		toxtr.append(tempxtr)
		toytr.append(1)
	#10 samples for hopping party
	for i in range(10):
		tempxtr=list()
		tempxtr=[80+random.triangular(-2, 2), 25+random.triangular(-5,5), 600+random.triangular(-50,50)]
		toxtr.append(tempxtr)
		toytr.append(2)
	
	#10 samples for insane party
	for i in range(10):
		tempxtr=list()
		tempxtr=[85+random.triangular(-3, 5), 35+random.triangular(-7,7), 700+random.triangular(-10,60)]
		toxtr.append(tempxtr)
		toytr.append(3)
	xtr = np.array(toxtr)
	ytr = np.array(toytr)
	knn = mlpy.Knn(k=3)
	knn.compute(xtr, ytr)
	xts = np.array(observList)
	return knn.predict(xts)

classify([76, 27 , 665])
