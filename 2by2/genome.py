import tree
import copy
import random
import os
import networkCreate
import environment
from subprocess import Popen, PIPE

FF = 0
FU = 1
UF = 2
UU = 3

MODULAR = 0
M2 = 1
M3 = 2

MNM1 = 3
MNM2 = 4

NONMODULAR_1 = 5
NONMODULAR_2 = 6

MOD_MORPH =1
NM_MORPH = 2
def Copy(parent,myID,envList):
	#Copies parent genome (mainly to prep for mutation)
	g = copy.deepcopy(parent)

	for e in envList:
		g['evaluated'][e] = False

	g['ID'] = myID

	g['dominated'] = False

	return g

def Create(myID,envList,robotType,p,steps):
	#Creates a genome with designated ID 
	g = {}
	g['evaluated'] = {}
	for e in envList:
		g['evaluated'][e] = False

	g['envError'] ={}
	g['ID'] = myID

	g['dominated'] = False

	g['age'] = 0
	g['p'] = p
	g['steps'] = steps
	ROBOT_TYPE = robotType
	# */	//MODULAR ERROR
	# 	//FF (0.0, 0.920911097732)
	# 	//FU,UF (0.0010, 0.9976)
	# 	//UU (0.0034, 1.0)
	# 	F_MIN_DIST = 5.156854;		
	# 	F_MAX_DIST = 5.315064;
	# 	U_MIN_DIST = 5.156854;
	# 	U_MAX_DIST = 5.315064;
	
	# /*
	# 	//NM ERror

	# 	//FF (0.1294 , 1.0)
	# 	//UF FU (0.1305, 1.0)
	# 	//UU (0.3185, 1.0)
	# 	F_MIN_DIST = 5.028258;		
	# 	F_MAX_DIST = 6.001822;
	# 	U_MIN_DIST = 5.028258;
	# 	U_MAX_DIST = 7.596333;
	# */
	morphology = 0
	if ROBOT_TYPE == MODULAR:
		g['tree'] = networkCreate.CreateModularTest_3_nodes_01() 
		morphology = 1
	elif ROBOT_TYPE == M2:
		g['tree'] = networkCreate.CreateModularTest_3_nodes_02()
		morphology = 1
	elif ROBOT_TYPE == M3:
		g['tree'] = networkCreate.CreateModularTest_3_nodes_03()
		morphology = 1
	elif ROBOT_TYPE == MNM1:
		g['tree'] = networkCreate.CreateMNM_01()
		morphology = 1
	elif ROBOT_TYPE == MNM2:
		g['tree'] = networkCreate.CreateMNM_02()
		morphology = 1
	elif ROBOT_TYPE == NONMODULAR_1:
		g['tree'] = networkCreate.CreateNonModularTest_3_nodes_01()
		morphology = 2
	elif ROBOT_TYPE == NONMODULAR_2:
		g['tree'] = networkCreate.CreateNonModularTest_3_nodes_02()
		morphology = 2


	if (morphology == NM_MORPH):
		g['F_min'] =  5.02;
		g['F_max'] = 5.8;		
		g['U_min']=  5.02 #5.028258;
		g['U_max']= 7.2#7.2 #7.2 #7.596333;
		g['Min_Case_Error'] = [0.169, 0.1634, 0.1634,  0.287425]#0.3065705813877807]#[0.13, 0.151669, 0.151669, 0.367764]
		g['Max_Case_Error'] = [1.0, 1.0, 1.0, 0.937223]#[0.989230,.742,.742,0.470388]
	#Create_Tree(g)

	if (morphology == MOD_MORPH):
		g['F_min'] = 5.156854
		g['F_max'] = 5.315064
		g['U_min'] =  5.156854
		g['U_max'] = 5.315064
		g['Min_Case_Error'] = [0.0, 0.013, 0.013, 0.026]
		g['Max_Case_Error'] = [1.0, 1.0, 1.0, 1.0]

	g['treeString'] = tree.toString(g['tree'])
	return g

def Reset(g,envList):
	g['envError'] = {}
	g['evaluated'] = {}
	for e in envList:
		g['evaluated'][e] = False

	g['dominated'] = False
def Create_Tree(g):
	#Initializes tree with desired parameters for experiment
	maxDepth = 3

	basePosition = {}
	basePosition[0] = 0
	basePosition[1] = 0
	basePosition[2] = 1.05

	g['tree'] = tree.Create({},0,maxDepth,basePosition,0.0,0.0,0.0,0.0,0)

def Determine_Whether_g1_Is_Dominated_By_g2(g1,g2):
	#Checks if g1 is dominated by g2
	#['dominated'] parameter is initialized to false
	if ( g2['age'] <= g1['age'] ): #If g1 is younger it is not dominated

		if ( g2['error'] <= g1['error'] ): #If fitness of greater than g2, g1 is not dominated

			if ( (g2['age']==g1['age']) & (g2['error']==g1['error']) ):
				#If both are equal take the one that has the higher ID
				g1['dominated'] = g2['ID'] > g1['ID']
			else:
				g1['dominated'] = True
	
def Dominated(g):

	return g['dominated']

def CalcFitness(f):
 	totalError = 0.0
 	for line in f:
 		totalError = totalError + float(str(line))

	return totalError

def Evaluated(g,env):
	return g['evaluated'][env]

def Reset_Error(g):
	g['error'] = 0.0
	return g

def Get_Results_From_Simulator(g,env):
	#Reads relult from simulator output
	resultsFileName = 'Data/results'+str(g['ID'])+'_'+str(env)+'.txt'
	#Waits until the result file is present
	while ( os.path.isfile(resultsFileName) == False):
		pass
	
	f = open(resultsFileName, 'r')
	#Reads fitness
	g['envError'][env] = abs(CalcFitness(f)-g['Min_Case_Error'][env])/(g['Max_Case_Error'][env]-g['Min_Case_Error'][env])
	f.close()
	
	#Deletes results file
	systemCommand = 'rm ' + resultsFileName
	os.system(systemCommand)


	#Checks that the genome was evaluated
	g['evaluated'][env] = True

def Get_Older(g):
	#Ages genome
	g['age'] = g['age'] + 1

def Make_Non_Dominated(g):
	#Resests dominated status
	g['dominated'] = False

def Mutate(g):
	#Mutates tree paramets
	#numInternalNodes = tree.NumInternalNodes(g['tree'])

	#tree.Mutate( g['tree'] , numInternalNodes , g['age'] )

	g['tree'] = tree.Mutate_Weights(g['tree'],g['p'])

def Print(g):

	print str(g['treeCost']) , str(g['age']), str(g['dominated']) , str(g['ID'])

def PickleBest(g,pickleFileName):
	tree.Save_Pickle(g['tree'],pickleFileName)

def Save(g,fileName,networkFileName):
	#Saves tree to file
	tree.Save( g['tree'] , fileName, networkFileName )

def Set_Total_Error(g,envList):
	totalError = 0.0
	counter = 0.0
	#max
	#for e in envList:
	#	if (totalError<g['envError'][e]):
	#		totalError = g['envError'][e]
	#g['error'] = totalError

	#avg
	for e in envList:
		totalError = totalError + g['envError'][e]
		counter = counter+1.0
	g['error'] = totalError/counter

	#weighted avg
	# if len(envList)==1:
	# 	g['error'] = g['envError'][envList[0]]
	# else:
	# 	valList = []
	# 	for e in envList:
	# 		valList.append(g['envError'][e])

	# 	valList.sort()
	# 	valList = valList[::-1]

	# 	numLeft = len(envList)
	# 	divider = 2.0
	# 	for val in valList:
	# 		totalError = totalError + val/divider
	# 		if numLeft>2:
	# 			divider = divider*2.0
	# 		numLeft = numLeft-1
	# 	g['error'] = totalError
	return g
def Send_Tree_To_Simulator(g,env):
	#Sends tree to simulator

	#Saves tree to designated file location
	#tempFileName = 'Data/temp'+str(g['ID'])+'.txt'
	#tempnetworkFileName = 'Data/networkTemp'+str(g['ID'])+'.txt'
	#Save(g,tempFileName,tempnetworkFileName)
	#gString = tree.toString(g['tree'])
	gNetworkString = tree.BrainToString(g['tree'])
	currEnv = environment.getEnv(env)
	#treeFileName = 'Data/tree'+str(g['ID'])+'.txt'
	#networkFileName = 'Data/network'+str(g['ID'])+'.txt'

	#Moves temp file to tree folder
	#systemCommand = 'mv '+str(tempFileName)+' '+str(treeFileName)
	#os.system(systemCommand)
	#systemCommand = 'mv '+str(tempnetworkFileName)+' '+str(networkFileName)
	#os.system(systemCommand)
	#Runs simulator in headless mode for x time steps on evironment 0
	#Gives command low priority

	p = Popen(['./Simulate','0'], stdout = PIPE, stdin = PIPE, stderr = PIPE)
	sendString = g['treeString'] + ' ' + gNetworkString + ' '+currEnv+ ' '+str(g['steps'])+' '+str(g['F_min'])+ ' ' +str(g['F_max'])+ ' ' + str(g['U_min'])+ ' ' + str(g['U_max'])
	fitness, errors = p.communicate(input = str.encode(sendString))
	g['envError'][env] = (float(fitness)-g['Min_Case_Error'][env])/(g['Max_Case_Error'][env]-g['Min_Case_Error'][env])
	g['evaluated'][env] = True
	#systemCommand = 'nice -n 20 ./Simulate '+str(g['ID'])+' '+str(env)+' ' \
	#				+str(g['steps'])+' 0 '+ str(g['F_min']) + ' ' + str(g['F_max']) \
	#				+ ' '+ str(g['U_min']) + ' ' + str(g['U_max'])+ '&'

	#os.system(systemCommand)

	