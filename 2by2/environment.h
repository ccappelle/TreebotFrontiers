#ifndef _ENVIRONMENT_H
#define _ENVIRONMENT_H

#include "object.h"

class ENVIRONMENT
{
private:
	int numObjects;

public:
	OBJECT **objects;

public:
	ENVIRONMENT(char *fileName);
	~ENVIRONMENT(void);
	void Create_In_Simulation(dWorldID world, dSpaceID space);
	void Draw(void);
	OBJECT *Get_Object(int index);
	int Get_NumObjects(void);
};

#endif