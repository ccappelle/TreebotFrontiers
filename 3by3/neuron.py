import edge
import math

NORMAL = 0
SENSOR = 1
MOTOR = 2
BIAS = 3
NEURON_PLOT_SIZE = .05
NEURON_BOTTOM = 3
NEURON_TOP = 4
COLORS = ['yellow','w','b','g']
def Create(value=0,typeOfNeuron=0):
	#Create an empty neuron with a value
	neuron = {}
	neuron['neuronID']= {}
	neuron['outEdges'] = {}
	neuron['value'] = value
	neuron['numEdges'] = 0
	neuron['nextIndex'] = 0
	neuron['type'] = typeOfNeuron
		
	return neuron

def AddOutEdge(neuron,edge):
	#Adds an edge to a neuron and increases the number of edges
	#and the next index to place an edge
	nextIndex = neuron['nextIndex']
	neuron['outEdges'][nextIndex] = edge
	neuron['nextIndex'] = nextIndex + 1
	neuron['numEdges'] = neuron['numEdges'] + 1

	return neuron

def RemoveOutEdge(neuron,index):
	#Removes an edge and re indexes remaining edges accordingly
	del neuron['outEdges'][index]

	for i in range(index,neuron['numEdges']-1):
		neuron['outEdges'][i] = neuron['outEdges'][i+1]

	if neuron['numEdges']-1 in neuron['outEdges']:
		del neuron['outEdges'][neuron['numEdges']-1]

	neuron['nextIndex'] = neuron['nextIndex'] - 1
	neuron['numEdges'] = neuron['numEdges'] - 1
	return neuron

def RemoveDeadEdges(neuron, nodeID, neuronIndex):
	for index in neuron['outEdges']:
		myEdge = neuron['outEdges'][index]
		if myEdge['nodePointedTo'] == nodeID:
			if myEdge['neuronPointedTo'] == neuronIndex:
				neuron = RemoveOutEdge(neuron,index)
				return neuron
	return neuron
def ChangePointedTo(neuron,nodeID,neuronIndex):
	for index in neuron['outEdges']:
		myEdge = neuron['outEdges'][index]
		if myEdge['nodePointedTo'] == nodeID:
			if myEdge['neuronPointedTo']>neuronIndex:
				myEdge = edge.PointToDifferentNeuron(myEdge,nodeID,myEdge['neuronPointedTo']-1)

	return neuron
def SetID(neuron,ID):
	neuron['neuronID'] = ID
	return neuron
def SetValueOfNeuron(neuron,value):
	neuron['value'] = value
	return neuron

def SetWeightOfEdge(neuron,index,weight):
	neuron['outEdges'][index] = edge.SetWeight(neuron['outEdges'][index],weight)
	return neuron

def ApplyUpdate(neuron, value):
	neuron['value'] = math.tanh(value)
	return neuron

def Mutate_Weights(neuron,p):
	for e in neuron['outEdges']:
		neuron['outEdges'][e] = edge.Mutate_Weights(neuron['outEdges'][e],p)

	return neuron
	
def UpdateNetwork(neuron, networkUpdateDict):
	#Adds values to the update dictionary for each edge in the neuron
	value = neuron['value']

	for e in neuron['outEdges']:
		nodePointedTo = edge.GetNodePointedTo(neuron['outEdges'][e])
		neuronPointedTo = edge.GetNeuronPointedTo(neuron['outEdges'][e])
		weight = edge.GetWeight(neuron['outEdges'][e])

		#Creates entries in the dict for given nodes and neurons
		if nodePointedTo not in networkUpdateDict:
			networkUpdateDict[nodePointedTo] = {}

		if neuronPointedTo not in networkUpdateDict[nodePointedTo]:
			networkUpdateDict[nodePointedTo][neuronPointedTo] = weight*neuron['value']
		else:
			networkUpdateDict[nodePointedTo][neuronPointedTo] = networkUpdateDict[nodePointedTo][neuronPointedTo]+weight*neuron['value']

	return networkUpdateDict

def PrintNeuron(neuron):
	print '\tNeuron ID: ', neuron['neuronID'], ', Value: ', neuron['value'], ', Number of Edges: ', neuron['numEdges']
	for index in neuron['outEdges']:
		edge.PrintEdge(neuron['outEdges'][index])

def Save(neuron, f):
	f.write('[')
	f.write(str(neuron['numEdges']))
	f.write(',')
	for index in neuron['outEdges']:
		edge.Save(neuron['outEdges'][index],f)
	f.write(']')

def PlotNeuron(neuron,ax,centerX,centerY):
	import myPlot
	#colors neuron based on its type
	color = COLORS[neuron['type']]

	#Plots a circle to represent the neuron
	ax = myPlot.plotCircle(centerX,centerY,NEURON_PLOT_SIZE,
			ax,color=color,zorder=NEURON_TOP,lineWidth=1) 
	return ax

def PlotSynapses(neuron,posDict,ax,nodeID):
	neurID = neuron['neuronID']
	#Plots each outward synapse from the neuron
	for e in neuron['outEdges']:
		ax = edge.PlotSynapse(neuron['outEdges'][e],posDict,ax,nodeID,neurID)

	return ax

def fillWeightMatrix(neuron,neuronPosList,weightMatrix,nodeID):
	for e in neuron['outEdges']:
		fromID = (nodeID,neuron['neuronID'])
		weightMatrix = edge.fillWeightMatrix(neuron['outEdges'][e],neuronPosList,weightMatrix,fromID)

	return weightMatrix
