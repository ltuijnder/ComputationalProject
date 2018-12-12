import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from numpy import sin 
from numpy import cos
from numpy import pi
from RK4method import *
from DoublePendulum import *
style.use('seaborn')


theta=(pi/2,pi)# radians
omega=(0,0)# radians/S
mass=(1,2)# mass
length=(1,1)# length



Pendulum.Tmax=60
DP=Pendulum(theta,omega,mass,length)
DP.Solve("RK4")

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal',autoscale_on=False, xlim=(-2.5,2.5),ylim=(-2.5,2.5))
ax.set_xlabel(r'$x$', fontsize=15)
ax.set_ylabel(r'$y$', fontsize=15)
ax.set_title(r'The Double Pendulum', fontsize=17)



Pathm1_not60fps=DP.GetPath1()
Pathm2_not60fps=DP.GetPath()

def Convertfps(array_OldFPS,dt,fpsNew):
	fpsOld=dt**-1# So we need to get this fpsOld -> fpsNew
	if fpsOld<fpsNew:
		print("Fps is lower than 60 fps. It will be played back at this rate")
		return fpsOld
	MaxFrameOld=len(array_OldFPS)
	Tmax=MaxFrameOld/fpsOld
	MaxFrameNew=Tmax*fpsNew
	FrameIndexOld=FrameNumberOld(fpsOld,fpsNew,np.arange(MaxFrameNew))
	array_NewFPS=array_OldFPS[FrameIndexOld]
	return array_NewFPS

def FrameNumberOld(FpsOld,FpsNew,FrameNumberNew):
	conver_factor=FpsOld/FpsNew
	if type(FrameNumberNew)==np.ndarray:# Generally we want FrameNumberNew to be an array which doens't know int()
		return (FrameNumberNew*conver_factor).astype(int)
	else:
		return int(FrameNumberNew*conver_factor)


output=Convertfps(Pathm1_not60fps,Pendulum.dt,60)# Convert to 60 fps
if type(output)== int:
	Pathm1=Pathm1_not60fps
	Pathm2=Pathm2_not60fps
	fps=output
	I=fps**-1*1000# I=Pendulum.dt*1000=tijd per frame in ms
	Frames=int(fps*Pendulum.Tmax)#  amount of frames=fps*total time
else:
	Pathm1=output
	Pathm2=Convertfps(Pathm2_not60fps,Pendulum.dt,60)
	fps=60
	I=fps**-1*1000# I=Pendulum.dt*1000=tijd per frame in ms
	Frames=int(fps*Pendulum.Tmax)#  amount of frames=fps*total time

ln1, =ax.plot((0,Pathm1[0][0]),(0,Pathm1[0][1]),lw=2, color='xkcd:green',animated=True)
ln2, =ax.plot((Pathm1[0][0],Pathm2[0][0]),(Pathm1[0][1],Pathm2[0][1]),lw=2, color='xkcd:red',animated=True)
m0, = ax.plot(0,0,'*',markersize=20, color= 'xkcd:gold',animated=True)
m1, =ax.plot([],[], 'o-',markersize=10, color= 'xkcd:green',animated=True)
m2, = ax.plot([],[], 'o-',markersize=10, color='xkcd:red',animated=True)
H_text=ax.text(0.75,0.95, '',transform=ax.transAxes)
t_text=ax.text(0.75,0.90,'',transform=ax.transAxes)



#define an initial state for the animation:
def init():
	ln1.set_data([],[])
	ln2.set_data([],[])
	m0.set_data(0,0)
	m1.set_data([],[])
	m2.set_data([],[])
	return ln1, ln2, m0, m1, m2,
	
	
#perform animation step
def animate(i):
	ln1.set_data((0,Pathm1[i][0]),(0,Pathm1[i][1]))
	ln2.set_data((Pathm1[i][0],Pathm2[i][0]),(Pathm1[i][1],Pathm2[i][1]))
	m1.set_data(Pathm1[i])
	m2.set_data(Pathm2[i])
	return ln1, ln2, m0, m1, m2,

# Big Problem !! FuncAnimation, also doensn't play it back correctly !!. It does it in 100 seconds while it should be 60 seconds
# I think it has to do, that the frame rate of computer screens ( at least my laptop) is locked to 60 FPS, the frame have to wait 
# on the refresshing of my computer. 
# My solution is to convert to 60 fps right away to function animation.

# fps=60#Pendulum.dt**-1
# print('fps='+str(fps))
# I=fps**-1*1000# I=Pendulum.dt*1000=tijd per frame in ms
# Frames=int(fps*Pendulum.Tmax)#  amount of frames=fps*total time
# print("Frames="+str(Frames))
ani=animation.FuncAnimation(fig,animate,frames=Frames, interval=I,init_func=init, blit=True, repeat=False)




plt.show()