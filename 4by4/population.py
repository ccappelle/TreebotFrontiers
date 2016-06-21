import genome
import random
import tree
import numpy as np
import multiprocessing
from operator import itemgetter


def Age_Survivors(population):
	#Increase the age of the leftover population
	for g in range(0,len(population)):

		genome.Get_Older( population[g] )

def Count_Non_Dominated_Solutions(population):
	#total the non dominated trees
	numNonDominated = 0

	while ( genome.Dominated(population[numNonDominated]) == False):
		numNonDominated = numNonDominated + 1
		if (numNonDominated==len(population)):
			return numNonDominated

	return numNonDominated
	
def Create(afpo,envList,robotType):
	#Creates new EA
	population = []
	popSize = afpo['pop']
	for g in range(0,popSize):
		#Add genomes until population size is reached
		population.append(genome.Create(afpo['nextAvailableID'],envList,robotType,afpo['p'],afpo['steps']))

		afpo['nextAvailableID'] = afpo['nextAvailableID'] + 1

	return population

def Reset(population,envList):
	popSize = len(population)
	for g in range(popSize):
		genome.Reset(population[g],envList)

def Cull(population):
	popSize = len(population)
	#Delete the dominated solutions
	for g in range(popSize-1,0,-1):

		if ( genome.Dominated(population[g]) ):

			del population[g]


def Evaluate(population,envList):
	popSize = len(population)
	#Runs x trials in parallel
	processesToRunInParallel = 5
	#population = Reset_Error(population)
	for env in envList:		
		for i in range(0,popSize,processesToRunInParallel):
			jobs = []
			#Sends each tree to simulator
			for g in range(i,i+processesToRunInParallel):
				if ( genome.Evaluated(population[g],env) == False ):
					SendToSimulator(population[g],env)
					
			#Retrieves the result from the simulator for each tree

			#for g in range(i,i+processesToRunInParallel):
			#	if ( genome.Evaluated(population[g],env) == False ):
			#		genome.Get_Results_From_Simulator(population[g],env)

	for g in range(popSize):
		genome.Set_Total_Error(population[g],envList)

def SendToSimulator(g,env):
	genome.Send_Tree_To_Simulator(g,env)


def Fill(afpo,envList):

	population = afpo['population']
	popSize = afpo['pop']
	#Fills the population with mutated trees
	for g in range( afpo['paretoFrontSize'] , popSize - 1 ):

		genomeToCopy = random.randint( 0 , afpo['paretoFrontSize'] - 1 ) 

		population.append( genome.Copy( population[genomeToCopy] , afpo['nextAvailableID'] , envList) )

		afpo['nextAvailableID'] = afpo['nextAvailableID'] + 1

		genome.Mutate( population[g] )

def Find_Pareto_Front(population):
	#Makes all genoms non dominated
	Make_All_Genomes_Non_Dominated(population)
	popSize = len(population)
	#Finds which genomes are dominated
	for g1 in range(0,popSize):
		g2 = 0
		while ( (g2<popSize) and (genome.Dominated(population[g1])==False) ):
			if ( g1 != g2 ):
				genome.Determine_Whether_g1_Is_Dominated_By_g2(population[g1],population[g2])
			
			g2 = g2 + 1

def Inject_New_Genome(afpo,envList,robotType):
	#Adds new random genome to the pool
	population = afpo['population']
	p = afpo['p']
	population.append( genome.Create(afpo['nextAvailableID'],envList,robotType, p,afpo['steps']) )

	afpo['nextAvailableID'] = afpo['nextAvailableID'] + 1

def Make_All_Genomes_Non_Dominated(population):
	#Resets dominated value
	for g in range(0,len(population)):
		genome.Make_Non_Dominated(population[g])

def Print(population):
	#Prints non-dominated population
	for g in range(0,len(population)):

		if ( genome.Dominated(population[g]) == False ):

			genome.Print(population[g])
def PickleBest(population, pickleFileName):
	genome.PickleBest(population[0], pickleFileName)



def SaveBest(population):

	genome.Save(population[0],'Data/evolved.txt', 'Data/evolvedNetwork.txt')
	#if population[0].has_key('error'):
	#	g = population[0]
	#	f = open('fitnessFile.txt','a')
	#	f.write(str(g['error'])+'\n')
	#	f.close()
	#	f = open('envErrorFile.txt','a')
	#	for key in g['envError']:
	#		f.write(str(key)+'-'+str(g['envError'][key])+',')
	#	f.write('\n')
	#	f.close()

def Sort(population):
	#Sorted list with nondominated best items first
	population.sort(key=itemgetter('error'))
	population.sort(key=itemgetter('dominated'))

def TestAllEnvs(population, envList):
	t = population[0]
	for e in envList:
		genome.Send_Tree_To_Simulator(t,e)
