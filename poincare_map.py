import numpy as np
import RK4method as RK4
from DoublePendulum import Pendulum
import matplotlib.pyplot as plt
import time

class Poincare_map:

	def __init__(self,DP,E=-1):
		self.Default=DP # THis just to save the initial condition just so we can load the original one again
		self.DP=DP # This is the Dubble pendulum we will be changing
		self.E=self.DP.H0 # Remember the starting E
		#self.Tsign=sign(self.DP.t1)

	def ShowDetailed(self,Points,H_diff,Time_diff,Error):
		fig=plt.figure(figsize=(10,10))
		plt.subplot(2,2,1)
		plt.plot(H_diff)
		plt.title("Difference from stating E")
		plt.ylabel("Energy in joule")
		plt.xlabel("Number of points")
		plt.subplot(2,2,2)
		plt.plot(Time_diff)
		plt.ylabel("Time in seconds")
		plt.xlabel("Point number")
		plt.title("Real time elapsed until next point")
		(xmin,xmax)=plt.xlim()
		(ymin,ymax)=plt.ylim()
		plt.text(0,0.965*ymax,"Total time:"+"{0:.2f}".format(np.sum(Time_diff))+' seconds')
		plt.subplot(2,2,3)
		plt.scatter(Points[:,0],Points[:,1])
		plt.ylabel(r'$\omega_2$')
		plt.xlabel(r'$\theta_2$')
		plt.title("Poincaré map")
		plt.subplot(2,2,4)
		plt.plot(Error[:,1])
		plt.title("Error in theta 2")
		plt.show()

	def ShowErrors(self,Error):
		fig=plt.figure(figsize=(10,10))
		plt.subplot(2,2,1)
		plt.plot(Error[:,0])
		plt.title("Error in theta 1")
		plt.subplot(2,2,2)
		plt.plot(Error[:,1])
		plt.title("Error in theta 2")
		plt.subplot(2,2,3)
		plt.plot(Error[:,2])
		plt.title("Error in omega 1")
		plt.subplot(2,2,4)
		plt.plot(Error[:,3])
		plt.title("Error in omega 2")
		plt.show()

	def ShowPoincareMap(self,Points):
		fig=plt.figure(figsize=(10,10))
		plt.scatter(Points[:,0],Points[:,1])
		plt.ylabel(r'$\omega_2$',fontsize=15)
		plt.xlabel(r'$\theta_2$',fontsize=15)
		plt.title("Poincaré map",fontsize=18)
		plt.grid()
		plt.tick_params(axis='both', labelsize=15)
		plt.show()

	def NextPoint(self):
		U_0=(self.DP.t1,self.DP.t2,self.DP.w1,self.DP.w2)
		U_i,U_j,t=RK4.RK4_signchange(Pendulum.dt,RK4.F,U_0,self.DP.Peninfo)# transition U's
		self.DP.SetPhaseSpace(U_j)
		error=U_j-U_i		# return the closed point
		if abs(U_i[0]-0)<abs(U_j[0]-0):# if U_i is closer to zero then U_j then return U_i
			return U_i,t,error
		return U_j,t,error

	def Solve(self,N=100,State=0):# Come up with a better 
		if type(State) is int:
			self.DP=self.Default
			self.E=self.Default.H0
		else:
			self.DP.SetPhaseSpace(State)# set DP To the state we want.
			self.E=self.DP.GetH()
		points=np.zeros((N,2))
		H_diff=np.zeros(N)
		Error=np.zeros((N,4))
		time=np.zeros(N)
		for i in range(N):
			U,t,error=self.NextPoint()
			points[i]=(U[1],U[3])# (t2,w2)
			H_diff[i]=self.E-self.DP.GetH()
			Error[i]=(error)
			time[i]=t# This returns the time it needed to search
		return (points,H_diff,time,Error)

	def TimeEstimate(self,N,mode=100,State=0): # This is just for fun
		# Take 5 time samples.
		print("Started with estimating time, This time estimated may also take a time")
		start_time = time.time()
		self.Solve(mode,State)
		elapsed_time = time.time() - start_time
		#print(elapsed_time)
		estimate=N/mode*elapsed_time
		print("Estimated time to calculate: "+"{0:.2f}".format(estimate)+" seconds")

		




