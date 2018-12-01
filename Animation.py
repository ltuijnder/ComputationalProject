import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from numpy import sin 
from numpy import cos
from numpy import pi
from RK4method import *
from DoublePendulum import *

DP=Pendulum()
DP.Solve("RK4")

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal',autoscale_on=False, xlim=(-2.5,2.5),ylim=(-2.5,2.5))
ax.set_xlabel(r'$x$', fontsize=15)
ax.set_ylabel(r'$y$', fontsize=15)
ax.set_title(r'The Double Pendulum', fontsize=17)
#ax.grid()

Pathm1=DP.GetPath1()
Pathm2=DP.GetPath()

ln1, =ax.plot((0,Pathm1[0][0]),(0,Pathm1[0][1]),lw=2, color='xkcd:green')
ln2, =ax.plot((Pathm1[0][0],Pathm2[0][0]),(Pathm1[0][1],Pathm2[0][1]),lw=2, color='xkcd:red')
m0, = ax.plot(0,0,'o-',lw=2)
m1, =ax.plot([],[], 'o-',lw=2)
m2, = ax.plot([],[], 'o-',lw=2 )
H_text=ax.text(0.75,0.95, '',transform=ax.transAxes)
t_text=ax.text(0.75,0.90,'',transform=ax.transAxes)
#define an initial state for the animation:

def init():
	m0.set_data(0,0)
	m1.set_data([],[])
	m2.set_data([],[])
	ln1.set_data([],[])
	ln2.set_data([],[])
	return m0, m1, m2, ln1, ln2,

#perform animation step
#print(DP.GetPath())


def animate(i):
	m1.set_data(Pathm1[i])
	m2.set_data(Pathm2[i])
	ln1.set_data((0,Pathm1[i][0]),(0,Pathm1[i][1]))
	ln2.set_data((Pathm1[i][0],Pathm2[i][0]),(Pathm1[i][1],Pathm2[i][1]))
	return m0, m1, m2, ln1, ln2,

from time import time
I=1000*Pendulum.dt
ani=animation.FuncAnimation(fig,animate,frames=2000, interval=I,init_func=init, blit=True, repeat=False)

plt.show()
# Before you read the comments, I want to say that your method indeed works good if we don't have caluclated DP.Solve('RK4')
# in advance, however it's far more effiecient that we do it this way. So to change to that, I have put some comments that will help you on how to change this

### First comment:
# What you could do, to improve the performance is call "DP.GetPath"& "DP.GetPath1", BEFORE animate(i), see comments
# And in animate(i) you keep the m1.set_data(Pathm1[i]) and m2.set_data(Pathm2[i]).
# This is ok, since Pathm1 & Pathm2 are defined outside the function.

### Second comment:
# Don't call NextStep() since The path is already callculated. Namely when we called DP.Solve('RK4') then DP.PSPath was already filled.
# This way you can already call GetPath1 & GetPath() before animate(i)

# So what happens when you call DP.NextStep()? Well now you callculate further where DP.Solve('RK4') left off.
# Since Tmax=60, you will now callculate the points for 60.01,60.02,...seconds and so forth, BUT we want the points with 0,0.01,0.02...seconds
# And there for we don't need to do DP.NextStep(), That is also what we said we wanted to do, That we first just solve whole the thing, and then animate
# What you now do is again calculate at each step. 

### Third comment: 
# This actually is a follow up on the second comment. Because you calculate the points 60.01,60.02,... seconds with NextStep().
# For this reason DP.GetH() will give you back the hamiltonian on the time points 60.01,60.02,...
# So I guess to solve this you also just call GetH(PSPath) before the function animate, and change accordingly.
