g++ -DHAVE_CONFIG_H -I. -I../ode-0.13/ode/src  -I../ode-0.13/include -DDRAWSTUFF_TEXTURE_PATH="\"../ode-0.13/drawstuff/textures\"" -DdTRIMESH_ENABLED -DdDOUBLE  -g -O2 -MT node.o -MD -MP -c -o node.o node.cpp

g++ -DHAVE_CONFIG_H -I. -I../ode-0.13/ode/src  -I../ode-0.13/include -DDRAWSTUFF_TEXTURE_PATH="\"../ode-0.13/drawstuff/textures\"" -DdTRIMESH_ENABLED -DdDOUBLE  -g -O2 -MT tree.o -MD -MP -c -o tree.o tree.cpp

g++ -DHAVE_CONFIG_H -I. -I../ode-0.13/ode/src  -I../ode-0.13/include -DDRAWSTUFF_TEXTURE_PATH="\"../ode-0.13/drawstuff/textures\"" -DdTRIMESH_ENABLED -DdDOUBLE  -g -O2 -MT network.o -MD -MP -c -o network.o network.cpp

g++ -DHAVE_CONFIG_H -I. -I../ode-0.13/ode/src  -I../ode-0.13/include -DDRAWSTUFF_TEXTURE_PATH="\"../ode-0.13/drawstuff/textures\"" -DdTRIMESH_ENABLED -DdDOUBLE  -g -O2 -MT object.o -MD -MP -c -o object.o object.cpp

g++ -DHAVE_CONFIG_H -I. -I../ode-0.13/ode/src  -I../ode-0.13/include -DDRAWSTUFF_TEXTURE_PATH="\"../ode-0.13/drawstuff/textures\"" -DdTRIMESH_ENABLED -DdDOUBLE  -g -O2 -MT environment.o -MD -MP -c -o environment.o environment.cpp

g++ -DHAVE_CONFIG_H -I. -I../ode-0.13/ode/src  -I../ode-0.13/include -DDRAWSTUFF_TEXTURE_PATH="\"../ode-0.13/drawstuff/textures\"" -DdTRIMESH_ENABLED -DdDOUBLE  -g -O2 -MT Simulate.o -MD -MP -c -o Simulate.o Simulate.cpp

/bin/sh ../ode-0.13/libtool --tag=CXX   --mode=link g++  -g -O2   -o Simulate Simulate.o synapse.o network.o node.o tree.o object.o environment.o ../ode-0.13/drawstuff/src/libdrawstuff.la ../ode-0.13/ode/src/libode.la -framework OpenGL -framework GLUT  -lm  -lpthread
