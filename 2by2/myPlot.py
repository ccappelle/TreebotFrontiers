import matplotlib as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import math

CIRCLE = 25
SQUARE = 4
def plotCircle(centerX,centerY,radius,ax,color='blue',zorder=20,lineWidth = 2):
	ax = plotPoly(centerX,centerY,radius,ax,CIRCLE,color,zorder=zorder,lineWidth=lineWidth)
	return ax
def plotSquare(centerX,centerY,radius,ax,color='red',zorder=20,lineWidth=2):
	ax = plotPoly(centerX,centerY,radius,ax,SQUARE,color,zorder=zorder,lineWidth=lineWidth)
	return ax
def plotPoly(centerX,centerY,radius,ax,n,color,lineWidth=2,zorder=20):
	radius = float(radius)
	delta = 2.0*math.pi/n
	verts = [(0,0)]*int(n+1)
	codes = [0]*int(n+1)
	x = centerX + radius*math.cos(0)
	y = centerY + radius*math.sin(0)
	verts[0] = (x,y)
	codes[0] = Path.MOVETO
	verts[int(n)] = (x,y)
	codes[int(n)] = Path.CLOSEPOLY
	for i in range(1,int(n)):
		x = centerX + radius*math.cos(delta*float(i))
		y = centerY + radius*math.sin(delta*float(i))
		verts[i] = (x,y)
		codes[i] = Path.LINETO

	path = Path(verts,codes)
	patch = patches.PathPatch(path,facecolor=color,lw=lineWidth,zorder=zorder)
	ax.add_patch(patch)
	return ax

