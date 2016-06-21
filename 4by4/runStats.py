import numpy as np
import scipy.stats as stats
import json

def gensToTarget(File):
	count = [0.0, 0.0]
	mySum = [0.0, 0.0]
	for date in File:
		if File[date]['style'] == 'target':
			envOrder = File[date]['envOrder']

			if (envOrder == [0,1,2,3]):
				index = 0
			else:
				index = 1
			mySum[index] += File[date]['gensToTargetTotal']
			count[index] += 1.

	print mySum[0]/count[0], mySum[1]/count[1]

def uTest(x1,x2):
	u, p = stats.mannwhitneyu(x1,x2)
	return u, p
def avgLast(File):
	index = 0
	mySum = [0,0]
	count = [0, 0]
	for date in File:
		envOrder = File[date]['envOrder']

		if (envOrder == [0,1,2,3]):
			index = 0
		else:
			index = 1

		if File[date]['popSize'] == 50:
			fitness = File[date]['fitness']
			mySum[index] += float(fitness[-1])
			count[index] += 1

	print count,mySum, mySum[0]/float(count[0]), mySum[1]/float(count[1])
def loadData(File):
	#plt.figure()
	#plt.suptitle(title)
	index = 0
	gensToTarget= np.zeros((50,4))
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
#print gensToTargetArray[count[index],:,index]
		count[index] = count[index]+1	
	print np.divide(np.sum(gensToTarget,axis=0),50)
	
	return gensToTarget


with open('Results/Modular_1/results.json','r') as f:
	M1_File = json.load(f)
with open('Results/Modular_2/results.json','r') as f:
	M2_File = json.load(f)
with open('Results/Modular_3/results.json','r') as f:
	M3_File = json.load(f)

with open('Results/Mod-NM1/results.json','r') as f:
	MNM1_File = json.load(f)
with open('Results/Mod-NM2/results.json','r') as f:
	MNM2_File = json.load(f)

with open('Results/Nonmodular_1/results.json','r') as f:
	NM1_File = json.load(f)
with open('Results/Nonmodular_2/results.json','r') as f:
	NM2_File = json.load(f)


print gensToTarget(M1_File)
print gensToTarget(M2_File)
print gensToTarget(M3_File)
print gensToTarget(MNM1_File)
print gensToTarget(MNM2_File)
print gensToTarget(NM1_File)
print gensToTarget(NM2_File)

#modularData = loadData(M_File)
#modular2Data = loadData(M2_File)
#mnmData = loadData(MNM_File)
#nmData = loadData(NM1_File)
#m3Data = loadData(M3_File)


#for i in range(4):
#	print i, uTest(modularData[:,i],mnmData[:,i])
#	print i, uTest(modularData[:,i],nmData[:,i])


