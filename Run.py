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
poin=Poincare_map(DP)
# DP.Solve("RK4")
# plt.plot(DP.PSPath[:,1])
# plt.show()

#### Plot H

# N=10000
# E=0.05
# PSPath=np.zeros((N,4))
# t1=0
# t2=0
# w2=0
# PSPath[:,0]=np.full(N,t1)
# PSPath[:,1]=np.full(N,t2)
# PSPath[:,2]=np.linspace(-50,50,N)
# PSPath[:,3]=np.full(N,w2)

# #plt.plot(PSPath[:,2],DP.GetH(PSPath)-E)
# #print("Minimum w1= "+str(PSPath[:,2][np.argmin(DP.GetH(PSPath))]))
# #plt.grid()
# #plt.show()

# State=poin.GetState(E,t2,w2,10**-15)
# print(State)

#### First attempt to make a FULL poincaré-map

#To see the 2 Harmonic solutions, Keep it to a low Energy. Let's choose E=0.05

E=0.05
precisionE=10**-15

# See Local_saves.txt, for a nice exploration of what the fuck happens. 

t2=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) # Inside the converging region.
w2=np.array([0.3872412,0.33,0.34,0.35,0.36,0,0.05,0.1,0.12,0.15,0.2,0.25,0.27,0.30,0.3175]) # limiting case. ( the conversion zone afbakenen)
leftright=np.full_like(w2,1)
# Let's now get a good screen converionn to conversion bottom and some nice thing in between

States=np.zeros((len(t2),4))
for i in range(len(t2)):
	#States[i]=poin.GetState(E,t2[i],w2[i],leftright[i],precisionE)
	States[i]=poin.GetState(E,t2[i],w2[i],leftright[i],precisionE)

N=100#np.array([100,100,20,20,10,100,100,100])
Solution,PS_Solution=poin.Solve_set(States,N,Precision=10**-10)
poin.Show_Map(Solution)
# #print(PS_Solution)
# H=np.zeros((len(Solution),len(Solution[0])))
# H[0]=DP.GetH(PS_Solution[0])


# number_random=5
# t2=np.zeros(number_random)
# w2=np.zeros(number_random)
# for i in range(number_random):
# 	randomindex=np.random.randint(0,len(Solution[0]))
# 	print(randomindex)
# 	randpoint=Solution[0,randomindex]
# 	t2[i]=randpoint[0]
# 	w2[i]=randpoint[1]
# 	print("Random point "+str(i)+ " is =" +np.str(randpoint))
# point20=Solution[0,20]
# print(point20)# Should be [-0.05855579  0.212657  ]
# t2=np.array([0,point20[0]])
# w2=np.array([0.2,point20[1]])
# leftright=np.array([1,0])
# States=np.zeros((len(t2),4))
# for i in range(len(t2)):
# 	States[i]=poin.GetState(E,t2[i],w2[i],leftright[i],precisionE)

# # Look at the difference in the states:
# print("PhaseSpace at point t2,w2=[-0.05855579,0.212657], Started from t2,w2=0,O.2:")
# print(PS_Solution[0,20])# [ 1.67936639e-13 -5.85557912e-02 -1.13296193e-01  2.12657002e-01]
# print("PhaseSpace at point t2,w2=[-0.05855579,0.212657], Started from t2,w2=[-0.05855579,0.212657]")
# print(States[1]) # [ 0.         -0.05855579 -0.1697617   0.212657  ]

# The p1 is different !! but why ?? I believe that the original one is correct and that thus GetState a mistakes does
# Let's look who is correct !!
# Ok after evaluation... We got the following. Both indeed are on the good energy. But the problem is that, there are always
# 2 solutions for w1. that result in the same energy. :///. Now when we DO GetState. we always take the most negative one.
# But it seems when let the system evolve that it can switch sides for the right solution.
# That's why when we did the random thing, the evolved state was sometime the most negative solution, from the two. Thus having the same result.
# But other times it was the other one. resulting in a different field.

# So the problem we now face is, There are 2 different independent poincaré map at the same energy !! but it's not clear how to distinguish the 2
# So how do we choose the correct p1? 

# N=100#np.array([100,100,20,20,10,100,100,100])
# Solution,PS_Solution=poin.Solve_set(States,N,Precision=10**-10)
# poin.Show_Map(Solution)
# H=np.zeros((len(Solution),len(Solution[0])))
# for i in range(2):
# 	H[i]=DP.GetH(PS_Solution[i])

#### Get State runs

# poin=Poincare_map(DP)
# E=0.5
# t2=0
# w2=0
# print('t2= '+str(t2))
# print('w2= '+str(w2))
# State=poin.GetState(E,t2,w2,10**-15)# Very precise !!
# print(State)

# theta=(State[0],State[1])# radians
# omega=(State[2],State[3])# radians/S
# DP=Pendulum(theta,omega,mass,length)
# print(DP.H0)
# DP.Solve("RK4")
# DP.ShowPath()
# DP.ShowH()

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