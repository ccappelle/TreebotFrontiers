import math

def Create(nodePointedTo, neuronPointedTo, weight=0):
	#Creates edge dictionary with given parameters
	edge = {}
	edge['nodePointedTo'] = nodePointedTo
	edge['neuronPointedTo'] = neuronPointedTo
	edge['weight'] = weight

	return edge

def PointToDifferentNeuron(edge,nodePointedTo,neuronPointedTo):
	edge['nodePointedTo'] = nodePointedTo
	edge['neuronPointedTo'] = neuronPointedTo

	return edge

def SetWeight(edge,newWeight):
	edge['weight'] = newWeight

	return edge

def Mutate_Weights(edge,p):
	import random 

	if random.random()<=p:
		newWeight = random.gauss(edge['weight'],.01+edge['weight'])
		edge['weight'] = newWeight

	return edge

def GetNodePointedTo(edge):
	return edge['nodePointedTo']

def GetNeuronPointedTo(edge):
	return edge['neuronPointedTo']

def GetWeight(edge):
	return edge['weight']

def PrintEdge(edge):
	outMsg = '\t\tNode Pointed To: %d, Neuron Pointed To: %d, Weight: %.3f' %(edge['nodePointedTo'], 
										edge['neuronPointedTo'], edge['weight'])
	print outMsg

def Save(edge,f):
	f.write('<')
	f.write(str(edge['nodePointedTo']))
	f.write(',')
	f.write(str(edge['neuronPointedTo']))
	f.write(',')
	f.write(str(edge['weight']))
	f.write(',')
	f.write('>')

def PlotSynapse(edge,posDict,ax,nodeID,neurID):
	import matplotlib as plt
	from matplotlib.path import Path
	import matplotlib.patches as patches
	import math

	#Gets spectific neuron in node pointed to
	toNodeID = edge['nodePointedTo']
	toNeurID = edge['neuronPointedTo']

	#Sets color on grayscale by weight +1==black -1==Gray
	#color = str((1.0-(edge['weight']/2.0+.5))/1.5)

	color = '0'
	#color = '.25'

	#If node points to itself, create loop
	if nodeID==toNodeID and neurID == toNeurID:
		x = posDict[nodeID][neurID][0]
		y = posDict[nodeID][neurID][1]
		#Draws loop
		verts = [(x,y),
				 (x-.25,y),
				 (x,y-.25),
				 (x,y)
					]
		codes = [Path.MOVETO,
				 Path.CURVE4,
				 Path.CURVE4,
				 Path.CURVE4,]
		path = Path(verts,codes)
		patch = patches.PathPatch(path, edgecolor=color,facecolor='none', lw=.75, zorder=3)
		ax.add_patch(patch)
	else:
		#Gets position of to and from neuron
		x1 = posDict[nodeID][neurID][0]
		y1 = posDict[nodeID][neurID][1]
		x2 = posDict[toNodeID][toNeurID][0]
		y2 = posDict[toNodeID][toNeurID][1]

		#Sets relative length of arrow based on 
		#physical distance (helps with actually seeing the arrowhead)
		if abs(x2-x1)<=.3 and abs(y2-y1)<=.2:
			x3 = (x2-x1)*.25
			y3 = (y2-y1)*.05
		else:
			x3 = (x2-x1)*2.0/3.0
			y3 = (y2-y1)*2.0/3.0
		if not(x3==0 and y3==0):
			ax.plot([x1,x2],[y1,y2], lw=.75,color=color,zorder=3)
			ax.arrow(x1,y1,x3,y3,lw=.5,head_width=0.05, head_starts_at_zero=True,
					fc=color,ec=color,zorder=1, overhang=.5)
	return ax

def fillWeightMatrix(edge,neuronPosList,weightMatrix,fromID):
	toID = (edge['nodePointedTo'],edge['neuronPointedTo'])
	fromIndex = neuronPosList.index(fromID)
	toIndex = neuronPosList.index(toID)

	weightMatrix[toIndex,fromIndex] = edge['weight']

	return weightMatrix
	