import neuron
import edge
import math
import tree

def AddNeuronToNode(node, neur):
	#Adds neuron to the node
	#Places neuron at the next available index
	neur = neuron.SetID(neur,node['nextIndex'])
	node['neurons'][node['nextIndex']] = neur

	node['nextIndex'] = node['nextIndex'] + 1
	node['numNeurons'] = node['numNeurons'] + 1
	return node
def AddEdgeToNeuron(node,neuronID,edge):

	node['neurons'][neuronID] = neuron.AddOutEdge(node['neurons'][neuronID],edge)
	return node
	
def Create(myID):
	#Creates a node empty of neurons
	node = {}
	node['ID'] = myID
	node['neurons'] = {}
	node['numNeurons'] = 0
	node['nextIndex'] = 0

	return node

def RemoveNeuronFromNode(node,index):
	#Removes the node from the Neuron
	del node['neurons'][index]

	for i in range(index,node['numNeurons']-1):
		node['neurons'][i] = node['neurons'][i+1]
		node['neurons'][i] = neuron.SetID(node['neurons'][i],i)

	if node['numNeurons']-1 in node['neurons']:
		del node['neurons'][node['numNeurons']-1]

	node['nextIndex'] = node['nextIndex'] - 1
	node['numNeurons'] = node['numNeurons'] - 1 
	return node

def RemoveDeadEdges(node,nodeID,neuronIndex):
	for index in node['neurons']:
		node['neurons'][index] = neuron.RemoveDeadEdges(node['neurons'][index],nodeID,neuronIndex)

	for index in node['neurons']:
		node['neurons'][index] = neuron.ChangePointedTo(node['neurons'][index],nodeID,neuronIndex)
	return node

def ReplaceNeuronInNode(node,index,replacementNeuron):
	node['neuron'][index] = replacementNeuron

def SetValueOfNeuron(node,indexOfNeuron,value):
	neur = node['neurons'][indexOfNeuron]
	node['neurons'][indexOfNeuron] = neuron.SetValueOfNeuron(neur,value)
	return node

def ApplyUpdate(node, newNeuronValues):
	for index in newNeuronValues:
		node['neurons'][index] = neuron.ApplyUpdate(node['neurons'][index],newNeuronValues[index])
	return node
	
def UpdateNetwork(node, networkUpdateDict):
	#Runs through the neurons in the node updating the update dict
	for neur in node['neurons']:
		currNeuron = node['neurons'][neur]
		networkUpdateDict = neuron.UpdateNetwork(currNeuron,networkUpdateDict)

	return networkUpdateDict

def Mutate_Weights(node,p):
	for n in node['neurons']:
		node['neurons'][n] = neuron.Mutate_Weights(node['neurons'][n],p)

	return node

def PrintNode(node):
	print 'Node ID: ', node['ID'], ', Num Neurons ', node['numNeurons']
	for index in node['neurons']:
		neuron.PrintNeuron(node['neurons'][index])

	print '-----------------'

def Save(node,f):
	f.write(str(node['ID']))
	f.write(',')
	f.write(str(node['numNeurons']))
	f.write(',')
def NodeToString(node):
	return str(node['ID'])+','+str(node['numNeurons']) + ','
def PlotNeurons(node,ax,centerX,centerY):
	numNeurons = float(node['numNeurons'])
	if numNeurons == 0:
		return ax
	delta = 2.*math.pi/numNeurons
	radius = 0.1
	count = 0.0
	for n in node['neurons']:
		x = centerX+radius*math.cos(count*delta-math.pi/2.0)
		y = centerY+radius*math.sin(count*delta-math.pi/2.0)
		ax = neuron.PlotNeuron(node['neurons'][n],ax,x,y)
		count = count + 1
	return ax

def PlotSynapses(node,posDict,ax):	
	nodeID = node['ID']
	for n in node['neurons']:
		ax=neuron.PlotSynapses(node['neurons'][n],posDict,ax,nodeID)

	return ax

def getPositionDict(node,centerX,centerY,posDict):
	numNeurons = float(node['numNeurons'])
	if numNeurons==0:
		return posDict

	delta = 2*math.pi/numNeurons
	radius = 0.1
	count = 0.0
	for n in node['neurons']:
		x = centerX+radius*math.cos(count*delta-math.pi/2.0)
		y = centerY+radius*math.sin(count*delta-math.pi/2.0)
		posDict[node['ID']][n]=[x,y]
		count = count+1

	return posDict

def fillNeuronLists(node, neuronPosList,neuronTypeList):
	for n in node['neurons']:
		neuronPosList.append((node['ID'],n)) 
		neuronTypeList.append(node['neurons'][n]['type'])

	return neuronPosList, neuronTypeList

def fillWeightMatrix(node, neuronPosList, weightMatrix):
	for n in node['neurons']:
		weightMatrix = neuron.fillWeightMatrix(node['neurons'][n],neuronPosList,weightMatrix,node['ID'])

	return weightMatrix
