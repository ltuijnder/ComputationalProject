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

theta2=(pi/2,3.1415)
omega2=(0,0)
mass2=(1,2)
length2=(1,1)

Pendulum.Tmax=60
DP=Pendulum(theta,omega,mass,length)
DP2=Pendulum(theta2,omega2,mass2,length2)
DP.Solve("RK4")
DP2.Solve('RK4')

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal',autoscale_on=False, xlim=(-2.5,2.5),ylim=(-2.5,2.5))
ax.set_xlabel(r'$x$', fontsize=15)
ax.set_ylabel(r'$y$', fontsize=15)
ax.set_title(r'The Double Pendulum: Small differences in initial conditions', fontsize=17)

Pathm1=DP.GetPath1()
Pathm2=DP.GetPath()

Path2m1=DP2.GetPath1()
Path2m2=DP2.GetPath()

ln1, =ax.plot((0,Pathm1[0][0]),(0,Pathm1[0][1]),lw=2, color='xkcd:green',animated=True)
ln2, =ax.plot((Pathm1[0][0],Pathm2[0][0]),(Pathm1[0][1],Pathm2[0][1]),lw=2, color='xkcd:red',animated=True)
m0, = ax.plot(0,0,'*',markersize=20, color= 'xkcd:gold',animated=True)
m1, =ax.plot([],[], 'o-',markersize=10, color= 'xkcd:green',animated=True)
m2, = ax.plot([],[], 'o-',markersize=10, color='xkcd:red',animated=True)
H_text=ax.text(0.75,0.95, '',transform=ax.transAxes)
t_text=ax.text(0.75,0.90,'',transform=ax.transAxes)

line1, =ax.plot((0,Path2m1[0][0]),(0,Path2m1[0][1]),lw=2, color='xkcd:leaf green',animated=True)
line2, =ax.plot((Path2m1[0][0],Path2m2[0][0]),(Path2m1[0][1],Path2m2[0][1]),lw=2, color='xkcd:reddish orange',animated=True)
M1, =ax.plot([],[],'o-',markersize=10, color='xkcd:leaf green',animated=True)
M2, =ax.plot([],[],'o-',markersize=10, color='xkcd:reddish orange',animated=True)


#define an initial state for the animation:
def init():
	ln1.set_data([],[])
	ln2.set_data([],[])
	line1.set_data([],[])
	line2.set_data([],[])
	m0.set_data(0,0)
	m1.set_data([],[])
	m2.set_data([],[])
	M1.set_data([],[])
	M2.set_data([],[])
	return ln1, ln2, line1, line2, m0, m1, m2, M1, M2,
	
	
#perform animation step
def animate(i):
	ln1.set_data((0,Pathm1[i][0]),(0,Pathm1[i][1]))
	ln2.set_data((Pathm1[i][0],Pathm2[i][0]),(Pathm1[i][1],Pathm2[i][1]))
	m1.set_data(Pathm1[i])
	m2.set_data(Pathm2[i])
	line1.set_data((0,Path2m1[i][0]),(0,Path2m1[i][1]))
	line2.set_data((Path2m1[i][0],Path2m2[i][0]),(Path2m1[i][1],Path2m2[i][1]))
	M1.set_data(Path2m1[i])
	M2.set_data(Path2m2[i])
	return ln1, ln2, m0, m1, m2,line1, line2, M1, M2,

fps=Pendulum.dt**-1
print('fps='+str(fps))
I=fps**-1*1000# I=Pendulum.dt*1000=tijd per frame in ms
Frames=int(fps*Pendulum.Tmax)#  amount of frames=fps*total time
print("Frames="+str(Frames))
ani=animation.FuncAnimation(fig,animate,frames=Frames, interval=I,init_func=init, blit=True, repeat=False)



plt.show()
