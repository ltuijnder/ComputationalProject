#!/usr/bin/env python3
##############################################
## Project DoublePendelum by Lennart & Yens
##############################################
from importlib import reload
import time
import DoublePendulum
from DoublePendulum import *
import poincare_map
from poincare_map import *
import RK4method
from RK4method import *


# have a function that let's you reload modules. Since if a kernel is strated once,
# it then does not reimport the module. Even you you make changes !!!
a=(DoublePendulum,poincare_map,RK4method)
def Reload(iterative_module_tuple):
	for package in iterative_module_tuple:
		reload(package)


#(first segment,second segement)
theta=(pi/2,pi/2)# radians
omega=(0,0)# radians/S
mass=(1,2)# mass
length=(1,1)# length

Pendulum.dt=0.01
#Pendulum.Tmax=

DP=Pendulum(theta,omega,mass,length)
# DP.Solve("RK4")
# plt.plot(DP.PSPath[:,1])
# plt.show()

#### Get State runs

poin=Poincare_map(DP)
E=0.5
t2=0
w2=0
print('t2= '+str(t2))
print('w2= '+str(w2))
State=poin.GetState(E,t2,w2,10**-15)# Very precise !!
print(State)

theta=(State[0],State[1])# radians
omega=(State[2],State[3])# radians/S
DP=Pendulum(theta,omega,mass,length)
print(DP.H0)
DP.Solve("RK4")
DP.ShowPath()
DP.ShowH()

#### Poincaré run
# poin=Poincare_map(DP)

# poin.TimeEstimate(100,10**-10,10)

# print("Started solving... Have some patients")
# start_time = time.time()# Time it
# (points,H_diff,t,error,IterNumber)=poin.Solve(N=100,Precision=10**-10)
# elapsed_time = time.time() - start_time
# print("Elapsed_time= "+"{0:.2f}".format(elapsed_time)+ " seconds")

# #poin.ShowDetailed(points,H_diff,t,IterNumber)
# #poin.ShowErrors(error)
# poin.ShowSingleSolution(points)


##### Multiple state run
#State=np.array([[pi/2,pi/2,0,0],[pi/2,-pi/2,0,0]])
#N=100#np.array()
#Solution=poin.Solve_set(State,N,Precision=10**-6)
#poin.Show_Map(Solution)