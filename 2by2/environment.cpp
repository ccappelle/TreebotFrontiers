#ifndef _ENVIRONMENT_CPP
#define _ENVIRONMENT_CPP

#include "stdio.h"

#include "environment.h"

#include "fstream"
using namespace std;

ENVIRONMENT::ENVIRONMENT(char *envStructure){
	//Read in file name of environment
	//ifstream *inFile = new ifstream(fileName);

	//char envData[100000];

	//(*inFile)>> envData;

	//inFile->close();
	//delete inFile;
	//inFile = NULL;

	//Break up enviroment data into tokens
	char *tokens = strtok(envStructure,"(");

	//Assign first number to numObjects
	sscanf(tokens,"%d, ", &numObjects);

	objects = new OBJECT *[numObjects];

	for (int i=0; i<numObjects;i++){
		//Get next token
		tokens = strtok(NULL,"(");
		//Create new object
		objects[i] = new OBJECT(tokens);
	}
}

ENVIRONMENT::~ENVIRONMENT(void){
	for(int i=0; i<numObjects; i++){
		delete objects[i];
		objects[i] = NULL;
	}

	delete[] objects;
	objects = NULL;
}
int ENVIRONMENT::Get_NumObjects(void){
	return numObjects;
}
void ENVIRONMENT::Create_In_Simulation(dWorldID world, dSpaceID space){
	//Creates environment in physics engine
	for (int i=0;i<numObjects;i++){
		if( objects[i]){
			objects[i]->Create_In_Simulation(world,space);
		}
	}
}

void ENVIRONMENT::Draw(void){\
	//Draw environment in Physics Engine
	for(int i=0; i<numObjects;i++){
		if(objects[i]){
			objects[i]->Draw();
		}
	}

}

OBJECT *ENVIRONMENT::Get_Object(int index){
	//Return object of index index
	if(objects[index]){
		return objects[index];
	}
	else
		return NULL;
}

#endif