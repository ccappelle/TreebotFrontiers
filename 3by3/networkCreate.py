import tree
import node
import neuron
import edge
import random
import numpy as np
import environment
initRange = 2.0
initOffset = 1.0
def AddFullNetwork(t,neuronsPerNode):
	numNodes = tree.CalcNodes(t['maxDepth'])
	numNeurons = numNodes*neuronsPerNode
	nodeID = t['nodeID']

	for currNeuron in range(neuronsPerNode):
		neuronValue = float(currNeuron)
		#myValue = random.random()*2.0-1.0
		myNeuron = neuron.Create(neuronValue)
		for nodeID in range(numNodes):
			for neuronID in range(neuronsPerNode):
				edgeWeight = random.random()*2.0-1.0
				#edgeWeight = float(neuronID)
				myEdge = edge.Create(nodeID,neuronID,edgeWeight)
				myNeuron = neuron.AddOutEdge(myNeuron,myEdge)

		t['node'] = node.AddNeuronToNode(t['node'],myNeuron)
	
	for c in range(t['numChildren']):
		t[c] = AddFullNetwork(t[c],neuronsPerNode)

	return t
def AddRandomNetwork(t, neuronArray, minEdges, maxEdges):
	nodeID = t['nodeID']
	neuronsInNode = neuronArray[nodeID]

	for n in range(neuronsInNode):
		myNeuron = neuron.Create()
		numEdges = random.randint(minEdges,maxEdges)
		usedEdges = {}
		for e in range(numEdges):
			nodePointedTo = random.randint(0,len(neuronArray)-1)
			neuronPointedTo = random.randint(0,neuronArray[nodePointedTo]-1)
			if (nodePointedTo not in usedEdges) or (nodePointedTo in usedEdges 
				and neuronPointedTo not in usedEdges[nodePointedTo]):
			
				weight = random.random()*2.0-1.0
				myEdge = edge.Create(nodePointedTo,neuronPointedTo,weight)
				myNeuron = neuron.AddOutEdge(myNeuron,myEdge)
				usedEdges[nodePointedTo] = {}
				usedEdges[nodePointedTo][neuronPointedTo] = neuronPointedTo
		t['node'] = node.AddNeuronToNode(t['node'],myNeuron)
	for c in range(t['numChildren']):
		t[c] = AddRandomNetwork(t[c], neuronArray,minEdges, maxEdges)

	return t

def CreateRandomNetwork(t,minNeurons,maxNeurons, minEdges, maxEdges):
	numNodes = tree.CalcNodes(t['maxDepth'])
	neuronArray = np.random.randint(minNeurons,maxNeurons,numNodes)
	nodeID = t['nodeID']
	t = AddRandomNetwork(t,neuronArray,minEdges,maxEdges)
	
	return t



def CreateModularTest_3_nodes_01():
	basePosition ={}
	basePosition[0] = 0.0
	basePosition[1] = 0.0
	basePosition[2] = 0.5
	t = tree.Create({},0,1,basePosition,0.0,0.0,0.0,0.0,0)
	t = tree.SetJointType(t,0,0)
	s1 = neuron.Create(0,1)
	s2 = neuron.Create(0,1)
	j1 = neuron.Create(0,2)
	j2 = neuron.Create(0,2)
	h11 = neuron.Create(0,0)
	h12 = neuron.Create(0,0)
	h13 = neuron.Create(0,0)
	h14 = neuron.Create(0,0)
	h15 = neuron.Create(0,0)
	h21 = neuron.Create(0,0)
	h22 = neuron.Create(0,0)
	h23 = neuron.Create(0,0)
	h24 = neuron.Create(0,0)
	h25 = neuron.Create(0,0)
	t = tree.AddNeuronList(t, [1,1,2,2],[s1,j1,s2,j2])
	t = tree.AddNeuronList(t, [1,1,1,1,1],[h11,h12,h13,h14,h15])
	t = tree.AddNeuronList(t, [2,2,2,2,2],[h21,h22,h23,h24,h25])
	
	s1_to_h11 = edge.Create(1,2,np.random.random()*initRange-initOffset)
	s1_to_h12 = edge.Create(1,3,np.random.random()*initRange-initOffset)
	s1_to_h13 = edge.Create(1,4,np.random.random()*initRange-initOffset)
	s1_to_h14 = edge.Create(1,5,np.random.random()*initRange-initOffset)
	
	h11_to_h11 = edge.Create(1,2,np.random.random()*initRange-initOffset)
	h11_to_h12 = edge.Create(1,3,np.random.random()*initRange-initOffset)
	h11_to_h13 = edge.Create(1,4,np.random.random()*initRange-initOffset)
	h11_to_h14 = edge.Create(1,5, np.random.random()*initRange-initOffset)
	h11_to_h15 = edge.Create(1,6, np.random.random()*initRange-initOffset)
	h11_to_j1 = edge.Create(1,1,np.random.random()*initRange-initOffset)

	h12_to_h11 = edge.Create(1,1,np.random.random()*initRange-initOffset)
	h12_to_h12 = edge.Create(1,3,np.random.random()*initRange-initOffset)
	h12_to_h13 = edge.Create(1,4,np.random.random()*initRange-initOffset)
	h12_to_h14 = edge.Create(1,5,np.random.random()*initRange-initOffset)
	h12_to_h15 = edge.Create(1,6,np.random.random()*initRange-initOffset)
	h12_to_j1 = edge.Create(1,1,np.random.random()*initRange-initOffset)

	h13_to_h13 = edge.Create(1,4,np.random.random()*initRange-initOffset)
	h13_to_h12 = edge.Create(1,3,np.random.random()*initRange-initOffset)
	h13_to_h11 = edge.Create(1,2,np.random.random()*initRange-initOffset)
	h13_to_h14 = edge.Create(1,5,np.random.random()*initRange-initOffset)
	h13_to_h15 = edge.Create(1,6,np.random.random()*initRange-initOffset)
	h13_to_j1 = edge.Create(1,1,np.random.random()*initRange-initOffset)

	h14_to_h14 = edge.Create(1,5,np.random.random()*initRange-initOffset)
	h14_to_h13 = edge.Create(1,4,np.random.random()*initRange-initOffset)
	h14_to_h11 = edge.Create(1,2,np.random.random()*initRange-initOffset)
	h14_to_h12 = edge.Create(1,3,np.random.random()*initRange-initOffset)
	h14_to_j1 = edge.Create(1,1,np.random.random()*initRange-initOffset)

	h15_to_h15 = edge.Create(1,6,np.random.random()*initRange-initOffset)
	h15_to_h13 = edge.Create(1,4,np.random.random()*initRange-initOffset)
	h15_to_h11 = edge.Create(1,2,np.random.random()*initRange-initOffset)
	h15_to_h12 = edge.Create(1,3,np.random.random()*initRange-initOffset)
	h15_to_j1 = edge.Create(1,1,np.random.random()*initRange-initOffset)


	j1_to_h11 = edge.Create(1,2,random.random()*initRange-initOffset)
	j1_to_h12 = edge.Create(1,3,random.random()*initRange-initOffset)
	j1_to_h13 = edge.Create(1,4,random.random()*initRange-initOffset)
	j1_to_h14 = edge.Create(1,5,random.random()*initRange-initOffset)
	j1_to_h15 = edge.Create(1,6,random.random()*initRange-initOffset)
	j1_to_j1  = edge.Create(1,1,random.random()*initRange-initOffset)
#------
	s2_to_h21 = edge.Create(2,2,np.random.random()*initRange-initOffset)
	s2_to_h22 = edge.Create(2,3,np.random.random()*initRange-initOffset)
	s2_to_h23 = edge.Create(2,4,np.random.random()*initRange-initOffset)
	s2_to_h24 = edge.Create(2,5,np.random.random()*initRange-initOffset)
	
	h21_to_h21 = edge.Create(2,2,np.random.random()*initRange-initOffset)
	h21_to_h22 = edge.Create(2,3,np.random.random()*initRange-initOffset)
	h21_to_h23 = edge.Create(2,4,np.random.random()*initRange-initOffset)
	h21_to_h24 = edge.Create(2,5,np.random.random()*initRange-initOffset)
	h21_to_h25 = edge.Create(2,6,np.random.random()*initRange-initOffset)
	h21_to_j2 = edge.Create(2,1,np.random.random()*initRange-initOffset)

	h22_to_h21 = edge.Create(2,2,np.random.random()*initRange-initOffset)
	h22_to_h22 = edge.Create(2,3,np.random.random()*initRange-initOffset)
	h22_to_h23 = edge.Create(2,4,np.random.random()*initRange-initOffset)
	h22_to_h24 = edge.Create(2,5,np.random.random()*initRange-initOffset)
	h22_to_h25 = edge.Create(2,6,np.random.random()*initRange-initOffset)
	h22_to_j2  = edge.Create(2,1,np.random.random()*initRange-initOffset)

	h23_to_h23 = edge.Create(2,4,np.random.random()*initRange-initOffset)
	h23_to_h22 = edge.Create(2,3,np.random.random()*initRange-initOffset)
	h23_to_h21 = edge.Create(2,2,np.random.random()*initRange-initOffset)
	h23_to_h24 = edge.Create(2,5,np.random.random()*initRange-initOffset)
	h23_to_h25 = edge.Create(2,6,np.random.random()*initRange-initOffset)
	h23_to_j2 = edge.Create(2,1,np.random.random()*initRange-initOffset)

	h24_to_h24 = edge.Create(2,5,np.random.random()*initRange-initOffset)
	h24_to_h23 = edge.Create(2,4,np.random.random()*initRange-initOffset)
	h24_to_h21 = edge.Create(2,2,np.random.random()*initRange-initOffset)
	h24_to_h22 = edge.Create(2,3,np.random.random()*initRange-initOffset)
	h24_to_j2 = edge.Create(2,1,np.random.random()*initRange-initOffset)

	h25_to_h25 = edge.Create(2,6,np.random.random()*initRange-initOffset)
	h25_to_h23 = edge.Create(2,4,np.random.random()*initRange-initOffset)
	h25_to_h21 = edge.Create(2,2,np.random.random()*initRange-initOffset)
	h25_to_h22 = edge.Create(2,3,np.random.random()*initRange-initOffset)
	h25_to_j2 = edge.Create(2,1,np.random.random()*initRange-initOffset)

	j2_to_h23 = edge.Create(2,4,random.random()*initRange-initOffset)
	j2_to_h21 = edge.Create(2,2,random.random()*initRange-initOffset)
	j2_to_h22 = edge.Create(2,3,random.random()*initRange-initOffset)
	j2_to_h24 = edge.Create(2,5,random.random()*initRange-initOffset)
	j2_to_h25 = edge.Create(2,6,random.random()*initRange-initOffset)
	j2_to_j2  = edge.Create(2,1,random.random()*initRange-initOffset)
#------------	
	t = tree.AddEdgeToNeuron(t, 1, 0, s1_to_h11)
	t = tree.AddEdgeToNeuron(t, 1, 0, s1_to_h12)
	t = tree.AddEdgeToNeuron(t, 1, 0, s1_to_h13)
	t = tree.AddEdgeToNeuron(t, 1, 0, s1_to_h14)

	t = tree.AddEdgeToNeuron(t, 1, 2, h11_to_h12)
	t = tree.AddEdgeToNeuron(t, 1, 2, h11_to_h11)
	t = tree.AddEdgeToNeuron(t, 1, 2, h11_to_j1)
	t = tree.AddEdgeToNeuron(t, 1, 2, h11_to_h13)
	t = tree.AddEdgeToNeuron(t, 1, 2, h11_to_h14)
	#t = tree.AddEdgeToNeuron(t, 1,2, h11_to_h15)

	t = tree.AddEdgeToNeuron(t, 1, 3, h12_to_h11)
	t = tree.AddEdgeToNeuron(t, 1, 3, h12_to_h12)
	t = tree.AddEdgeToNeuron(t, 1, 3, h12_to_j1)
	t = tree.AddEdgeToNeuron(t, 1,3, h12_to_h13)
	t = tree.AddEdgeToNeuron(t, 1,3, h12_to_h14)
	#t = tree.AddEdgeToNeuron(t,1,3, h12_to_h15)

	t = tree.AddEdgeToNeuron(t, 1, 4, h13_to_h13)
	t = tree.AddEdgeToNeuron(t, 1, 4, h13_to_h12)
	t = tree.AddEdgeToNeuron(t, 1, 4, h13_to_h11)
	t = tree.AddEdgeToNeuron(t, 1, 4, h13_to_h14)
	#t = tree.AddEdgeToNeuron(t, 1,4, h13_to_h15)
	t = tree.AddEdgeToNeuron(t, 1, 4, h13_to_j1)


	t = tree.AddEdgeToNeuron(t, 1, 5, h14_to_h14)
	t = tree.AddEdgeToNeuron(t, 1, 5, h14_to_h12)
	t = tree.AddEdgeToNeuron(t, 1, 5, h14_to_h11)
	t = tree.AddEdgeToNeuron(t, 1, 5, h14_to_h13)
	t = tree.AddEdgeToNeuron(t, 1, 5, h14_to_j1)

	#t = tree.AddEdgeToNeuron(t, 1,6,h15_to_h11)
	#t = tree.AddEdgeToNeuron(t, 1,6,h15_to_h12)
	#t = tree.AddEdgeToNeuron(t, 1,6,h15_to_h13)
	#t = tree.AddEdgeToNeuron(t, 1,6,h15_to_h15)
	#t = tree.AddEdgeToNeuron(t, 1,6,h15_to_j1)

	t = tree.AddEdgeToNeuron(t, 1, 1, j1_to_j1)
	t = tree.AddEdgeToNeuron(t, 1, 1, j1_to_h13)
	t = tree.AddEdgeToNeuron(t, 1, 1, j1_to_h11)
	t = tree.AddEdgeToNeuron(t, 1, 1, j1_to_h12)
	#t = tree.AddEdgeToNeuron(t, 1,1,j1_to_h15)
	#t = tree.AddEdgeToNeuron(t, 1, 1, j1_to_h14)
   #-----------
	t = tree.AddEdgeToNeuron(t, 2, 0, s2_to_h21)
	t = tree.AddEdgeToNeuron(t, 2, 0, s2_to_h22)
	t = tree.AddEdgeToNeuron(t, 2, 0, s2_to_h23)
	t = tree.AddEdgeToNeuron(t, 2, 0, s2_to_h24)

	t = tree.AddEdgeToNeuron(t, 2, 2, h21_to_h21)
	t = tree.AddEdgeToNeuron(t, 2, 2, h21_to_h22)
	t = tree.AddEdgeToNeuron(t, 2, 2, h21_to_j2)
	t = tree.AddEdgeToNeuron(t, 2, 2, h21_to_h23)
	t = tree.AddEdgeToNeuron(t, 2, 2, h21_to_h24)
	#t = tree.AddEdgeToNeuron(t, 2,2, h21_to_h25)

	#t = tree.AddEdgeToNeuron(t, 2, 3, h22_to_h21)
	t = tree.AddEdgeToNeuron(t, 2, 3, h22_to_h22)
	#t = tree.AddEdgeToNeuron(t, 2, 3, h22_to_j2)
	#t = tree.AddEdgeToNeuron(t, 2,3, h22_to_h23)
	t = tree.AddEdgeToNeuron(t, 2,3, h22_to_h24)
	t = tree.AddEdgeToNeuron(t, 2, 3, h22_to_h25)

	t = tree.AddEdgeToNeuron(t, 2, 4, h23_to_h23)
	t = tree.AddEdgeToNeuron(t, 2, 4, h23_to_h22)
	t = tree.AddEdgeToNeuron(t, 2, 4, h23_to_h21)
	t = tree.AddEdgeToNeuron(t, 2, 4, h23_to_j2)
	t = tree.AddEdgeToNeuron(t, 2, 4, h23_to_h24)
	#t = tree.AddEdgeToNeuron(t,2,4, h23_to_h25)

	t = tree.AddEdgeToNeuron(t, 2, 5, h24_to_h24)
	t = tree.AddEdgeToNeuron(t, 2, 5, h24_to_h22)
	t = tree.AddEdgeToNeuron(t, 2, 5, h24_to_h21)
	t = tree.AddEdgeToNeuron(t, 2, 5, h24_to_h23)
	t = tree.AddEdgeToNeuron(t, 2, 5, h24_to_j2)	

	#t = tree.AddEdgeToNeuron(t, 2, 6, h25_to_h25)
	#t = tree.AddEdgeToNeuron(t, 2, 6, h25_to_h22)
	#t = tree.AddEdgeToNeuron(t, 2, 6, h25_to_h21)
	#t = tree.AddEdgeToNeuron(t, 2, 6, h25_to_h23)
	#t = tree.AddEdgeToNeuron(t, 2, 6, h25_to_j2)	

	t = tree.AddEdgeToNeuron(t, 2, 1, j2_to_j2)
	t = tree.AddEdgeToNeuron(t, 2, 1, j2_to_h23)
	t = tree.AddEdgeToNeuron(t, 2, 1, j2_to_h21)
	t = tree.AddEdgeToNeuron(t, 2, 1, j2_to_h22)
	t = tree.AddEdgeToNeuron(t, 2, 1, j2_to_h24)
	#t = tree.AddEdgeToNeuron(t,2,1,j2_to_h25)
	return t


def CreateMNM_01():
	basePosition ={}
	basePosition[0] = 0.0
	basePosition[1] = 0.0
	basePosition[2] = 0.5
	t = tree.Create({},0,1,basePosition,0.0,0.0,0.0,0.0,0)
	t = tree.SetJointType(t,0,0)
	s1 = neuron.Create(0,1)
	s2 = neuron.Create(0,1)
	j1 = neuron.Create(0,2)
	j2 = neuron.Create(0,2)
	t = tree.AddNeuronList(t, [1,1,2,2],[s1,j1,s2,j2])
	myRand = np.random.rand(4)*initRange-initOffset
	s1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	s1_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)

	j1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	j1_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	

	s2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	s2_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)

	j2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	j2_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)

	t = tree.AddEdgeList(t,[1,1],[0,0],[s1_to_j1,s1_to_j2])
	t = tree.AddEdgeList(t,[1,1],[1,1],[j1_to_j1,j1_to_j2])
	t = tree.AddEdgeList(t,[2,2],[0,0],[s2_to_j2,s2_to_j1])
	t = tree.AddEdgeList(t,[2,2],[1,1],[j2_to_j2,j2_to_j1])

	return t

def CreateMNM_02():
	basePosition ={}
	basePosition[0] = 0.0
	basePosition[1] = 0.0
	basePosition[2] = 0.5
	t = tree.Create({},0,1,basePosition,0.0,0.0,0.0,0.0,0)
	t = tree.SetJointType(t,0,0)
	s1 = neuron.Create(0,1)
	s2 = neuron.Create(0,1)
	j1 = neuron.Create(0,2)
	j2 = neuron.Create(0,2)
	h1 = neuron.Create(0,0)
	h2 = neuron.Create(0,0)


	t = tree.AddNeuronList(t, [1,1,2,2,1,2],[s1,j1,s2,j2,h1,h2])
	myRand = np.random.rand(4)*initRange-initOffset
	s1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	s1_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	s1_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)
	s1_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)

	j1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	j1_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	j1_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)
	j1_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)

	s2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	s2_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	s2_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)
	s2_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)

	j2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	j2_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	j2_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)
	j2_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)

	h1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	h1_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	h1_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)
	h1_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)

	h2_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	h2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	h2_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)
	h2_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)

	t = tree.AddEdgeList(t,[1,1,1,1],[0,0,0,0],[s1_to_j1,s1_to_j2,s1_to_h1,s1_to_h2])

	t = tree.AddEdgeList(t,[1,1,1,1],[1,1,1,1],[j1_to_j1,j1_to_j2,j1_to_h1,j1_to_h2])

	t = tree.AddEdgeList(t,[2,2,2,2],[0,0,0,0],[s2_to_j2,s2_to_j1,s2_to_h1,s2_to_h2])

	t = tree.AddEdgeList(t,[2,2,2,2],[1,1,1,1],[j2_to_j2,j2_to_j1,j2_to_h1,j2_to_h2])

	t = tree.AddEdgeList(t,[1,1,1,1],[2,2,2,2],[h1_to_j1,h1_to_j2,h1_to_h1,h1_to_h2])
	
	t = tree.AddEdgeList(t,[2,2,2,2],[2,2,2,2],[h2_to_j1,h2_to_j2,h2_to_h2,h2_to_h1])
	
	return t

def CreateModularTest_3_nodes_02():
	basePosition ={}
	basePosition[0] = 0.0
	basePosition[1] = 0.0
	basePosition[2] = 0.5
	t = tree.Create({},0,1,basePosition,0.0,0.0,0.0,0.0,0)
	t = tree.SetJointType(t,0,0)
	s1 = neuron.Create(0,1)
	s2 = neuron.Create(0,1)
	j1 = neuron.Create(0,2)
	j2 = neuron.Create(0,2)
	h1 = neuron.Create(0,0)
	h2 = neuron.Create(0,0)
	t = tree.AddNeuronList(t, [1,1,2,2],[s1,j1,s2,j2])
	t = tree.AddNeuronList(t,[1,2],[h1,h2])
	s1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	s1_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)

	j1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	j1_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)

	s2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	s2_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)

	j2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	j2_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)

	h2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	h2_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)

	h1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	h1_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)


	t = tree.AddEdgeList(t,[1,1],[0,0],[s1_to_j1,s1_to_h1])
	t = tree.AddEdgeList(t,[1,1],[1,1],[j1_to_j1,j1_to_h1])
	t = tree.AddEdgeList(t,[1,1],[2,2],[h1_to_h1,h1_to_j1])
	t = tree.AddEdgeList(t,[2,2],[0,0],[s2_to_j2,s2_to_h2])
	t = tree.AddEdgeList(t,[2,2],[1,1],[j2_to_j2,j2_to_h2])
	t = tree.AddEdgeList(t,[2,2],[2,2],[h2_to_h2,h2_to_j2])
	return t

def CreateModularTest_3_nodes_03():
	basePosition ={}
	basePosition[0] = 0.0
	basePosition[1] = 0.0
	basePosition[2] = 0.5
	t = tree.Create({},0,1,basePosition,0.0,0.0,0.0,0.0,0)
	t = tree.SetJointType(t,0,0)
	s1 = neuron.Create(0,1)
	s2 = neuron.Create(0,1)
	j1 = neuron.Create(0,2)
	j2 = neuron.Create(0,2)
	h1 = neuron.Create(0,0)
	h2 = neuron.Create(0,0)
	h3 = neuron.Create(0,0)
	h4 = neuron.Create(0,0)
	t = tree.AddNeuronList(t, [1,1,2,2],[s1,j1,s2,j2])
	t = tree.AddNeuronList(t,[1,2,1,2],[h1,h2,h3,h4])
	s1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	s1_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)
	s1_to_h3 = edge.Create(1,3,np.random.rand()*initRange-initOffset)
	
	j1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	j1_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)
	j1_to_h3 = edge.Create(1,3,np.random.rand()*initRange-initOffset)
	
	s2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	s2_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)
	s2_to_h4 = edge.Create(2,3,np.random.rand()*initRange-initOffset)
	
	j2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	j2_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)
	j2_to_h4 = edge.Create(2,3,np.random.rand()*initRange-initOffset)
	
	h2_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	h2_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)
	h2_to_h4 = edge.Create(2,3,np.random.rand()*initRange-initOffset)

	h1_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	h1_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)
	h1_to_h3 = edge.Create(1,3,np.random.rand()*initRange-initOffset)

	h3_to_j1 = edge.Create(1,1,np.random.rand()*initRange-initOffset)
	h3_to_h1 = edge.Create(1,2,np.random.rand()*initRange-initOffset)
	h3_to_h3 = edge.Create(1,3,np.random.rand()*initRange-initOffset)

	h4_to_j2 = edge.Create(2,1,np.random.rand()*initRange-initOffset)
	h4_to_h2 = edge.Create(2,2,np.random.rand()*initRange-initOffset)
	h4_to_h4 = edge.Create(2,3,np.random.rand()*initRange-initOffset)

	t = tree.AddEdgeList(t,[1,1,1],[0,0,0],[s1_to_j1,s1_to_h1,s1_to_h3])
	t = tree.AddEdgeList(t,[1,1,1],[1,1,1],[j1_to_j1,j1_to_h1,j1_to_h3])
	t = tree.AddEdgeList(t,[1,1,1],[2,2,2],[h1_to_h1,h1_to_j1,h1_to_h3])
	t = tree.AddEdgeList(t,[2,2,2],[0,0,0],[s2_to_j2,s2_to_h2,s2_to_h4])
	t = tree.AddEdgeList(t,[2,2,2],[1,1,1],[j2_to_j2,j2_to_h2,j2_to_h4])
	t = tree.AddEdgeList(t,[2,2,2],[2,2,2],[h2_to_h2,h2_to_j2,h2_to_h4])
	t = tree.AddEdgeList(t,[1,1,1],[3,3,3],[h3_to_h3,h3_to_h1,h3_to_j1])
	t = tree.AddEdgeList(t,[2,2,2],[3,3,3],[h4_to_h4,h4_to_h2,h4_to_j2])
	return t

def CreateNonModularTest_03():
	basePosition ={}
	basePosition[0] = 0.0
	basePosition[1] = 0.0
	basePosition[2] = 0.5
	t = tree.Create({},0,1,basePosition,0.0,0.0,0.0,0.0,0)

	t = tree.SetJointType(t,0,1)
	t = tree.SetJointType(t,1,0)
	t = tree.SetJointType(t,2,0)

	s1 = neuron.Create(0,1)
	s2 = neuron.Create(0,1)
	j = neuron.Create(0,2)

	h1 = neuron.Create(0,0)
	h2 = neuron.Create(0,0)
	h3 = neuron.Create(0,0)
	h4 = neuron.Create(0,0)

	t = tree.AddNeuronList(t, [1,2,0,0,0,0,0],[s1,s2,j,h1,h2,h3,h4])
	#t = tree.AddNeuronToNode(t, 0, b1)

	s1_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	s1_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	s1_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	s1_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	s2_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	s2_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	s2_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	s2_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	j_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	j_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	j_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	j_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	h1_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	h1_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h1_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h1_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	h2_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h2_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	h2_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h2_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	h3_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	h3_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h3_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h3_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	#Sensor 1 
	#t = tree.AddEdgeList(t,[1,1,1],[0,0,0],[s1_to_h2,s1_to_h1,s1_to_h3])
	t = tree.AddEdgeList(t,[1,1],[0,0],[s1_to_h2,s1_to_h1])

	#Sensor 2
	#t = tree.AddEdgeList(t,[2,2,2],[0,0,0],[s2_to_h1,s2_to_h2,s2_to_h3])
	t = tree.AddEdgeList(t,[2,2],[0,0],[s2_to_h1,s2_to_h2])
	
	#Joint neuron
	t = tree.AddEdgeList(t,[0,0,0,0],[0,0,0,0],[j_to_j,j_to_h1,j_to_h2,j_to_h3])

	#H1
	t = tree.AddEdgeList(t,[0,0,0,0],[1,1,1,1],[h1_to_j,h1_to_h1,h1_to_h2,h1_to_h3])

	#h2
	t = tree.AddEdgeList(t,[0,0,0,0],[2,2,2,2],[h2_to_j,h2_to_h2,h2_to_h1,h2_to_h3])

	#h3
	t = tree.AddEdgeList(t,[0,0,0,0],[3,3,3,3],[h3_to_j,h3_to_h1,h3_to_h2,h3_to_h3])

	return t

def CreateNonModularTest_3_nodes_02():
	basePosition ={}
	basePosition[0] = 0.0
	basePosition[1] = 0.0
	basePosition[2] = 0.5
	t = tree.Create({},0,1,basePosition,0.0,0.0,0.0,0.0,0)

	t = tree.SetJointType(t,0,1)
	t = tree.SetJointType(t,1,0)
	t = tree.SetJointType(t,2,0)

	s1 = neuron.Create(0,1)
	s2 = neuron.Create(0,1)
	j = neuron.Create(0,2)

	h1 = neuron.Create(0,0)
	h2 = neuron.Create(0,0)
	h3 = neuron.Create(0,0)

	t = tree.AddNeuronList(t, [1,2,0,0,0,0],[s1,s2,j,h1,h2,h3])
	#t = tree.AddNeuronToNode(t, 0, b1)

	s1_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	s1_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	s1_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	s1_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	s2_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	s2_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	s2_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	s2_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	j_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	j_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	j_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	j_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	h1_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	h1_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h1_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h1_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	h2_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h2_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	h2_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h2_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	h3_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	h3_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h3_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h3_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)

	#Sensor 1 
	#t = tree.AddEdgeList(t,[1,1,1],[0,0,0],[s1_to_h2,s1_to_h1,s1_to_h3])
	t = tree.AddEdgeList(t,[1,1],[0,0],[s1_to_h2,s1_to_h1])

	#Sensor 2
	#t = tree.AddEdgeList(t,[2,2,2],[0,0,0],[s2_to_h1,s2_to_h2,s2_to_h3])
	t = tree.AddEdgeList(t,[2,2],[0,0],[s2_to_h1,s2_to_h2])
	
	#Joint neuron
	t = tree.AddEdgeList(t,[0,0,0,0],[0,0,0,0],[j_to_j,j_to_h1,j_to_h2,j_to_h3])

	#H1
	t = tree.AddEdgeList(t,[0,0,0,0],[1,1,1,1],[h1_to_j,h1_to_h1,h1_to_h2,h1_to_h3])

	#h2
	t = tree.AddEdgeList(t,[0,0,0,0],[2,2,2,2],[h2_to_j,h2_to_h2,h2_to_h1,h2_to_h3])

	#h3
	t = tree.AddEdgeList(t,[0,0,0,0],[3,3,3,3],[h3_to_j,h3_to_h1,h3_to_h2,h3_to_h3])

	return t

def CreateNonModularTest_3_nodes_01():
	basePosition ={}
	basePosition[0] = 0.0
	basePosition[1] = 0.0
	basePosition[2] = 0.5
	t = tree.Create({},0,1,basePosition,0.0,0.0,0.0,0.0,0)
	t = tree.SetJointType(t,0,1)
	t = tree.SetJointType(t,1,0)
	t = tree.SetJointType(t,2,0)
	s1 = neuron.Create(0,1)
	s2 = neuron.Create(0,1)
	j = neuron.Create(0,2)
	h1 = neuron.Create(0,0)
	h2 = neuron.Create(0,0)
	h3 = neuron.Create(0,0)
	h4 = neuron.Create(0,0)
	h5 = neuron.Create(0,0)
	t = tree.AddNeuronList(t, [1,2,0,0,0],[s1,s2,j,h1,h2])
	t = tree.AddNeuronList(t,[0],[h3])
	t = tree.AddNeuronList(t,[0],[h4])
	t = tree.AddNeuronList(t,[0],[h5])
	#t = tree.AddNeuronToNode(t, 0, b1)

	s1_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	s1_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	s1_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)
	s1_to_h5 = edge.Create(0,5,random.random()*initRange-initOffset)

	s2_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	s2_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	s2_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)
	s2_to_h5 = edge.Create(0,5,random.random()*initRange-initOffset)

	j_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	j_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	j_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	j_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)
	j_to_h4 = edge.Create(0,4,random.random()*initRange-initOffset)
	j_to_h5 = edge.Create(0,5,random.random()*initRange-initOffset)

	h1_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	h1_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h1_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h1_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)
	h1_to_h4 = edge.Create(0,4,random.random()*initRange-initOffset)
	h1_to_h5 = edge.Create(0,5,random.random()*initRange-initOffset)

	h2_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h2_to_j = edge.Create(0,0,random.random()*initRange-initOffset)
	h2_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h2_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)
	h2_to_h4 = edge.Create(0,4,random.random()*initRange-initOffset)
	h2_to_h5 = edge.Create(0,5,random.random()*initRange-initOffset)


	h3_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h3_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h3_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)
	h3_to_h4 = edge.Create(0,4,random.random()*initRange-initOffset)
	h3_to_h5 = edge.Create(0,5,random.random()*initRange-initOffset)
	h3_to_j = edge.Create(0,0,random.random()*initRange-initOffset)

	h4_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h4_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h4_to_h4 = edge.Create(0,4,random.random()*initRange-initOffset)
	h4_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)
	h4_to_h5 = edge.Create(0,5,random.random()*initRange-initOffset)
	h4_to_j = edge.Create(0,0,random.random()*initRange-initOffset)


	h5_to_h1 = edge.Create(0,1,random.random()*initRange-initOffset)
	h5_to_h2 = edge.Create(0,2,random.random()*initRange-initOffset)
	h5_to_h3 = edge.Create(0,3,random.random()*initRange-initOffset)
	h5_to_h4 = edge.Create(0,4,random.random()*initRange-initOffset)
	h5_to_h5 = edge.Create(0,5,random.random()*initRange-initOffset)
	h5_to_j = edge.Create(0,0,random.random()*initRange-initOffset)

	t = tree.AddEdgeList(t,[1],[0],[s1_to_h2])
	t = tree.AddEdgeList(t,[1],[0],[s1_to_h1])
	#t = tree.AddEdgeList(t,[1],[0],[s1_to_h5])
	t = tree.AddEdgeList(t,[1],[0],[s1_to_h3])

	t = tree.AddEdgeList(t,[2],[0],[s2_to_h1])
	t = tree.AddEdgeList(t,[2],[0],[s2_to_h2])
	#t = tree.AddEdgeList(t,[2],[0],[s2_to_h5])
	t = tree.AddEdgeList(t,[2],[0],[s2_to_h3])
	
	t = tree.AddEdgeList(t,[0],[0],[j_to_j])
	#t = tree.AddEdgeList(t,[0],[0],[j_to_h1])
	#t = tree.AddEdgeList(t,[0],[0],[j_to_h2])
	#t = tree.AddEdgeList(t,[0],[0],[j_to_h3])
	t = tree.AddEdgeList(t,[0],[0],[j_to_h4])
	t = tree.AddEdgeList(t,[0],[0],[j_to_h5])

	t = tree.AddEdgeList(t,[0],[1],[h1_to_h1])
	#t = tree.AddEdgeList(t,[0],[1],[h1_to_j])
	#t = tree.AddEdgeList(t,[0],[1],[h1_to_h2])
	#t = tree.AddEdgeList(t,[0],[1],[h1_to_h3])
	t = tree.AddEdgeList(t,[0],[1],[h1_to_h4])
	t = tree.AddEdgeList(t,[0],[1],[h1_to_h5])

	#t = tree.AddEdgeList(t,[0],[2],[h2_to_j])
	#t = tree.AddEdgeList(t,[0],[2],[h2_to_h1])
	t = tree.AddEdgeList(t,[0],[2],[h2_to_h2])
	#t = tree.AddEdgeList(t,[0],[2],[h2_to_h3])
	t = tree.AddEdgeList(t,[0],[2],[h2_to_h4])
	t = tree.AddEdgeList(t,[0],[2],[h2_to_h5])

	t = tree.AddEdgeList(t,[0],[3],[h3_to_h3])
	#t = tree.AddEdgeList(t,[0],[3],[h3_to_j])
	#t = tree.AddEdgeList(t,[0],[3],[h3_to_h1])
	#t = tree.AddEdgeList(t,[0],[3],[h3_to_h2])
	t = tree.AddEdgeList(t,[0],[3],[h3_to_h5])
	t = tree.AddEdgeList(t,[0],[3],[h3_to_h4])


	t = tree.AddEdgeList(t,[0],[4],[h4_to_h4])
	t = tree.AddEdgeList(t,[0],[4],[h4_to_j])
	t = tree.AddEdgeList(t,[0],[4],[h4_to_h3])
	t = tree.AddEdgeList(t,[0],[4],[h4_to_h1])
	t = tree.AddEdgeList(t,[0],[4],[h4_to_h2])

	t = tree.AddEdgeList(t,[0],[5],[h5_to_h1])
	t = tree.AddEdgeList(t,[0],[5],[h5_to_h2])
	#t = tree.AddEdgeList(t,[0],[5],[h5_to_h4])
	t = tree.AddEdgeList(t,[0],[5],[h5_to_h3])
	t = tree.AddEdgeList(t,[0],[5],[h5_to_h5])
	t = tree.AddEdgeList(t,[0],[5],[h5_to_j])

	return t


#myTree = CreateNonModularTest_3_nodes_01()
#tree.Plot_Tree_Neurons_Synapses(myTree)
#myTree =CreateModBody_NonModBrain()
#myTree = CreateModularTest_3_nodes()
#myTree = CreateNonModularTest_3_nodes_02()
#tree.Plot_Tree_Neurons_Synapses(myTree)
#tree.Plot_Tree_Neurons_Synapses(myTree)
#myTree =CreateMNM_02()
#myTree = CreateNonModularTest_3_nodes_02()
#tree.Plot_Tree_Neurons_Synapses(myTree)
#myTree = CreateNonModularTest_3_nodes_01()
#tree.Plot_Tree_Neurons_Synapses(myTree)
#print '*********************************************'
#tree.PrintTree(myTree)
#f = open('tempNet.txt','w')
#tree.SaveNetwork(myTree, f)
#myTree = tree.Mutate_Weights(myTree)
#print '____________________________________________'
#tree.PrintTree(myTree)

#tree.Save(myTree,'Data/evolved.txt','Data/evolvedNetwork.txt')



#************* Modular Trial *********************
# newNeuron = neuron.Create(typeOfNeuron=1)
# myTree = tree.AddNeuronToNode(myTree,1,newNeuron)
# newNeuron = neuron.Create(typeOfNeuron=1)
# myTree = tree.AddNeuronToNode(myTree,2,newNeuron)
# newNeuron = neuron.Create(typeOfNeuron=2)
# myTree = tree.AddNeuronToNode(myTree,1,newNeuron)
# newNeuron = neuron.Create(typeOfNeuron=2)
# myTree = tree.AddNeuronToNode(myTree,2,newNeuron)
# newEdge = edge.Create(1,1,.5)
# myTree = tree.AddEdgeToNeuron(myTree,1,0,newEdge)
# newEdge = edge.Create(2,1,.5)
# myTree = tree.AddEdgeToNeuron(myTree,2,0,newEdge)
# tree.Plot_Tree_Neurons_Synapses(myTree)

#************ Non-Modular Trial ********************
# myTree['joint']['type'] = 1
# myTree[0]['joint']['type'] = 0
# myTree[1]['joint']['type'] = 0
# newNeuron = neuron.Create(typeOfNeuron=2)
# myTree = tree.AddNeuronToNode(myTree,0,newNeuron)
# newNeuron = neuron.Create(typeOfNeuron=1)
# myTree = tree.AddNeuronToNode(myTree,1,newNeuron)
# myTree = tree.AddNeuronToNode(myTree,2,newNeuron)
# newEdge = edge.Create(0,0,.5)
# myTree = tree.AddEdgeToNeuron(myTree,1,0,newEdge)
# myTree = tree.AddEdgeToNeuron(myTree,2,0,newEdge)
# tree.Plot_Tree_Neurons_Synapses(myTree)


# tree.Plot_Tree_Only(myTree)
# tree.Plot_Tree_Neurons_Only(myTree)
# tree.Plot_Tree_Neurons_Synapses(myTree)

# myTree = tree.Create({},0,1,basePosition, 0.0,0.0,0.0,0.0,0)

# myTree = AddFullNetwork(myTree, 2)
# tree.Plot_Tree_Neurons_Synapses(myTree)
# tree.RemoveNeuron(myTree,0,0)
# tree.Plot_Tree_Neurons_Synapses(myTree)
# newNeuron = neuron.Create()
# tree.AddNeuronToNode(myTree,1,newNeuron)
# tree.Plot_Tree_Neurons_Synapses(myTree)
# newEdge = edge.Create(2,0,.5)
# tree.AddEdgeToNeuron(myTree,1,2,newEdge)
# newEdge = edge.Create(0,1,.5)
# tree.AddEdgeToNeuron(myTree,1,2,newEdge)
# newEdge = edge.Create(1,2,.5)
# tree.AddEdgeToNeuron(myTree,1,2,newEdge)
# tree.Plot_Tree_Neurons_Synapses(myTree)