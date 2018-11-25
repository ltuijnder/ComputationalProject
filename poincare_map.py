import numpy as np
import RK4method as RK4
from DoublePendulum import Pendulum

class Poincare_map:

	def __init__(self,DP,E=-1):
		self.DP=DP
		self.E=self.DP.H0
		#self.Tsign=sign(self.DP.t1)

	def Show(self,t1,w1):
		pass

	def Sort(self,points):
		pass

	def NextPoint(self):
		U_0=(self.DP.t1,self.DP.t2,self.DP.w1,self.DP.w2)
		U_i,U_j,t=RK4.RK4_signchange(Pendulum.dt,RK4.F,U_0,self.DP.Peninfo)
		self.DP.SetPhaseSpace(U_j)
		# return the closed point
		if abs(U_i[0]-0)<abs(U_j[0]-0):# if U_i is closer to zero then U_j then return U_i
			return U_i,t
		return U_j,t

	def Points(self):# Come up with a better 
		N=100
		points=np.zeros((N,2))
		H_diff=np.zeros(N)
		time=np.zeros(N)
		for i in range(N):
			U,t=self.NextPoint()
			points[i]=(U[1],U[3])# (t2,w2)
			H_diff[i]=self.E-self.DP.GetH()
			time[i]=t# This returns the time it needed to search
		return (points,H_diff,time)

		




