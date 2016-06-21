#ifndef _TREE_CPP
#define _TREE_CPP

#include "stdio.h"
#include "string.h"

#include "fstream"

#include "tree.h"
#include "node.h"
#include "network.h"
#include "environment.h"

using namespace std;

TREE::TREE(char *treeStructure, char *networkStructure){
//TREE::TREE(const char *fileName, const char *networkFileName) {
	//Read in tree text file
	//ifstream *inFile = new ifstream(fileName);
	//ifstream *networkFile = new ifstream(networkFileName);
	//char robotData[1000000];
	//char networkData[100000];

	//Write data into variable
	//(*inFile) >> robotData;
	//(*networkFile) >> networkData;

	//Garbage collection
	//inFile->close();
	//networkFile->close();
	//delete inFile;
	//delete networkFile;
	//inFile = NULL;
	//networkFile = NULL;

	//Create root token
	char *tokens = strtok(treeStructure,"(");

	//Creates tree from root token
	root = new NODE(tokens);

	//Create network
	char *networkTokens = strtok(networkStructure,",");
	network = new NETWORK(networkTokens);

	//Initialize variables
	numberOfSelfCollisions = 0;
	distanceFromSegmentsToObject = 0.0;
	totalRayLengths = 0.0;
}

TREE::~TREE(void) {
	//Destructor method
	if ( root ) {

		delete root;
		root = NULL;
	}
}

void TREE::Add_DistanceFromSegmentsToObject(OBJECT *obj){
	//Calculate the trees total distance to object
	if(root){
		distanceFromSegmentsToObject = distanceFromSegmentsToObject + 
											root->DistanceFromSegmentsToObject(obj);
	}
}

void TREE::Add_Self_Collisions(int newSelfCollisions){
	//Updates the number of self collisions
	numberOfSelfCollisions = numberOfSelfCollisions + newSelfCollisions;
}

void TREE::Add_Sensor_Readings(void){
	//Updates the values based on sensors
	if(root)
		totalRayLengths = totalRayLengths + root->Add_Up_Sensor_Readings();
}

void TREE::Create_In_Simulation(dWorldID world, dSpaceID space) {
	//Generates cylinders for branches making up the tree
	if ( root )
		root->Create_In_Simulation(world,space,NULL);
}

void TREE::Deactivate_Sensors(void){
	if(root)
		root->Deactivate_Sensors();
}

void TREE::Draw(void) {
	//Draws tree
	if ( root )
		root->Draw();
}

float TREE::Get_Min_Dist(float *pos){
	if (root)
		return root->Get_Min_Dist(pos,10000.0);
	else
		return -1.0;
}

float TREE::Get_Node_Angle(int nodeID){
	if (root){
		return root->Get_Node_Angle();
	}
}


void TREE::Move(double timer) {
	//Actuates joints of tree
	
	if ( root )
		root->Move(timer, network);
}

int TREE::Num_Leaves(void){
	//Returns the number of leaves on the tree
	if(root)
		return root->Num_Leaves();
	else
		return 0;
}

int TREE::Num_Nodes(void){
	//Returns the number of nodes in the tree
	if(root)
		return root->Num_Nodes();
	else
		return 0;
}
void TREE::Send_Results(ofstream *outFile, int timer, ENVIRONMENT *e) {
	//Writes the results out to file
	//double totalSensorReadings = root->Add_Up_Sensor_Readings();
	if(root)
		root->Send_Results(outFile,timer,e);
	//(*outFile) << (totalRayLengths/(float(Num_Leaves())*float(timer)))*
		//			float(1+numberOfSelfCollisions); 
}


void TREE::Sense(void){
	if (root){
		network->Reset_Sensor_Values();
		root->Sense(network);
		network->Reset_Bias();
		network->Update_Rest_Of_Network();
	}
}



#endif
