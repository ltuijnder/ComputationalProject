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

	def ShowDetailed(self,Points,H_diff,Time_diff,Numbers):
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
		plt.plot(Numbers)
		plt.title("Number of iterations with the Bisection method")
		plt.xlabel("Point number")
		plt.ylabel("Number of iterations")
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

	def ShowSingleSolution(self,Points):# This is only to plot single solution, The more general one is "Show_Map"
		fig=plt.figure(figsize=(10,10))
		plt.scatter(Points[:,0],Points[:,1])
		plt.ylabel(r'$\omega_2$',fontsize=15)
		plt.xlabel(r'$\theta_2$',fontsize=15)
		plt.title("Poincaré map",fontsize=18)
		plt.grid()
		plt.tick_params(axis='both', labelsize=15)
		plt.show()

	def NextPoint(self,Precision):
		U_0=(self.DP.t1,self.DP.t2,self.DP.w1,self.DP.w2)
		U_i,U_j,t=RK4.RK4_signchange(Pendulum.dt,RK4.F,U_0,self.DP.Peninfo)# transition U's
		U_i,U_j,itternumber,Extratime=self.CloseIn(U_i,U_j,Precision)# Close the gap between the U's
		t+=Extratime# When closing in we moved "Extratime" forward in time
		self.DP.SetPhaseSpace(U_j) # Set the state after the transition
		error=U_j-U_i		# Give the difference between the states
		if abs(U_i[0]-0)<abs(U_j[0]-0):# if return the U_i where theta1 is closed to 0
			return U_i,t,error,itternumber
		return U_j,t,error,itternumber

	def Bisection(self,U_a,U_b,dt):# Define it such that it can be used in reverse
		self.DP.SetPhaseSpace(U_a)# Set DP to be in the state of U_a
		U_c=self.DP.GetNextStep(dt)# Calculate new point with half the dt
		sign_a=np.sign(U_a[0])# sign of t1 
		sign_c=np.sign(U_c[0])
		if sign_a==sign_c:
			return U_c,U_b,0 # U_c is the new point U_a # Point A did not advanced so we don't add time
		else:
			return U_a,U_c,dt # U_c is the new point U_b # Point A advanced so we update the time

	def CloseIn(self,U_i,U_j,Threshold):
		MaxError=np.max(abs(U_i-U_j))
		number=0# Just to keep some statistics
		dt=Pendulum.dt
		Extratime=0# Keep track how much time we moved forward when we close in
		while MaxError>Threshold:
			dt/=2# Go half size !!! important to make go preciser
			U_i,U_j,t=self.Bisection(U_i,U_j,dt)
			MaxError=np.max(abs(U_i-U_j))
			number+=1
			Extratime+=t# Keep track how much time we moved forward when we close in
		return U_i,U_j,number,Extratime

	def Solve(self,N=100,Precision=0.01,State=0): 
		if type(State) is int: # When no state is given (aka State=0), We use the default State
			self.DP=self.Default # Second purpose of this is to RESET the self.DP and self.E. Since if you would call Solve again you want to have the same result and not go further in time
			self.E=self.Default.H0
		else:
			self.DP.SetPhaseSpace(State)# set DP To the state we want.
			self.E=self.DP.GetH()
		points=np.zeros((N,2))# These hold the X,Y for the points to scatter
		H_diff=np.zeros(N) # This holds how much we deviate from the initial H. Can be used for stop condtion
		Error=np.zeros((N,4)) # This holds the difference between the 2 PhaseSpace points on which the transition happens
		time=np.zeros(N) # This measures the time between the events
		IterNumber=np.zeros(N) # This Holds how many bisection itteration we had to do to get the desired precision
		for i in range(N):
			U,t,error,number=self.NextPoint(Precision)# Calculate the next point. 
			points[i]=(U[1],U[3])# (t2,w2) 
			H_diff[i]=self.E-self.DP.GetH()
			Error[i]=(error)
			time[i]=t# This returns the time it needed to search
			IterNumber[i]=number
		return (points,H_diff,time,Error,IterNumber)

	def Solve_set(self,States,N=100,Precision=0.01):
		N_states=len(States)
		if type(N) is int:# Why this complex? Well so that N can be more general.
			N=np.full(N_states,N)
		elif len(N)!=len(States):
			print("Error N and States need to be the same size. len(N)= "+str(len(N))+", len(States)= "+str(len(States)))
			return
		Solution=np.zeros((N_states,np.max(N),2))# Create a 3 Dimensional array. Dimension 1=Are the solution of the States,Dimension 2=The individual points, Dimension 3=X and Y value of the point
		# Note in the case that N is not the same every where, the excess point in that array will be zero. Note this is not optimal but much easier
		for i in range(N_states):
			points=self.Solve(N[i],Precision,States[i])[0]# Take the zeroth element or, aka only points
			Solution[i,:len(points)]=points # Set The i'th state, Then from this i'th state reduce it's length to that of points, such that we can equal.
		return Solution

	def Show_Map(self,Solution):# Maybe add a flag as parameter?
		fig=plt.figure(figsize=(10,10))
		plt.ylabel(r'$\omega_2$',fontsize=15)
		plt.xlabel(r'$\theta_2$',fontsize=15)
		plt.title("Poincaré map",fontsize=18)
		plt.grid()
		plt.tick_params(axis='both', labelsize=15)
		for i in range(len(Solution)):
			plt.scatter(Solution[i,:,0],Solution[i,:,1])
		plt.show()

	def GetState(self,E,t2,w2,Threshold): # Given E,t2,w2, it gives back w1 (we assume t1=0)
		w1lower=0 # This state will result in the lowest possible energy given the t2 and w2
		if self.DP.GetH(np.array([[0,t2,w1lower,w2]]))>E: # If the Energy is already higher then the Energy of the state we want. Well there is no hope then. Since there is already to much enery contained in t2,W2
			print("ERROR!!!: The state you are looking for doesn't exist, since t2,w2 already contain to much Energy")
			return np.array([0,0,0,0])
		w1upper=-20# Set the upperlimit of w1 to be 20 rad/sec. -> This itself is an extreme upperlimit, State above this E, have no interest to us.
		DiffE=self.DP.GetH(np.array([[0,t2,w1upper,w2]]))-self.DP.GetH(np.array([[0,t2,w1lower,w2]]))
		w1middle,E_middle=0,0# init w1middle and E_middle # maybe unnecesary in python but that's my habit from C/C++
		while DiffE>Threshold:
			w1middle=(w1upper+w1lower)/2
			E_middle=self.DP.GetH(np.array([[0,t2,w1middle,w2]]))
			if E_middle-E>0: # Meaning E_middle is above the wanted E. Thus w1upper get's replaced by middle now  
				w1upper=w1middle  
			else: # The middle energy is lower then the wanted E, So we move the lower bound up.
				w1lower=w1middle
			DiffE=self.DP.GetH(np.array([[0,t2,w1upper,w2]]))-self.DP.GetH(np.array([[0,t2,w1lower,w2]]))# again now calculate the difference
		if abs(self.DP.GetH(np.array([[0,t2,w1upper,w2]]))-E)<abs(self.DP.GetH(np.array([[0,t2,w1lower,w2]]))-E): # Return the state which is closest to the wanted energy
			return np.array([0,t2,w1upper,w2])
		else:
			return np.array([0,t2,w1lower,w2])

	def TimeEstimate(self,N,Precision,mode=100,State=0): # This is just for fun
		# Take 5 time samples.
		print("Started with estimating time, This time estimated may also take a time")
		start_time = time.time()
		self.Solve(mode,Precision,State)
		elapsed_time = time.time() - start_time
		#print(elapsed_time)
		estimate=N/mode*elapsed_time
		print("Estimated time to calculate: "+"{0:.2f}".format(estimate)+" seconds")

		




