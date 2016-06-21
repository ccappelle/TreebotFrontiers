#ifndef _OBJECT_CPP
#define _OBJECT_CPP

#include "stdio.h"
#include "object.h"

#ifdef dDOUBLE
#define dsDrawSphere dsDrawSphereD
#endif

OBJECT::OBJECT(char *tokens){
	//Sets radius of object and position based on incoming tokens
	sscanf(tokens, "%d, %f, %f, %f, %f, ", &type, &length,&pos[0],&pos[1],&pos[2]);
}

OBJECT::~OBJECT(void){

}

void OBJECT::Create_In_Simulation(dWorldID world, dSpaceID space){
	//Create sphere in ODE
	//set mass
	dMass m;

	//Create body
	body = dBodyCreate(world);

	//Set position
	dBodySetPosition(body,pos[0],pos[1],pos[2]);

	//Adjust and set mass
	dMassSetSphere(&m,1,length);
	dMassAdjust(&m,1);
	dBodySetMass(body,&m);

	//Create geom object
	geom = dCreateSphere(space,length);

	//Link geom and body
	dGeomSetBody(geom,body);

	//Removes collision detection
	dBodyDisable(body);
}

void OBJECT::Draw(void){
	//Draw sphere 
	dsSetColor(1,1,1);
	dsDrawSphere(dBodyGetPosition(body),dBodyGetRotation(body),length);
}

int OBJECT::Get_Type(void){
	return type;
}

float *OBJECT::Get_Pos(void){
	return pos;
}
#endif