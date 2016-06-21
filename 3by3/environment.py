import object
root3 = 3.**(.5)
numObjects = 2
X_POS_1 = -4.
X_POS_2 = 4.
Y_POS = 5.0
Z_POS = .5
U_RADIUS = .5
F_RADIUS = 2.5
BIG = 0
SMALL = 1

def CreateUF(myID):
	env={}
	env['myID']=myID
	env['numObjects'] = numObjects
	env[0] = object.CreateSphere([X_POS_1,Y_POS,Z_POS],U_RADIUS, SMALL)
	env[1] = object.CreateSphere([X_POS_2,Y_POS,Z_POS],F_RADIUS, BIG)

	return env
def CreateFF(myID):
	env={}
	env['myID']=myID
	env['numObjects'] = numObjects
	env[0] = object.CreateSphere([X_POS_1,Y_POS,Z_POS],F_RADIUS, BIG)
	env[1] = object.CreateSphere([X_POS_2,Y_POS,Z_POS],F_RADIUS, BIG)

	return env
def CreateUU(myID):
	env={}
	env['myID']=myID
	env['numObjects'] = numObjects
	env[0] = object.CreateSphere([X_POS_1,Y_POS,Z_POS],U_RADIUS, SMALL)
	env[1] = object.CreateSphere([X_POS_2,Y_POS,Z_POS],U_RADIUS, SMALL)

	return env
def CreateFU(myID):
	env={}
	env['myID']=myID
	env['numObjects'] = numObjects
	env[0] = object.CreateSphere([X_POS_1,Y_POS,Z_POS],F_RADIUS, BIG)
	env[1] = object.CreateSphere([X_POS_2,Y_POS,Z_POS],U_RADIUS, SMALL)

	return env

def Create(myID):
	#Designates a new environment with a certain
	#number of shapes (objects)
	env = {}

	env['myID'] = myID

	env['numObjects'] = numObjects

	for i in range(0,numObjects):
		env[i] = object.Create(i)

	return env

def Save(env):
	fileName = 'Data/env' + str(env['myID']) + '.env'

	f = open(fileName, 'w')

	f.write('(')
	f.write(str(env['numObjects']))
	f.write(',')

	for i in range(0,env['numObjects']):
		object.Save(env[i],f)

	f.write(')')

	f.close()

def getEnv(index):
	row = index/3
	col = index%3
	typeL = ''
	sizeL = ''
	typeR = ''
	typeL = ''

	if row==0:
		typeL = '0'
		sizeL = '3.5'
	elif row==1:
		typeL = '1'
		sizeL = '2.0'
	elif row==2:
		typeL = '0'
		sizeL = '0.5'

	if col == 0:
		typeR = '0'
		sizeR = '3.5'
	elif col == 1:
		typeR = '1'
		sizeR = '2.0'
	elif col == 2:
		typeR = '0'
		sizeR = '0.5'

	return '(2,('+typeL+',' +sizeL +',-4.0,5.0,0.5,)('+typeR+',' +sizeR +',4.0,5.0,0.5,))'

#print getEnv(1)
