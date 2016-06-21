#include <ode/ode.h>
#include <drawstuff/drawstuff.h>
#include <iostream>
#include "texturepath.h"
#include "time.h"
#include "tree.h"
#include "environment.h"

#include "fstream"
#include "stdio.h"
#include "string.h"

#include <cmath>
using namespace std;

static dWorldID world;
static dSpaceID space;
static dJointGroupID contactgroup;

TREE *t;

ENVIRONMENT *e;

static dGeomID ground;

int timer;

int useGraphics = true;
bool SEND_RESULT;

char treeFileName[500];
char networkFileName[500];
char envFileName[500];
char tempFileName[500];
char velocityFileName[500];
char tempVelocityFileName[500];
char outFileName[500];

int evaluationTime;
int pause;
float U_MIN_DIST;
float U_MAX_DIST;

float F_MIN_DIST;
float F_MAX_DIST;

float NORMALIZER;
const int U = 1;
const int F = 0;
float output = 0.0;
float result = 0.0;
float totalVelocity = 0.0;
float vel_normalize = 0.;
float last_num_counted = 1.0;//10.0;
void Delete_File(char *fileName) {
	//Deletes file
	remove(fileName);
}
void Collect_Results(){
	float Normalizer = 0.0;
	float alpha = .5;
	output = 0.0;
	for(int i=0; i<e->Get_NumObjects();i++){
		OBJECT *currObj = e->Get_Object(i);
		float *pos = currObj->Get_Pos();
		float dist = t->Get_Min_Dist(pos);
		
		if (currObj->Get_Type()== F){
			if(dist>F_MAX_DIST){
				output = output + alpha;
			}
			else if (dist<F_MIN_DIST){
				output = output+0;
			}
			else
			{
				output = output + (alpha)*abs(dist-F_MIN_DIST)/(F_MAX_DIST-F_MIN_DIST);
			}
			Normalizer = Normalizer + alpha;
			
		}
		else{
			if(dist>U_MAX_DIST){
				output =output + 0.0;
			}
			else if (dist<U_MIN_DIST){
				output = output + alpha;
			}
			else
			{
				output = output + (1.0-alpha)*abs(U_MAX_DIST-dist)/(U_MAX_DIST-U_MIN_DIST);
			}		
			Normalizer = Normalizer + (1.0-alpha);
		}
		/*
		if (currObj->Get_Type()== F){
			tempOutput = abs(dist-MIN_DIST)/NORMALIZER;
			if (tempOutput>output){
				output = tempOutput;
			}
		}
		else{
			tempOutput = abs(MAX_DIST-dist)/NORMALIZER;
			if(tempOutput>output){
				output = tempOutput;
			}
		}*/
	}

	output = output/Normalizer;
	result = result + output;
}
void Send_Results(void) {
	//Sends result to a text file
	/*
	ofstream *outFile = new ofstream(tempFileName);
	ofstream *velocityFile = new ofstream(tempVelocityFileName);
	*/

	result = result/last_num_counted;
	//temp = output;
	//char command[100];
	printf("%f\n", result);
	/*
	(*outFile) << result;
	(*outFile) << "\n";

	outFile->close();
	delete outFile;
	outFile = NULL;*/

	
	//Moves data from temp File to specific tree file
   	//sprintf(command,"mv %s %s",tempFileName,outFileName);

   	//system(command);
}

void Terminate(void) {
	//Ends the simulation
	Delete_File(treeFileName);
	Delete_File(networkFileName);
	if (SEND_RESULT){
		Send_Results();	
	}
	else{
		//printf("%f \n",t->Get_Node_Angle(0));
	}
	exit(0);
}

int RayCollidesWithSphere(dGeomID o1, dGeomID o2){
	//Returns true (1) if there is a collision between a ray and sphere
	int o1IsSphere = dGeomGetClass(o1)==0;
	int o1IsRay    = dGeomGetClass(o1)==5;

	int o2IsSphere = dGeomGetClass(o2)==0;
	int o2IsRay    = dGeomGetClass(o2)==5;

	return (o1IsSphere && o2IsRay) || (o1IsRay && o2IsSphere);
}

int CylinderCollidesWithCylinder(dGeomID o1, dGeomID o2){
	//Returns 1 if there is a collision between cylinders (branches)
	int o1IsCylinder = dGeomGetClass(o2)==2;
	int o2IsCylinder = dGeomGetClass(o1)==2;

	int bothObjectsAreCylinders = o1IsCylinder && o2IsCylinder;

	return bothObjectsAreCylinders;
}

void Trigger_Sensor(dGeomID o1, dGeomID o2){
	//Between collision objects activate sensor inside node which
	//has the sensor
	dContact contact;

	int n = dCollide(o1,o2,1,&contact.geom,sizeof(dContact));

	if(n>0){
		NODE *nodeContainingSensor;

		if (dGeomGetClass(o1)==5)
			nodeContainingSensor = (NODE*)dGeomGetData(o1);
		else
			nodeContainingSensor = (NODE*)dGeomGetData(o2);

		nodeContainingSensor->Activate_Sensor(contact.geom.pos);
		nodeContainingSensor = NULL;
	}
}

int Parent_And_Child(dGeomID o1, dGeomID o2){
	//Returns 1 if given objects have parent-child relationship
	NODE *node1 = (NODE*)dGeomGetData(o1);
	NODE *node2 = (NODE*)dGeomGetData(o2);

	int OneIsParentOfTwo = (node2->parent) && (node2->parent==node1);
	int TwoIsParentOfOne = (node1->parent) && (node1->parent==node2);

	return OneIsParentOfTwo || TwoIsParentOfOne;
}

int Siblings(dGeomID o1, dGeomID o2){
	//Returns 1 if given objects have sibling relationship
	NODE *node1 = (NODE*)dGeomGetData(o1);
	NODE *node2 = (NODE*)dGeomGetData(o2);

	return ( node1->parent && node2-> parent && node1->parent == node2->parent);
}

void Resolve_Self_Collision(dGeomID o1, dGeomID o2){
	//Ignore collisions between parent and siblings
	if( Parent_And_Child(o1,o2))
		return;
	if( Siblings(o1,o2))
		return;

	const int N=10;
	dContact contact[N];
	int n = dCollide(o1,o2,10,&contact[0].geom,sizeof(dContact));

	//for each possible contact point set the following parameters
	if (n>0){
		for (int i=0; i<n; i++){
			contact[i].surface.mode = dContactSlip1 | dContactSlip2 | dContactApprox1;
			contact[i].surface.mu = dInfinity;
			contact[i].surface.slip1 = 0.1;
			contact[i].surface.slip2 = 0.1;
			dJointID c = dJointCreateContact(world,contactgroup,&contact[i]);
			dJointAttach(c,dGeomGetBody(contact[i].geom.g1),dGeomGetBody(contact[i].geom.g2));
		}
	}
}
static void nearCallback (void *data, dGeomID o1, dGeomID o2)
{
	//Collision detection
	//If ray and sphere turn on sensor
	//If cylinders proceed with designated actions
	if( RayCollidesWithSphere(o1,o2) )
		Trigger_Sensor(o1,o2);
	if( CylinderCollidesWithCylinder(o1,o2) )
		Resolve_Self_Collision(o1,o2);
	
}


static void start()
{
  //Assocate data required for accessing ODE from current thread
  dAllocateODEDataForThread(dAllocateMaskAll);

  //Sets camera
  static float xyz[3] = {0.0f,-1.817f,4.000f};
  static float hpr[3] = {90.0f,-35.0000f,-0.0000f};
  dsSetViewpoint (xyz,hpr);
  printf ("Welcome.\n");
}


// called when a key pressed

static void command (int cmd)
{
	switch (cmd) {
  		case 'a': case 'A':
    			break;
    	}

}

void SimulateForOneTimeStep(int pause) {
	if ( !pause ) {
		//Runs tree for a time step
		
	  	dSpaceCollide (space,0,&nearCallback);

	  	dJointGroupEmpty(contactgroup);
		t->Sense();
		t->Move(timer/double(evaluationTime));
		//t->Add_DistanceFromSegmentsToObject(e->Get_Object(0));
	  	//Step forward one timestep
		dWorldStep (world,.085);

		//Removes collisions

		//t->Add_Sensor_Readings();

		timer++;
		/*if(evaluationTime-timer<10.0){
			Collect_Results();
		}*/
	}

	if ( useGraphics ){
		//If graphics are on draw
		t->Draw();
		e->Draw();
	}
	if(evaluationTime-timer<last_num_counted){
		Collect_Results();
	}
	//Run simulation until timer is reached
	if ( timer==evaluationTime )
		Terminate();

	if(!pause)
		t->Deactivate_Sensors();
}

static void simLoop (int pause) {
	//Runs simulation
	pause = false;
	SimulateForOneTimeStep(pause);
}

void Initialize_Environment(ENVIRONMENT *e){
	//Creates environment in ODE
	e->Create_In_Simulation(world,space);
}

void Initialize_Robot(TREE *t) {
	//Creates thee in ODE
	t->Create_In_Simulation(world,space);
}

void Initialize_World(dsFunctions *fn) {
	//Preps draw stuff
        fn->version = DS_VERSION;
        fn->start = &start;
        fn->step = &simLoop;
        fn->command = &command;
        fn->stop = 0;
        fn->path_to_textures = DRAWSTUFF_TEXTURE_PATH;

    //Set up ODE
	dInitODE2(0);
	world = dWorldCreate();
	space = dHashSpaceCreate (0);
	contactgroup = dJointGroupCreate (0);
	dWorldSetGravity (world,0,0,-0.5);
	ground = dCreatePlane (space,0,0,1,0);
}

void SimulateWithGraphics(int argc, char **argv, int windowHeight, int windowWidth, dsFunctions fn) {
	//Simulates the robot with graphics
	dsSimulationLoop (argc,argv,windowHeight,windowWidth,&fn);
}

void SimulateWithoutGraphics(void) {
	//Simulates without graphics
	while ( 1 )
		SimulateForOneTimeStep(pause);
}

int main (int argc, char **argv) {
	useGraphics = atoi(argv[1]);
	// Initialize the simulation.

	dsFunctions fn;

	Initialize_World(&fn);

	//Creates folder structure for result files
	char treeStructure[50000];
	char networkStructure[50000];
	char environmentStructure[50000];
	if (useGraphics == 1){
		SEND_RESULT = false;
		sprintf(treeFileName,"Data/tree%s.txt",argv[2]);
		sprintf(networkFileName,"Data/network%s.txt",argv[2]);
    	//sprintf(tempFileName,"Data/temp%s.txt",argv[1]);
		//sprintf(outFileName,"Data/results%s_%s.txt",argv[1],argv[2]);
		sprintf(envFileName,"Data/env%s.env",argv[3]);
		evaluationTime = atoi(argv[4]);

		ifstream *treeFile = new ifstream(treeFileName);
		ifstream *networkFile = new ifstream(networkFileName);
		ifstream *envFile = new ifstream(envFileName);

		//Write data into variable
		(*treeFile) >> treeStructure;
		(*networkFile) >> networkStructure;
		(*envFile) >> environmentStructure;

		//Garbage collection
		treeFile->close();
		networkFile->close();
		envFile->close();
		delete treeFile;
		delete networkFile;
		delete envFile;
		treeFile = NULL;
		networkFile = NULL;
		envFile = NULL;


	}
	else{
		SEND_RESULT = true;
		std::cin >> treeStructure;
		std::cin >> networkStructure;
		std::cin >> environmentStructure;
		std::cin >> evaluationTime;
		std::cin >> F_MIN_DIST;
		std::cin >> F_MAX_DIST;
		std::cin >> U_MIN_DIST;
		std::cin >> U_MAX_DIST;
	}


	/*if(argc>5){
		SEND_RESULT = true;
		F_MIN_DIST = atof(argv[5]);
		F_MAX_DIST = atof(argv[6]);
		U_MIN_DIST = atof(argv[7]);
		U_MAX_DIST = atof(argv[8]);
	}
	else{
		SEND_RESULT = false;
	}*/
	srand(time(NULL));	
	/*
	ifstream *MinMaxFile = new ifstream("Data/minmax.data");
	char distData[100];
	(*MinMaxFile) >> distData;
	MinMaxFile->close();
	delete MinMaxFile;
	MinMaxFile = NULL;

	sscanf(distData,"%f, %f",&MIN_DIST,&MAX_DIST);
	*/

	//Create tree
	//t = new TREE(treeFileName,networkFileName);
	t = new TREE(treeStructure, networkStructure);
	//Create environment
	e = new ENVIRONMENT(environmentStructure);

	//Set up robot
	Initialize_Robot(t);
	Initialize_Environment(e);

	timer = 0;
	output = 0.0;


	//Loop and draw
	if ( useGraphics )
		SimulateWithGraphics(argc,argv,700,700,fn);
	else
		SimulateWithoutGraphics();


}

