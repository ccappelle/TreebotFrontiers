SPHERE=0
CUBE = 1

BIG=0
SMALL = 1
def CreateSphere(posVec,radius,sizeType):
	#Create sphere object in one of three positions
	obj = CreateObject(posVec,SPHERE,radius,sizeType)

	return obj

def CreateCube(posVec,length):
	obj = CreateObject(posVec,CUBE, length)
	return obj

def CreateObject(posVec, myType, length,sizeType):
	obj = {}

	obj['length']=length
	obj['type'] = myType
	obj['x']=posVec[0]
	obj['y']=posVec[1]
	obj['z']=posVec[2]
	obj['sizeType'] = sizeType
	return obj

def ChangeType(obj, newType):
	obj['type'] = newType
	return obj

def ChangeLength(obj,newLength):
	obj['length']=newLength

	return obj

def Save(obj,f):

	#Write sphere paramaters out to file
	f.write('(')

	f.write(str(obj['sizeType']))
	f.write(',')

	f.write(str(obj['length']))
	f.write(',')

	f.write(str(obj['x']))
	f.write(',')

	f.write(str(obj['y']))
	f.write(',')

	f.write(str(obj['z']))
	f.write(',')

	f.write(')')
