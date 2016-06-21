#ifndef _Network_CPP
#define _Network_CPP

#include "stdio.h"
#include "string.h"
#include "fstream"
#include "network.h"
#include "math.h"
using namespace std;

	const int SENSOR=1;
	const int MOTOR = 2;
	const int NORMAL = 0;
	const int BIAS = 3;
NETWORK::NETWORK(char *networkTokens){
	char tempStr [1000];
	sscanf(networkTokens,"%d",&numNodes);
	networkTokens = strtok(NULL,",");
	sscanf(networkTokens,"%d",&numNeurons);
	networkTokens = strtok(NULL,",");

	whichNode = new int[numNeurons];
	for(int i=0; i<numNeurons;i++){
		sscanf(networkTokens,"%d",&whichNode[i]);
		networkTokens = strtok(NULL,",");
	}

	neuronType = new int[numNeurons];
	for(int i=0; i<numNeurons;i++){
		sscanf(networkTokens,"%d",&neuronType[i]);
		networkTokens = strtok(NULL,",");
	}

	weightMatrix = new double[numNeurons*numNeurons];
	for(int i=0;i<numNeurons;i++){
		for(int j=0;j<numNeurons;j++){
			sscanf(networkTokens,"%lf",&weightMatrix[i*numNeurons+j]);
			networkTokens = strtok(NULL,",");
		}
	}
	
	neuronValues = new double[numNeurons];
	for( int i=0; i<numNeurons; i++){
		neuronValues[i] = 0.0;
	}

}

NETWORK::~NETWORK(void){

}
void NETWORK::Reset_Sensor_Values(){
	for(int i=0; i<numNeurons;i++){
		if(neuronType[i]==SENSOR){
			neuronValues[i]=0.0;
		}
	}
}

void NETWORK::Update_Rest_Of_Network(){
	double sum = 0.0;
	double updatedNeuronValues[numNeurons];
	for(int i=0;i<numNeurons;i++){
		for(int j=0;j<numNeurons;j++){
			sum = sum + weightMatrix[i*numNeurons+j]*neuronValues[j];
		}
		sum = tanh(sum);
		updatedNeuronValues[i]=sum;
		sum = 0.0;
	}

	for(int i=0;i<numNeurons;i++){
		neuronValues[i]=updatedNeuronValues[i];
	}
}

void NETWORK::Print_Adjacency_Matrix(){
	for(int i=0;i<numNeurons;i++){
		for(int j=0;j<numNeurons;j++){
			printf("%f ", weightMatrix[i*numNeurons+j]);
		}
		printf("%n");
	}
}
void NETWORK::Update_Sensor_Value(int nodeID, double value){
	for(int i=0; i<numNeurons;i++){
		if(neuronType[i]==SENSOR && whichNode[i]==nodeID){
			neuronValues[i]= value;
			break;
		}
	}
}
void NETWORK::Reset_Bias(){
	for(int i=0; i<numNeurons; i++){
		if(neuronType[i]==BIAS){
			neuronValues[i] = 1.0;
		}
	}
}

void NETWORK::Print_Neuron_Values(){
	for(int i=0;i<numNeurons;i++){
		printf(" %lf, ",neuronValues[i]);
	}
	printf("\n");
}

double NETWORK::Get_Motor_Neuron_Value(int nodeID){
	for(int i=0; i<numNeurons;i++){
		if(neuronType[i]==MOTOR && whichNode[i]==nodeID){
			return neuronValues[i];
		}
	}
	return 0.0;
}
#endif