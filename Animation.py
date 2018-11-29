import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from numpy import sin 
from numpy import cos
from numpy import pi
from RK4method import *
from DoublePendulum import *

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal',autoscale_on=False, xlim=(-2.5,2.5),ylim=(-2.5,2.5))
ax.set_xlabel(r'$x$', fontsize=15)
ax.set_ylabel(r'$y$', fontsize=15)
ax.set_title(r'The Double Pendulum', fontsize=17)
#ax.grid()

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
	return m0, m1, m2,

#perform animation step
#print(DP.GetPath())
Pathm1=DP.GetPath1()
Pathm2=DP.GetPath()

def animate(i):
	m1.set_data(Pathm1[i])
	m2.set_data(Pathm2[i])
	return m0, m1, m2, 

from time import time
I=100
ani=animation.FuncAnimation(fig,animate,frames=2000, interval=I,init_func=init, blit=True, repeat=False)

plt.show()
