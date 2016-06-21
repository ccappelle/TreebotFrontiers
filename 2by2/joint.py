import random
import math

FIXED_JOINT = 0
HINGE_JOINT = 1

def Create(jointType,minAngle,maxAngle):
	#Creates a hinge with a random desired angle between
	#specified range
	joint = {}

	joint['type'] = jointType

	joint['minAngle'] = minAngle

	joint['maxAngle'] = maxAngle

	joint['desiredAngle'] = 0

	if ( joint['type'] == HINGE_JOINT ):
		Randomize_Desired_Angle(joint)

	return joint 

def SetJointType(joint,jointType):
	joint['type'] = jointType
	return joint

def Is_Hinge_Joint(joint):

	return ( joint['type'] == HINGE_JOINT ) 

def Perturb_Desired_Angle(joint,age):
	#Move desired angle a random bit
	joint['desiredAngle'] = joint['desiredAngle'] + random.gauss(0,math.fabs(joint['desiredAngle']))

	#Keep angle within limits
	if(joint['desiredAngle']<joint['minAngle']):
		joint['desiredAngle'] = joint['minAngle']
	if joint['desiredAngle']>joint['maxAngle']:
		joint['desiredAngle'] = joint['maxAngle']

def Randomize_Desired_Angle(joint):
	#Initialize random desired angle in joint
	joint['desiredAngle'] = random.uniform(joint['minAngle'],joint['maxAngle'])

def JointToString(joint):
	return str(joint['type'])+','
	
def Save(joint,f):
	#Writes the joint to the file with its desired angle
	f.write( str(joint['type']) )
        f.write( "," )

	#f.write( str(joint['desiredAngle']) )
     #   f.write( "," )

def Set_Desired_Angle(joint,desiredAngle):
	joint['desiredAngle'] = desiredAngle