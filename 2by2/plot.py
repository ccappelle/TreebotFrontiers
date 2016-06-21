import matplotlib.pyplot as plt
import numpy as np
import sys
import json
from datetime import datetime
import matplotlib.patches as mpatches
import scipy.stats as stats
from matplotlib.collections import PathCollection
N = 400
colors = ['b','purple','g','r','orange']
width = .15

def runStats(data1,data2):
	U, p = stats.mannwhitneyu(data1,data2)
	print U,p
def plotFit(File,title,order):
	#plt.figure()
	#plt.suptitle(title)
	index = 0
	gensToTarget= np.zeros((50,4))
	gensToTargetArray = np.zeros((50,4,4))
	gens = ()
	gensInEnv = ((),(),(),())
	count = np.zeros(4)
	for date in File:
		target = File[date]['targetError']
		envOrder = File[date]['envOrder']

		if (envOrder==[0,1,2,3]):
			index = 0
		elif (envOrder==[0,3,1,2]):
			index= 2

		if (target == .1):
			pass
		elif (target == .085):
			index = index + 1
		#elif (target == .07):
		#	index1 = 2



		gensToTarget[count[index],index] = File[date]['gensToTargetTotal']
		gensToTargetArray[count[index],:,index] = File[date]['gensToTargetArray']
		count[index] = count[index]+1

	avg = np.zeros(4)
	std = np.zeros(4)
	avgArray = np.zeros((4,4))
	for i in range(4):
		currArray = gensToTarget[:,i]
		vals = np.where(currArray>1000)[0]
		currArray = currArray[currArray<1000]

		for j in range(4):
		 	envArray = gensToTargetArray[:,j,i]
		 	if len(vals)>0:
		 		envArray = np.delete(envArray,vals)
		 	
		 	avgArray[j,i] = np.divide(np.sum(envArray),len(envArray))
		
		avg[i] = np.divide(np.sum(currArray),len(currArray))
		std[i] = stats.sem(currArray)
	print avg
	#avgArray = np.sum(gensToTargetArray,axis=0)
	#avgArray = np.divide(avgArray,50.0)

	for i in range(4):
		#print i, gensToTarget[:,i]
		#print avg[i],std[i]
		bottom = 0.0
		for j in range(4):
			if (j==3):
				plt.bar(i+width*order,avgArray[j,i],width,bottom=bottom,alpha=((j+1)/4.0),color=colors[order],yerr=std[i],ecolor='k')
			else:
				plt.bar(i+width*order,avgArray[j,i],width,bottom=bottom,alpha=((j+1)/4.0),color=colors[order])
			bottom = bottom + avgArray[j,i]

		#plt.bar(i+width*(order),avgArray[0,i],width,alpha=.3,color=colors[order])
		#plt.bar(i+width*(order),avgArray[1,i],width,bottom=avgArray[0,i],alpha=.5,color=colors[order])
		#plt.bar(i+width*(order),avgArray[2,i],width,bottom=avgArray[1,i],alpha=.75,color=colors[order])
		#plt.bar(i+width*(order),avgArray[3,i],width,bottom=avgArray[2,i],alpha=1,color=colors[order],yerr=std[i],ecolor='k')
		
		#plt.plot(np.zeros(50)+i+width*(order+.5),gensToTarget[:,i],'o',color=colors[order],)

	return gensToTarget


with open('Results/Modular/results.json','r') as f:
	M_File = json.load(f)

with open('Results/Nonmodular_1/results.json','r') as f:
	NM1_File = json.load(f)

with open('Results/ModBod-NMBrain/results.json','r') as f:
	MNM_File = json.load(f)

with open('Results/Modular_2/results.json','r') as f:
	M2_File = json.load(f)

with open('Results/Modular_3/results.json','r') as f:
	M3_File = json.load(f)


modularData = plotFit(M_File, "M",0)
modular2Data = plotFit(M2_File,"M2",1)
mnmData = plotFit(MNM_File,"MNM",3)
nmData = plotFit(NM1_File, 'NM',4)
m3Data = plotFit(M3_File,"M3",2)


Labels = ['M1','M2','M3','M-NM','NM']
red_Patch = mpatches.Patch(color='red')
blue_Patch = mpatches.Patch(color='b')
orange_Patch = mpatches.Patch(color='orange')
purple_Patch = mpatches.Patch(color='purple')
green_Patch = mpatches.Patch(color='green')

plt.legend([blue_Patch,purple_Patch,green_Patch,red_Patch,orange_Patch],Labels)
plt.ylim(ymin=0.0)
plt.xticks((np.arange(4)+2.*width),('\n$O_1,0.1$','\n$O_1,0.085$','\n$O_2,0.1$','\n$O_2,0.085$'))
plt.ylabel('Generations')
plt.xlabel('Env. Order, Target Error')
plt.title('Average Generations to Target Error')
plt.show()

#print '----statistics-------'
#for i in range(4):
#	data1 = modularData[:,i]
#	data2 = nmData[:,i]
#	runStats(data1,data2)


#plotFit(NM2_File, 'NM_2-No_Add_Ons')
#plt.show()