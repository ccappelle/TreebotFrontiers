#ifndef _NETWORK_H
#define _NETWORK_H

#include <ode/ode.h>
#include <drawstuff/drawstuff.h>
#include "object.h"

class NETWORK{
private:
	int numNodes;
	int numNeurons;
	int *whichNode;
	double *weightMatrix;
	int *neuronType;
	double *neuronValues;


public:
	NETWORK(char *networkData);
	~NETWORK(void);
	void Reset_Sensor_Values(void);
	void Print_Neuron_Values(void);
	void Print_Adjacency_Matrix(void);
	void Reset_Bias(void);
	void Update_Sensor_Value(int nodeID, double value);
	void Update_Rest_Of_Network(void);
	double Get_Motor_Neuron_Value(int nodeID);

};


#endif