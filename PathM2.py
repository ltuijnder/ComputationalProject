import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from numpy import sin 
from numpy import cos
from numpy import pi
from RK4method import *
from DoublePendulum import *

theta=(pi/2,pi/2)# radians
omega=(0,0)# radians/S
mass=(1,1)# mass
length=(1.99,0.01)# length



Pendulum.Tmax=60
DP=Pendulum(theta,omega,mass,length)
DP.Solve("RK4")
DP.ShowPath()
