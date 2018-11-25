#!/usr/bin/env python3
##############################################
## Project DoublePendelum by Lennart & Yens
##############################################
from importlib import reload
import DoublePendulum
from DoublePendulum import *
import poincare_map
from poincare_map import *
import RK4method
from RK4method import *


# have a function that let's you reload modules. Since if a kernel is strated once,
# it then does not reimport the module. Even you you make changes !!!
a=(DoublePendulum,poincare_map,RK4method)
b=(poincare_map,)
def Reload(iterative_module_tuple):
	for package in iterative_module_tuple:
		reload(package)


#(first segment,second segement)
theta=(pi/2,0)# radians
omega=(0,0)# radians/S
mass=(1,2)# mass
length=(1,1)# length

DP=Pendulum(theta,omega,mass,length)
DP.Solve('RK4')
# plt.plot(DP.PSPath[:,0])
# plt.show()
#DP.ShowPath()
#DP.ShowH()

# poin=Poincare_map(DP)

# dt=0.01
# U_0=(pi/2,0,0,0)
# Peninfo=(9.81,1,2,1,1)
# U_i,U_j=RK4_signchange(dt,F,U_0,Peninfo)
# print(U_i)
# print(U_j)

DP=Pendulum(theta,omega,mass,length)
poin=Poincare_map(DP)
(points,H_diff,time)=poin.Points()
#print(H_diff)
plt.plot(H_diff)
plt.show()
plt.plot(time)
print("Total time:"+str(np.sum(time))+' seconds')
plt.show()
plt.scatter(points[:,0],points[:,1])
plt.show()


