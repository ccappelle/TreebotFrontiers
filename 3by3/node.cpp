#ifndef _NODE_CPP
#define _NODE_CPP

#include "stdio.h"
#include "string.h"
#include "math.h"
#include "node.h"
#include "fstream"
#include "environment.h"

#ifdef dDOUBLE
#define dsDrawLine dsDrawLineD
#define dsDrawBox dsDrawBoxD
#define dsDrawSphere dsDrawSphereD
#define dsDrawCylinder dsDrawCylinderD
#define dsDrawCapsule dsDrawCapsuleD
#endif

#define FIXED_JOINT 0
#define HINGE_JOINT 1

using namespace std;

NODE::NODE(char *tokens) {

	//Scans input line and breaks string into children,
	//position, and radius data
	sscanf(tokens,"%d, %lf,%lf,%lf, %lf,%lf,%lf, %lf, %d,%d,%d, %d",	&numChildren,
									&basePosition[0],&basePosition[1],&basePosition[2],
									&tipPosition[0],&tipPosition[1],&tipPosition[2],
									&radius,
									&depth,
									&jointType,
									&nodeID,
									&numNeurons
									);


	//Sets center x,y,z position of current branch in order
	//to create cylinder
	centerPosition[0] = ( basePosition[0] + tipPosition[0] ) / 2.0;
        centerPosition[1] = ( basePosition[1] + tipPosition[1] ) / 2.0;
        centerPosition[2] = ( basePosition[2] + tipPosition[2] ) / 2.0;

    //Gets length of the current branch
	length = sqrt(	pow(tipPosition[0]-basePosition[0],2.0) +
			pow(tipPosition[1]-basePosition[1],2.0) +
			pow(tipPosition[2]-basePosition[2],2.0) );
	

	Deactivate_Sensor();

	//Creates a new node for each child
	children = new NODE*[numChildren];

	//Loops through tokenizing each brach noted by
	//delimeter new nodes for each branch
	for (int c=0;c<numChildren;c++) {
        tokens = strtok(NULL,"(");
		children[c] = new NODE(tokens);
		//sets parent of children to this node
		children[c]->parent = this;
	}

	if(numChildren==0){
		isLeafNode=true;
	}
	else{
		isLeafNode=false;
	}

	//Randomizes color of branch
	for (int i=0;i<3;i++)
		color[i] = ((double)rand()) / RAND_MAX;

	parent = NULL;
}

NODE::~NODE(void) {
	//Destructor method
	//Deletes children nodes for garbage collection
	for (int c=0;c<numChildren;c++) {

		delete children[c];
		children[c] = NULL;
	}

	delete[] children;
	children = NULL;
	parent = NULL;
	

}
void NODE::Activate_Sensor(double *pos){
	//Set the starting position of the ray based on
	// the position of the body
	const dReal *startPos = dBodyGetPosition(body);

	raySensorStartingPoint[0] = startPos[0];
	raySensorStartingPoint[1] = startPos[1];
	raySensorStartingPoint[2] = startPos[2];

	raySensorCollisionPoint[0] = pos[0];
	raySensorCollisionPoint[1] = pos[1];
	raySensorCollisionPoint[2] = pos[2];

	sensorActivated = true;
}
double NODE::Add_Up_Desired_Angles(void) {
	//Adds up the total desired angles of the children
	double total = jointDesiredAngle;

	for (int c=0;c<numChildren;c++)
        	total = total + children[c]->Add_Up_Desired_Angles();

	return total;
}

double NODE::Add_Up_Sensor_Readings(void){
	//Adds up the sensor values from all the leaves 
	//of the tree
	double total = 0.0;

	if( Is_Leaf_Node()){
		double value = Get_Sensor_Reading();
		total = total + value;
	}

	for (int c=0;c<numChildren;c++)
		total = total + children[c]->Add_Up_Sensor_Readings();

	return total;
}

void NODE::Create_In_Simulation(dWorldID world, dSpaceID space, NODE *parent) {
	//Creates node in physical world
	Create_Cylinder(world,space);

	//Creates a ray in each leaf
	if( Is_Leaf_Node())
		Create_Ray(space);

	Create_Joint(world,space,parent);

	for (int c=0;c<numChildren;c++)
		//Create ecah children 
		children[c]->Create_In_Simulation(world,space,this);
}

void NODE::Deactivate_Sensors(void){
	//Deactivate sensors of entire tree
	if( Is_Leaf_Node())
		Deactivate_Sensor();

	for (int c=0;c<numChildren;c++)
		children[c]->Deactivate_Sensors();
}

double NODE::DistanceFromSegmentsToObject(OBJECT *obj){
	//Finds the distance from entire tree to given object
	//adds it up and return it
	const dReal *myPos = dBodyGetPosition(body);
	const dReal *itsPos = dBodyGetPosition(obj->body);

	double dist = 0.0;

	dist = sqrt(pow(myPos[0]-itsPos[0], 2.0) + pow(myPos[1]-itsPos[1],2.0));

	for(int c=0;c<numChildren;c++)
		dist = dist + children[c]->DistanceFromSegmentsToObject(obj);

	return dist;
}

void NODE::Draw(void) {
	//Draw the node in ODE
	dsSetColor (color[0],color[1],color[2]);
	dsSetTexture (DS_WOOD);
	dsDrawCylinder(dBodyGetPosition(body),dBodyGetRotation(body),length,radius);
	dVector3 pos;
	const float delta = 2.0*3.14159/numNeurons;
	const float radius = 0.1;
	
	for(int i=0;i<numNeurons;i++){
		dBodyCopyPosition(body,pos);
		pos[0] = pos[0]+ radius*cos(delta*i);
		pos[1] = pos[1]+ radius*sin(delta*i);
		dsDrawSphere(pos,dBodyGetRotation(body),.075);
	}
	
	//Draw the sensor
	if (sensorActivated)
		Draw_Sensor();

    for (int c=0;c<numChildren;c++)
    	//Draw children
		children[c]->Draw();
}

int NODE::GetNodeID(void){
	return nodeID;
}


float NODE::Get_Min_Dist(float *objPos, float minDist){
	if(isLeafNode){
		const dReal *nodePos = dBodyGetPosition(body);
		return sqrt(pow(objPos[0]-nodePos[0],2.0)+pow(objPos[1]-nodePos[1],2.0)+pow(objPos[2]-nodePos[2],2.0));
	}
	else{
		for(int c=0;c<numChildren;c++){
			float testDist = children[c]->Get_Min_Dist(objPos, minDist);
			if (testDist<minDist){
				minDist = testDist;
			}
		}
	}

	return minDist;
	
}
float NODE::Get_Node_Angle(void){
	return dJointGetHingeAngle(joint);
}


void NODE::Move(double timer, NETWORK *controllerNetwork) {
	//Actuate joint motors to desired position
	if ( jointType != FIXED_JOINT )
		Actuate_Motor(timer, controllerNetwork);

	for (int c=0;c<numChildren;c++)

		children[c]->Move(timer,controllerNetwork);
}

int NODE::Num_Leaves(void){
	//Returns the number of leaf nodes of given tree/subtree
	int numLeaves = Is_Leaf_Node();

	for (int c=0;c<numChildren;c++)
		numLeaves = numLeaves + children[c]->Num_Leaves();

	return numLeaves;
}

int NODE::Num_Nodes(void){
	//Returns number of nodes in tree/subtree
	int numNodes = 1;

	for(int c=0;c<numChildren;c++){
		numNodes = numNodes + children[c]->Num_Nodes();
	}

	return numNodes;
}

void NODE::Sense(NETWORK *controllerNetwork){
	//Prints out sensor data for the tree

	if (Is_Leaf_Node()){
		double value=Get_Sensor_Reading();
		for (int i=1;i<nodeID+1;i++){
			value = value;
		}

		controllerNetwork->Update_Sensor_Value(nodeID,value);
	}

	for(int c=0;c<numChildren;c++)
		children[c]->Sense(controllerNetwork);
}

void NODE::Send_Results(ofstream *outFile, int timer,ENVIRONMENT *e){
	int F = 0;
	int U = 1;
	float MAX_U_DIST = 6.12371;
	if ( isLeafNode ){
		float fitnessResult = 0.0;
		const dReal *nodePos = dBodyGetPosition(body);
		for(int i=0; i<e->Get_NumObjects();i++){
			OBJECT *obj = e->Get_Object(i);
			float *objPos = obj->pos;
			//printf("%f \n", ((objPos[0]-nodePos[0])^2+objPos[1]-nodePos[1]+objPos[2]-nodePos[2]));
			float distance = sqrt(pow(objPos[0]-nodePos[0],2.0)+pow(objPos[1]-nodePos[1],2.0)+pow(objPos[2]-nodePos[2],2.0));
			int objType = obj->Get_Type();
			if (objType==F){
				printf("yep \n");
				fitnessResult = fitnessResult*(distance);
			}
			else{
				fitnessResult = fitnessResult*(MAX_U_DIST/distance);
			}
		}
		(*outFile) << fitnessResult;
		(*outFile) << "\n";
	}
	else{
		for(int c=0; c<numChildren;c++){
			children[c]->Send_Results(outFile,timer,e);
		}
	}

	/*

	if ( jointType == FIXED_JOINT)
		(*outFile) << 0.0;
	else
		(*outFile) << dJointGetHingeAngle(joint);
	(*outFile) << "   ";
	(*outFile) << nodeID;
	(*outFile) << "\n";
	for (int c=0;c<numChildren;c++) {
		children[c]->Send_Results(outFile,timer,e);
	}*/

}

// ------------------------ Private methods -----------------------


void NODE::Actuate_Motor(double timer, NETWORK *controllerNetwork) {
	double desiredPosition;
	//Moves joint towards desired angle
	//double desiredPosition = jointDesiredAngle;
	double modifier = 3.1415/(2.0*(depth+1));
	if (nodeID==0){
		modifier = .666*3.1415;
	}
	desiredPosition = (controllerNetwork->Get_Motor_Neuron_Value(nodeID))*modifier;
	//desiredPosition = -1.1;
	//desiredPosition = -0.974533;
	//desiredPosition =-1.243992;
	//desiredPosition = 3.1415/2.0-.3;
	//desiredPosition = +.666*3.1415;
	//desiredPosition = 0.0;
	
	/*if (nodeID==2)
		desiredPosition = 0.0*modifier;
	else
		desiredPosition = 0.0*modifier;
	*/
	//desiredPosition = -1.456;
	double divider = 4.0;

	/*
	if (timer>.75){
		divider = divider + timer*10.0;
	}*/
	//desiredPosition = -1.5468;
	double currentPosition = dJointGetHingeAngle(joint);
	double desiredVelocity = (desiredPosition - currentPosition)/divider;
	//printf("%f\n", desiredVelocity);
	/*
	if (desiredVelocity<.01 && desiredVelocity>-.01){
		desiredVelocity = 0.0;
	}*/
	dJointSetHingeParam(joint,dParamVel, desiredVelocity );
}

void NODE::Create_Cylinder(dWorldID world, dSpaceID space) {
	//Creates cylinder(branch) 
    dMass m;

    //Sets body ID
    body = dBodyCreate (world);

    //Sets body position to the center of branch
    dBodySetPosition(body,centerPosition[0],centerPosition[1],centerPosition[2]);

    dMatrix3 R; //Rotation matrix

    //Orient rotation matrix along the length of the branch
    dRFromZAxis(R, tipPosition[0] - basePosition[0], tipPosition[1] - basePosition[1], tipPosition[2] - basePosition[2]);

    //Set orientation of the body according to the rotation matrix
	dBodySetRotation(body,R);

	//Set mass and asign it to the body(branch)
    dMassSetSphere (&m,1,radius);
    dMassAdjust (&m,1);
    dBodySetMass (body,&m);

    //Create cylinder geom object
    geom = dCreateCapsule(space,radius,length);

    //Link body and geom objects
    dGeomSetBody(geom,body);

    dGeomSetData(geom,this);
}

void NODE::Create_Joint(dWorldID world, dSpaceID space, NODE *parent) {
	//Creates appropriate joint based on type
	if ( jointType == FIXED_JOINT )

		Create_Joint_Fixed(world,space,parent);
	else
		Create_Joint_Hinge(world,space,parent);
}

void NODE::Create_Joint_Fixed(dWorldID world, dSpaceID space, NODE *parent) {
	joint = dJointCreateFixed(world,0);

	if ( parent == NULL )

		dJointAttach(joint,body,0);

	else
		dJointAttach(joint,body,parent->body);

	dJointSetFixed(joint);
}

void NODE::Create_Joint_Hinge(dWorldID world, dSpaceID space, NODE *parent) {

    joint = dJointCreateHinge(world,0);

    if ( parent == NULL )
		dJointAttach(joint,body,0);
	else
		dJointAttach(joint,body,parent->body);

	dJointSetHingeAnchor(joint,basePosition[0],basePosition[1],basePosition[2]);
	//Turn branch left and right
	dJointSetHingeAxis(joint,0,0,-1);

	//Turn branch up and down
	//dJointSetHingeAxis(joint,1,0,0);
	dJointSetHingeParam(joint,dParamFMax,10000.0);
}

void NODE::Create_Ray(dSpaceID space){
	//Creates a ray with length 10
	ray = dCreateRay(space,10.0);

	//Creates ray at tip of leaf and orient it
	//in direction of branch
	dGeomRaySet(ray, 
				tipPosition[0],tipPosition[1],tipPosition[2],
				tipPosition[0]-basePosition[0],
				tipPosition[1]-tipPosition[1],
				tipPosition[2]-tipPosition[2]);

	//Link ray with body of leaf
	dGeomSetBody(ray,body);

	//Links ray geom ID with this node
	dGeomSetData(ray,this);
}

void NODE::Deactivate_Sensor(void){
	//Turns sensor off
	sensorActivated = false;
}

void NODE::Draw_Sensor(void){
	//Draws line indicating ray
	dsDrawLine(raySensorStartingPoint, 
				raySensorCollisionPoint);
}

double NODE::Get_Sensor_Reading(void){
	double raySensorLength = 10.0;
	//Calculates the distance to first object in 
	//the path of the ray
	if(sensorActivated){
		raySensorLength = sqrt(
					pow(raySensorCollisionPoint[0]-raySensorStartingPoint[0],2.0) +
					pow(raySensorCollisionPoint[1]-raySensorStartingPoint[1],2.0) +
					pow(raySensorCollisionPoint[2]-raySensorStartingPoint[2],2.0) );
	
	}	
	
	return raySensorLength;
}

int NODE::Is_Leaf_Node(void){
	return( numChildren==0);
}

void NODE::Print_Sensor_Values(void){
	//Gets length of ray
	double length = dGeomRayGetLength(ray);
}
#endif
