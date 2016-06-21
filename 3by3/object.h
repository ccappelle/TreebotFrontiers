#ifndef _OBJECT_H
#define _OBJECT_H

#include <ode/ode.h>
#include <drawstuff/drawstuff.h>

class OBJECT{

public:
	float pos[3];
	float length;
	int type;
	dBodyID body;
	dGeomID geom;

public:
	OBJECT(char *tokens);
	~OBJECT(void);
	void Create_In_Simulation(dWorldID world, dSpaceID space);
	void Draw(void);
	int Get_Type(void);
	float *Get_Pos();
};

#endif

