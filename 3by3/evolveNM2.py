import afpo
import random
import sys
import os
import os.path
import datetime
import numpy as np
import matplotlib.pyplot as plt
import json


p = .33
gens = 100
steps = 300
pop = 50

MODULAR = 0
NONMODULAR_1=1
NONMODULAR_2=2

now = datetime.datetime.now()

robotType = NONMODULAR_2

fileDate = now.strftime("%Y-%m-%d_%H_%M")

typeString = 'nonmodular_2'
folderString = 'Nonmodular_2'

fileName = 'Results/'+folderString+'/'+fileDate + '-plot-'+typeString+'.txt'
pickleFileName = 'Results/'+folderString+'/'+fileDate + '-pickled-robot-'+typeString+'.p'
random.seed(0)	
open('fitnessFile.txt','w').close()

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



evolver = afpo.Create([0,1,2,3],robotType, p,gens,steps,pop)

afpo.Evolve(evolver,[1])
print '------------------------------------------------- 1'
afpo.Evolve(evolver,[1,2])
print '------------------------------------------------- 2'
afpo.Evolve(evolver,[0,1,2])
print '------------------------------------------------- 3'
afpo.Evolve(evolver,[3,1,2,0])


with open('fitnessFile.txt','r') as f:
	fitnessList = []
	for line in f:
		fitnessList.append(line.split()[0])

results[fileDate]['fitness'] = fitnessList

afpo.SaveBest(evolver)
afpo.PickleBest(evolver,pickleFileName)

results[fileDate]['bestTree'] = evolver['population'][0]['tree']

os.remove('fitnessFile.txt')

with open(resultsFilePath,'w') as f:
	json.dump(results,f)
