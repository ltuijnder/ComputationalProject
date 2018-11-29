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
theta=(pi/100,pi/100)# radians
omega=(0,0)# radians/S
mass=(1,2)# mass
length=(1,1)# length

DP=Pendulum(theta,omega,mass,length)
poin=Poincare_map(DP)

#poin.TimeEstimate(1000,10**-10,10)

#print("Started solving... Have some patients")
#start_time = time.time()
#(points,H_diff,t,error,IterNumber)=poin.Solve(N=10,Precision=10**-10)
#elapsed_time = time.time() - start_time
#print("Elapsed_time= "+"{0:.2f}".format(elapsed_time)+ " seconds")

#poin.ShowDetailed(points,H_diff,t,IterNumber)
#poin.ShowErrors(error)
#poin.ShowSingleSolution(points)
#poin.ShowDetailed(points,H_diff,t,IterNumber)

State=np.array([[pi/2,pi/2,0,0],[pi/2,-pi/2,0,0]])
N=100#np.array()
Solution=poin.Solve_set(State,N,Precision=10**-6)
poin.Show_Map(Solution)