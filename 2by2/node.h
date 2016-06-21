#ifndef _NODE_H
#define _NODE_H

#include <ode/ode.h>
#include <drawstuff/drawstuff.h>
#include "object.h"
#include "network.h"
#include "fstream"
#include "environment.h"

using namespace std;

class NODE {

public: 
	NODE *parent;

private:
	
	int numChildren;
	NODE **children;
	int numNeurons;
	int nodeID;
	int isLeafNode;
	
	//x,y,z positions of a given branch
	double basePosition[3];
	double centerPosition[3];
	double tipPosition[3];

	//radius and length for branch
	double radius;
	double length;

	//Joint variables
	int jointType;
	double jointDesiredAngle;
	double jointCurrentAngle;
	double currentVelocity;

	int depth;

	//ID variables for ODE
	dBodyID body;
	dGeomID geom;
	dGeomID ray;
	dJointID joint;

	//Color of branch
	double color[3];

	int sensorActivated;

	//Ray sensor positioning arrays
	double raySensorStartingPoint[3];
	double raySensorCollisionPoint[3];

public:

	NODE(char *tokens);
	~NODE(void);
	void Activate_Sensor(double *pos);
	double Add_Up_Desired_Angles(void);
	double Add_Up_Sensor_Readings(void);
	void Create_In_Simulation(dWorldID world, dSpaceID space, NODE *parent);
	void Deactivate_Sensors(void);
	double DistanceFromSegmentsToObject(OBJECT *obj);
	void Draw(void);
	int GetNodeID(void);
	float Get_Node_Angle(void);
	float Get_Min_Dist(float *pos, float minDist);
	void Move(double timer, NETWORK *controllerNetwork);
	int Num_Leaves(void);
	int Num_Nodes(void);
	void Sense(NETWORK *controllerNetwork);
	void Send_Results(ofstream *outfile, int timer,ENVIRONMENT *e);

private:
	void Actuate_Motor(double timer, NETWORK *controllerNetwork);
	void Create_Cylinder(dWorldID world, dSpaceID space);
	void Create_Joint(dWorldID world, dSpaceID space, NODE *parent);
    void Create_Joint_Fixed(dWorldID world, dSpaceID space, NODE *parent);
    void Create_Joint_Hinge(dWorldID world, dSpaceID space, NODE *parent);
    void Create_Ray(dSpaceID space);
    void Deactivate_Sensor(void);
    void Draw_Sensor(void);
    double Get_Sensor_Reading(void);
    int Is_Leaf_Node(void);
    void Print_Sensor_Values(void);
};

#endif
