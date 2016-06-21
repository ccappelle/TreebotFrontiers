import afpo
import random
import sys
import os
import os.path
import datetime
import numpy as np
import matplotlib.pyplot as plt
import json
import time

gens = 200
steps = 200
pop = 40


MODULAR = 0
MODULAR_2 = 1
MODULAR_3 = 2

M_With_NM1 = 3
M_With_NM2 = 4

NONMODULAR_1 = 5
NONMODULAR_2=6

def Modular(p,envOrder,target=-1):
	evolve(MODULAR, 'modular_1', 'Modular_1',p,envOrder,target)

def NM1(p,envOrder,target=-1):
	evolve(NONMODULAR_1, 'nonmodular_1', 'Nonmodular_1',p,envOrder,target)

def NM2(p,envOrder,target=-1):
	evolve(NONMODULAR_2, 'nonmodular_2','Nonmodular_2',p,envOrder,target)

def M2(p,envOrder,target=-1):
	evolve(MODULAR_2, 'modular_2','Modular_2',p,envOrder,target)

def M3(p,envOrder,target=-1):
	evolve(MODULAR_3, 'modular_3','Modular_3',p,envOrder,target)

def MNM1(p,envOrder,target=-1):
	evolve(M_With_NM1,'mod-nm1','Mod-NM1',p,envOrder,target)

def MNM2(p,envOrder,target=-1):
	evolve(M_With_NM2, 'mnm_2','Mod-NM2',p,envOrder,target)

def evolve(robotType, typeString, folderString,p,envOrder,target):
	now = datetime.datetime.now()

	random.seed()	
	fileDate = now.strftime("%Y-%m-%d_%H_%M_%S")



	fileName = 'Results/'+folderString+'/'+fileDate + '-plot-'+typeString+'.txt'
	pickleFileName = 'Results/'+folderString+'/'+fileDate + '-pickled-robot-'+typeString+'.p'

		
	evolver = afpo.Create(range(9),robotType, p,gens,steps,pop)
	gensToTarget = np.zeros((len(envOrder)))
	#for i in range(1,len(envOrder)+1):
	#	print '------------------------------------------------- ' + str(i)
	#	gensToTarget[i-1]=afpo.Evolve(evolver,envOrder[:i],target)

	gensToTarget[0] = afpo.Evolve(evolver,envOrder,target)
	afpo.TestAllEnvs(evolver, range(9))


	print gensToTarget, np.sum(gensToTarget), evolver['population'][0]['envError']
	resultsFilePath = 'Results/'+folderString+'/results.json'
	with open('Results/'+folderString+'/last.data','w') as f:
	 	f.write(fileDate)

	if os.path.isfile(resultsFilePath):
	 	with open(resultsFilePath,'r') as f:
			results = json.load(f)
	else:
		results ={}


	results[fileDate] = {}
	results[fileDate]['p'] = p
	results[fileDate]['numGens'] = gens
	results[fileDate]['numSteps'] = steps
	results[fileDate]['popSize'] = pop
	#with open('fitnessFile.txt','r') as f:
	#	fitnessList = []
	#	for line in f:
	#		fitnessList.append(line.split()[0])
	#with open('envErrorFile.txt','r') as f:
	#	envErrorList = []
	#	for line in f:
	#		envErrorList.append(line.split()[0])

	results[fileDate]['fitness'] = evolver['fitnessList']
	results[fileDate]['envError'] = evolver['population'][0]['envError']
	results[fileDate]['style'] = 'target'
	#results[fileDate]['style'] = 'fixed'
	results[fileDate]['gensToTargetTotal'] = np.sum(gensToTarget)
	results[fileDate]['gensToTargetArray'] = list(gensToTarget)
	results[fileDate]['targetError'] = target
	afpo.SaveBest(evolver)
	results[fileDate]['envOrder'] = envOrder
	results[fileDate]['bestTree'] = evolver['population'][0]['tree']

	with open(resultsFilePath,'w') as f:
		json.dump(results,f)

O1 = [0,1,2,3]
O2 = [0,3,1,2]
p_nm1 = 1.0/28.0
p_nm2 = 1.0/22.0
p_m1 = 1.0/50.0
p_m2 = 1.0/12.0
p_m3 = 1.0/24.0
p_mnm1 = 1.0/8.0
p_mnm2 = 1.0/20.0

#M3(p_m3,O2,target = 0.1)
#Modular(.25, [0,1,2,3],target=0.0001)
#NM1(p_nm1,[0,1,2,3],target = 0.5)
#NM2(p_nm2,[0,1,2,3],target = .1)
#MNM2(.05,[0,3,1,2])
#MandNM(.1,[0,3], 0.0)
for i in range(50):
	NM1(p_nm1, [0,1,3], target = .05)
	print i
	Modular(p_m1, [0,1,3])
#for i in range(50):
# 	print i
# 	NM2(p_nm2,O1,target=0.1)
# 	NM2(p_nm2,O2,target=0.1)

# 	MNM2(p_mnm2,O1,target=0.1)
# 	MNM2(p_mnm2,O2,target=0.1)
 	#Modular(p_m1,O1,target = 0.1)
 	#Modular(p_m1,O2,target = 0.1)

 	#M2(p_m2, O1, target = .1)
 	#M2(p_m2, O2, target = .1)

 	#M3(p_m3, O1, target = .1)
 	#M3(p_m3, O2, target = .1)
 	
 	#MNM1(p_mnm1,O1,target = 0.1)
 	#MNM1(p_mnm1,O2,target = 0.1)

 	#NM1(p_nm1, O1, target = 0.1)
 	#NM1(p_nm1, O2, target = 0.1)


# 	MandNM(.1,[0,1,2],)
# 	print i
#   	M3(.05, [0,3,1,2],.1)

#  # 	print i, ' of 10   3 of 4'
#   	M3(.05, [0,1,2,3],.085)

# 	print i
#   	M3(.05, [0,3,1,2],.085)




