import copy
import math
import random
import node
import joint
import pickle
import myPlot
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

FIXED_JOINT = 0
HINGE_JOINT = 1
TREE_BOTTOM = 1
TREE_TOP = 2

def AddNeuronList(t,nodeIDs, neurons):
	for i in range(len(nodeIDs)):
		nodeID = nodeIDs[i]
		neuron = neurons[i]
		t = AddNeuronToNode(t,nodeID,neuron)

	return t

def AddNeuronToNode(t,nodeID,neur):
	if t['isRoot']:
		t['numNeurons'] = t['numNeurons'] + 1
	#Searches tree nodes to find right ID and then adds a neuron
	#to that node
	t['AvailableNodes'][nodeID] = t['node']['nextIndex']
	#Uses binary search (i.e. only viable for binary trees with
		#specific ID numbering convention)
	if nodeID == t['nodeID']:
		t['node'] = node.AddNeuronToNode(t['node'],neur)
	else:
		if nodeID>=t[1]['nodeID']:
			t[1] = AddNeuronToNode(t[1],nodeID,neur)
		else:
			t[0] = AddNeuronToNode(t[0],nodeID,neur)
			
	return t
def AddEdgeList(t,nodeIDs,neuronIDs,edges):
	for i in range(len(nodeIDs)):
		nodeID = nodeIDs[i]
		neuronID = neuronIDs[i]
		edge = edges[i]
		t = AddEdgeToNeuron(t,nodeID,neuronID,edge)

	return t

def AddEdgeToNeuron(t,nodeID,neuronID,edge):
	#Finds node id and adds edge to the specific neuron in the node
	if nodeID == t['nodeID']:
		t['node'] = node.AddEdgeToNeuron(t['node'],neuronID,edge)
	else:
		if nodeID>=t[1]['nodeID']:
			t[1] = AddEdgeToNeuron(t[1],nodeID,neuronID,edge)
		else:
			t[0] = AddEdgeToNeuron(t[0],nodeID,neuronID,edge)
	return t

def RemoveNeuron(t,nodeID,neuronIndex):
	t = RemoveNeuronFromNode(t,nodeID,neuronIndex)
	t = RemoveDeadEdges(t,nodeID,neuronIndex)
	return t

def RemoveNeuronFromNode(t,nodeID,neuronIndex):
	#Finds the neuron to remove and deletes it
	if t['isRoot']:
		t['numNeurons'] = t['numNeurons'] - 1

	if nodeID == t['nodeID']:
		t['node'] = node.RemoveNeuronFromNode(t['node'],neuronIndex)
	else:
		if nodeID>=t[1]['nodeID']:
			t[1] = RemoveNeuronFromNode(t[1], nodeID,neuronIndex)
		else:
			t[0] = RemoveNeuronFromNode(t[0],nodeID,neuronIndex)
	
	return t

def RemoveDeadEdges(t,nodeID,neuronIndex):
	#Searches thru each node removing all edges to that specific location
	t['node'] = node.RemoveDeadEdges(t['node'], nodeID,neuronIndex)
	for c in range(t['numChildren']):
		t[c] = RemoveDeadEdges(t[c],nodeID,neuronIndex)

	return t

def CalcNodes(depth):
	return 2**(depth+1)-1

def Cost(t):

	cost = t['length']

	for c in range(0,t['numChildren']):
		cost = cost + Cost(t[c])

	return cost

def Create(t,currDepth,maxDepth,basePosition,minAngle,myAngle,maxAngle,cumulativeAngle,nodeID):
	#Base position for each branch
	t['basePosition'] = basePosition
	t['maxDepth'] = maxDepth
	t['myAngle'] = myAngle
	t['numNeurons'] = 0

	#Changes relative angle to global one
	cumulativeAngle = cumulativeAngle + myAngle 

	t['AvailableNodes'] = {}
	#Radius used in ODE
	t['radius'] = 0.05
	t['length'] = 1.0

	if currDepth ==0:
		t['isRoot'] = True
	else:
		t['isRoot'] = False
	t['depth'] = currDepth
	#Sets tip position at vector with relative angle as indicated
	#and length 1
	t['tipPosition'] = {}
	t['tipPosition'][0] = t['basePosition'][0] + t['length'] * math.sin( cumulativeAngle )
	t['tipPosition'][1] = t['basePosition'][1] + t['length'] * math.cos( cumulativeAngle )
	t['tipPosition'][2] = t['basePosition'][2]

	#Start by creating hinge joints everywhere
	t['joint'] = joint.Create(HINGE_JOINT,minAngle,maxAngle)

	t['node'] = node.Create(nodeID)
	t['nodeID'] = nodeID
	#Creates children if max depth is not reached
	if ( currDepth < maxDepth ):
		t['numChildren'] = 2
		childAngle = ( 3.14159/4.0 ) / ( float(currDepth) + 1.0 ) 

		myAngle = -childAngle

		minAngle = -3.14159/2.0 - myAngle
		maxAngle = +3.14159/2.0 - myAngle

		t[0] = Create({},currDepth+1,maxDepth,t['tipPosition'],minAngle,myAngle,maxAngle,cumulativeAngle,nodeID+1)
		
		myAngle = +childAngle

		minAngle = -3.14159/2.0 - myAngle
		maxAngle = +3.14159/2.0 - myAngle

		t[1] = Create({},currDepth+1,maxDepth,t['tipPosition'],minAngle,myAngle,maxAngle,cumulativeAngle,nodeID+1+CalcNodes(maxDepth-currDepth-1))

	else:
		t['numChildren'] = 0

	if t['numChildren'] == 0:
		t['isLeaf'] = True
	else:
		t['isLeaf'] = False
	return t

def SetJointType(t,nodeID,jointType):
	if nodeID == t['nodeID']:
		t['joint'] = joint.SetJointType(t['joint'],jointType)
	elif nodeID>=t[1]['nodeID']:
		t[1] = SetJointType(t[1],nodeID,jointType)
	else:
		t[0] = SetJointType(t[0],nodeID,jointType)

	return t

def Fingers_Will_Cross(t):
	#Calculate wether the leaves will collide eventually
	finger0EventualAngle = t[0]['myAngle'] + t[0]['joint']['desiredAngle']
	finger1EventualAngle = t[1]['myAngle'] + t[1]['joint']['desiredAngle']

	return finger0EventualAngle>=finger1EventualAngle

def Has_Children(t):

	return ( t['numChildren'] > 0 )

def Has_Hinge_Joint(t):

	return joint.Is_Hinge_Joint(t['joint'])

def Mutate(t,numInternalNodes,age):
	if (Has_Children(t)):
		Mutate_DesiredAngle(t,numInternalNodes,age)

		for c in range(0,t['numChildren']):
			Mutate(t[c],numInternalNodes,age)

def Mutate_Weights(t,p):
	t['node'] = node.Mutate_Weights(t['node'],p)

	for c in range(t['numChildren']):
		t[c] = Mutate_Weights(t[c],p)

	return t

def Mutate_DesiredAngle(t,numInternalNodes,age):
	prob = 1.0/float(numInternalNodes + 1.0)

	if ( random.random()>=prob):
		return
	originalDesiredAngle = t[1]['joint']['desiredAngle']
	joint.Perturb_Desired_Angle(t[1]['joint'],age);

	while( Fingers_Will_Cross(t)):
		joint.Set_Desired_Angle(t[1]['joint'],originalDesiredAngle)
		joint.Perturb_Desired_Angle(t[1]['joint'],age);

def NumInternalNodes(t):
	#Returns number of branches
	if ( t['numChildren'] == 0 ):

		return 0

	else:

		numInternalNodes = 1

		for c in range(0,t['numChildren']):

			numInternalNodes = numInternalNodes + NumInternalNodes(t[c])

		return numInternalNodes

def Print(t):

	print 'Number of children: ' , t['numChildren']

	node.PrintNode(t['node'])

def Print_Node_And_Its_Children(t):

	Print(t)

	for c in range(0,t['numChildren']):
	
		Print(t[c])

def PrintTree(t):
	Print(t)

	for c in range(0,t['numChildren']):
		PrintTree(t[c])
def Recalculate_Length(t):

	t['length'] = math.pow( t['tipPosition'][0] - t['basePosition'][0] ,2.0)
	t['length'] = t['length'] + math.pow( t['tipPosition'][1] - t['basePosition'][1] ,2.0)
	t['length'] = t['length'] + math.pow( t['tipPosition'][2] - t['basePosition'][2] ,2.0)
	t['length'] = math.sqrt( t['length'] )

def Save_Pickle(t,pickleFileName):
	pickleFile = open(pickleFileName,'w')
	pickle.dump(t,pickleFile)
	pickleFile.close()

def toString(t):
	treeBody = BodyToString(t) + ')'
	#treeBrain = BrainToString(t)
	return treeBody
def Save(t,fileName1,fileName2):
	f1 = open(fileName1,'w')
	SaveNode(t,f1)
	f1.close()

	f2 = open(fileName2,'w')
	SaveNetwork(t,f2)
	f2.close()

def BodyToString(t):

	bodyString = ('(' + str(t['numChildren'])+
					',' + str(t['basePosition'][0]) + ',' + str(t['basePosition'][1]) + ',' + str(t['basePosition'][2])+
					',' + str(t['tipPosition'][0]) + ',' + str(t['tipPosition'][1]) +','+ str(t['tipPosition'][2]) +
					',' + str(t['radius']) + ',' + str(t['depth']) + ',')

	bodyString = bodyString + joint.JointToString(t['joint']) + node.NodeToString(t['node'])

	for c in range(0,t['numChildren']):
		bodyString = bodyString + BodyToString(t[c]) + ')'
	
	return bodyString 
def SaveNode(t,f):

	f.write( '(' )		

        f.write( str(t['numChildren']) )
        f.write( "," )

	f.write( str(t['basePosition'][0]) )
        f.write( "," )

        f.write( str(t['basePosition'][1]) )
        f.write( "," )

        f.write( str(t['basePosition'][2]) )
        f.write( "," )


        f.write( str(t['tipPosition'][0]) )
        f.write( "," )

        f.write( str(t['tipPosition'][1]) )
        f.write( "," )

        f.write( str(t['tipPosition'][2]) )
        f.write( "," )

        f.write( str(t['radius']) )
        f.write( "," )

        f.write( str(t['depth']))
        f.write(",")
        
	joint.Save(t['joint'],f)
	node.Save(t['node'],f)
	for c in range(0,t['numChildren']):

		SaveNode(t[c],f)

        f.write( ')' ) 


def Size(t):

	size = 1

        for c in range(0,t['numChildren']):

		size = size + Size(t[c])

	return size
def Plot_Tree_Only(t):
	fig = plt.figure()
	ax = fig.add_subplot(111, aspect = 'equal')
	ax = PlotTree(t,ax)
	plt.axis('off')
	plt.show()

def Plot_Tree_Neurons_Only(t):
	fig = plt.figure()
	ax = fig.add_subplot(111,aspect = 'equal')
	ax = PlotTree(t,ax)
	ax = PlotNeurons(t,ax)
	plt.axis('off')
	plt.show()

def Plot_Tree_Neurons_Synapses(t):
	posDict ={}
	posDict = getPositionDict(t,posDict)
	fig = plt.figure()
	ax = fig.add_subplot(111,aspect = 'equal',axisbg='white')
	ax = PlotTree(t,ax)
	ax = PlotNeurons(t,ax)
	ax = PlotSynapses(t,posDict,ax)
	plt.axis('off')
	plt.show()

def PlotTree(t,ax):
	nodeXPos = t['basePosition'][0]
	nodeYPos = t['basePosition'][1]
	baseXPos = t['basePosition'][0]
	baseYPos = t['basePosition'][1]
	tipXPos = t['tipPosition'][0]
	tipYPos = t['tipPosition'][1]

	if joint.Is_Hinge_Joint(t['joint']):
		ax = myPlot.plotCircle(nodeXPos,nodeYPos,0.2,ax,color='#ADDFFF',zorder=TREE_TOP)
	else:
		ax = myPlot.plotSquare(nodeXPos,nodeYPos,0.25,ax,color='#E77471',zorder=TREE_TOP)
	if t['isLeaf']:
		ax = myPlot.plotCircle(tipXPos,tipYPos,0.2,ax,color='#FFF8DC',zorder=TREE_TOP)

	ax.plot([baseXPos, tipXPos],[baseYPos, tipYPos],'k',linewidth=3,zorder=TREE_BOTTOM)
	for c in range(t['numChildren']):
		ax = PlotTree(t[c],ax)

	return ax

def PlotNeurons(t,ax):
	nodeXPos = t['basePosition'][0]
	nodeYPos = t['basePosition'][1]
	baseXPos = t['basePosition'][0]
	baseYPos = t['basePosition'][1]
	tipXPos = t['tipPosition'][0]
	tipYPos = t['tipPosition'][1]
	ax = node.PlotNeurons(t['node'],ax,tipXPos,tipYPos)
	for c in range(t['numChildren']):
		ax = PlotNeurons(t[c],ax)
	return ax

def PlotSynapses(t,posDict,ax):
	ax = node.PlotSynapses(t['node'],posDict,ax)
	for c in range(t['numChildren']):
		ax = PlotSynapses(t[c],posDict,ax)

	return ax

def getPositionDict(t,posDict):
	x = t['tipPosition'][0]
	y = t['tipPosition'][1]
	posDict[t['nodeID']] = {}
	posDict = node.getPositionDict(t['node'],x,y,posDict)
	for c in range(t['numChildren']):
		posDict = getPositionDict(t[c],posDict)

	return posDict

def RunUpdate(t):
	updateDict = {}
	updateDict = UpdateNetwork(t,updateDict)

	t = ApplyUpdate(t,updateDict)

	return t

def ApplyUpdate(t,updateDict):
	nodeID = t['nodeID']
	if nodeID in updateDict:
		t['node'] = node.ApplyUpdate(t['node'],updateDict[nodeID])
	for c in range(t['numChildren']):
		t[c] = ApplyUpdate(t[c],updateDict)

	return t

def UpdateNetwork(t,networkUpdateDict):
	networkUpdateDict = node.UpdateNetwork(t['node'],networkUpdateDict)
	for c in range(t['numChildren']):
		networkUpdateDict = UpdateNetwork(t[c],networkUpdateDict)

	return networkUpdateDict
	
def SaveNetwork(t,f):
	CreateOutNetwork(t,f)

def BrainToString(t):
	import numpy as np
	numNodes = CalcNodes(t['maxDepth'])
	neuronPosList, neuronTypeList = fillNeuronLists(t,[],[])
	numNeurons = len(neuronTypeList)

	weightMatrix = np.zeros((numNeurons,numNeurons))
	weightMatrix = fillWeightMatrix(t,neuronPosList,weightMatrix)

	whichNode = np.zeros(numNeurons)
	for index in range(numNeurons):
		whichNode[index] = int(neuronPosList[index][0])

	brainString = str(numNodes)+','+str(int(numNeurons))+','
	for n in whichNode:
		brainString = brainString + str(int(n)) + ','

	for t in neuronTypeList:
		brainString = brainString + str(int(t)) + ','

	for i in range(numNeurons):
		for j in range(numNeurons):
			brainString = brainString + str(weightMatrix[i][j]) + ','
	
	return brainString

def CreateOutNetwork(t,f):
	import numpy as np
	numNodes = CalcNodes(t['maxDepth'])
	neuronPosList, neuronTypeList = fillNeuronLists(t,[],[])
	numNeurons = len(neuronTypeList)

	weightMatrix = np.zeros((numNeurons,numNeurons))
	weightMatrix = fillWeightMatrix(t,neuronPosList,weightMatrix)


	whichNode = np.zeros(numNeurons)
	for index in range(numNeurons):
		whichNode[index] = int(neuronPosList[index][0])


	f.write('{:d}'.format(numNodes))
	f.write(',')
	f.write('{:d}'.format(int(numNeurons)))
	f.write(',')
	for n in whichNode:
		f.write('{:d}'.format(int(n)))
		f.write(',')

	for t in neuronTypeList:
		f.write('{:d}'.format(int(t)))
		f.write(',')
	
	for i in range(numNeurons):
		for j in range(numNeurons):
			f.write(str(weightMatrix[i][j]))
			f.write(',')


def fillNeuronLists(t,neuronPosList,neuronTypeList):
	neuronPosList, neuronTypeList = node.fillNeuronLists(t['node'],neuronPosList,neuronTypeList)
	for c in range(t['numChildren']):
		neuronPosList, neuronTypeList = fillNeuronLists(t[c],neuronPosList,neuronTypeList)

	return neuronPosList, neuronTypeList

def fillWeightMatrix(t,neuronPosList,weightMatrix):
	weightMatrix = node.fillWeightMatrix(t['node'],neuronPosList,weightMatrix)

	for c in range(t['numChildren']):
		weightMatrix = fillWeightMatrix(t[c],neuronPosList,weightMatrix)

	return weightMatrix

def Load_Tree(fileName):
	f = open(fileName)
	t = pickle.load(f)
	f.close()

	return t





