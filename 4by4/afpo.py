#Afpo is an EA which creates a Pareto front consisting of fitness and age. Dominated 
#solutions are those which have a younger and fitter counterparts. Dominated solutions
#are deleted and population is filled with mutations. Pop is aged by one and a new
#individual is introduced to the population age 0

import population 
import os
import environment

MODULAR = 0
NONMODULAR_1=1
NONMODULAR_2=2

def Age_Survivors(afpo):
	#Increases age of survivors by 1
	population.Age_Survivors(afpo['population'])

def Count_Non_Dominated_Solutions(afpo):
	#Calculates size of Pareto Front
	afpo['paretoFrontSize'] = population.Count_Non_Dominated_Solutions(afpo['population'])

def Cull(afpo):
	#Removes dominated solutions
	population.Cull(afpo['population'])

def Create(envList, robotType, p, gens, steps, pop):
	#Creates new afpo algorithm
	afpo = {}

	afpo['nextAvailableID'] = 0

	afpo['currentGeneration'] = 0
	afpo['p'] = p
	afpo['gens'] = gens
	afpo['steps'] = steps
	afpo['pop'] = pop
	afpo['paretoFrontSize'] = 0
	afpo['robotType'] = robotType
	afpo['population'] = population.Create(afpo,envList,robotType)
	afpo['fitnessList'] = []
	#afpo['environment'] = environment.CreateFF(0)
	#environment.Save(afpo['environment'])

	return afpo
def Reset(afpo,envList):
	afpo['currentGeneration'] = 0
	population.Reset(afpo['population'],envList)

def Delete_Data_Files():
	#Deletes data folder
	systemCommand = 'rm Data/*'
	os.system(systemCommand)

def Evaluate(afpo,envList):
	#Sends each member of the population to the simulator
	population.Evaluate(afpo['population'],envList)

def Evolve(afpo,envList,target=-1):
	#Evolves the population
	Reset(afpo,envList)
	count = 1
	notFit= True

	while notFit:
		fit = Evolve_For_One_Generation(afpo,envList)
		afpo['fitnessList'].append(fit)
		notFit = False
		afpo['currentGeneration'] += 1
		for e in envList:
			if afpo['population'][0]['envError'][e] >.15:
				notFit = True
		count = count+1
		
	return count

	# Reset(afpo,envList)
	# count = 1
	# for afpo['currentGeneration'] in range(0,afpo['gens']):
	# 	fit = Evolve_For_One_Generation(afpo,envList)
	# 	afpo['fitnessList'].append(fit)
	# 	if (fit<=target):
	# 		return count
	# 	count = count+1
	# return count
def Evolve_For_One_Generation(afpo,envList):
	#Runs through AFPO cycle of finding dominated solutions
	#and removing them etc.
	Evaluate(afpo,envList)

	Find_Pareto_Front(afpo)

	Sort(afpo)

	Count_Non_Dominated_Solutions(afpo)

	Print(afpo)

	bestFitness = afpo['population'][0]['error']

	SaveBest(afpo)
	
	Cull(afpo)

	Age_Survivors(afpo)

	Fill(afpo,envList)

	Inject_New_Genome(afpo,envList)

	return bestFitness

def Fill(afpo,envList):
	#Adds mutated individuals to the population
	population.Fill(afpo,envList)
		
def Find_Pareto_Front(afpo):
	#Finds non - dominated solutions
	population.Find_Pareto_Front(afpo['population'])

def Inject_New_Genome(afpo,envList):
	#Adds new individual age 0
	population.Inject_New_Genome(afpo,envList,afpo['robotType'])

def Print(afpo):
	errList = []
	for env in afpo['population'][0]['envError']:
		errList.append(afpo['population'][0]['envError'][env])
	errList = "%.2f "*len(errList) % tuple(errList)
	print afpo['currentGeneration'] , afpo['paretoFrontSize'] , afpo['population'][0]['error'] , errList, afpo['population'][0]['age']

def PickleBest(afpo,pickleFileName):
	population.PickleBest(afpo['population'],pickleFileName)

def SaveBest(afpo):

	population.SaveBest(afpo['population'])

def Sort(afpo):
	#Sorts population by non-dominated best solutions
	population.Sort(afpo['population'])
def TestAllEnvs(afpo,envList):
	population.TestAllEnvs(afpo['population'], envList)
