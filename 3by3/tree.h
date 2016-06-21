#ifndef _TREE_H
#define _TREE_H

#include "node.h"
#include "fstream"
#include "object.h"
#include "network.h"
#include "environment.h"
using namespace std;

class TREE {

public:
	NODE *root;
	NETWORK *network;
	int numberOfSelfCollisions;
	double distanceFromSegmentsToObject;
	double totalRayLengths;

public:
	TREE(char *treeStructure, char *networkFileName);
	~TREE(void);
	void Add_DistanceFromSegmentsToObject(OBJECT *obj);
	void Add_Self_Collisions(int newSelfCollisions);
	void Add_Sensor_Readings(void);
	void Create_In_Simulation(dWorldID world, dSpaceID space);
	void Deactivate_Sensors(void);
	void Draw(void);
	float Get_Node_Angle(int nodeID);
	float Get_Min_Dist(float *pos);
	void Move(double timer);
	void Send_Results(ofstream *outFile, int timer, ENVIRONMENT *e);
	void Sense(void);

private:
	void Load(char *robotData, int firstLoad);
	int Num_Nodes(void);
	int Num_Leaves(void);
};

#endif
