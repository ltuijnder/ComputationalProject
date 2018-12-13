import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from numpy import sin 
from numpy import cos
from numpy import pi
from RK4method import *
from DoublePendulum import *

theta=(pi/2,pi)# radians
omega=(0,0)# radians/S
mass=(1,2)# mass
length=(1,1)# length



Pendulum.Tmax=60
DP=Pendulum(theta,omega,mass,length)
DP.Solve("RK4")
DP.ShowPath()
DP.ShowH()
