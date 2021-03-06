#!/usr/bin/env python3
##############################################
## Project DoublePendulum by Lennart & Yens
##############################################

import numpy as np 
from matplotlib import style
from numpy import sin 
from numpy import cos
from numpy import pi
from RK4method import *




def ThetatoXY(t1,t2,l1,l2):
    x1=l1*cos(t1)
    y1=l1*sin(t1)
    x2=x1+l2*cos(t2)
    y2=y1+l2*sin(t2)
    return x2,y2
def ThetatoXY1(t1,t2,l1,l2):
    x1=l1*cos(t1)
    y1=l1*sin(t1)
    x2=x1+l2*cos(t2)
    y2=y1+l2*sin(t2)
    return x1,y1

class Pendulum:
	g=9.81
	Tmax=60
	dt=0.01

	def __init__(self,angle=(pi/2,pi),omega=(0,0),mass=(1,1),length=(1,1)):
		self.t1=angle[0] # in rad
		self.t2=angle[1] # in rad
		self.w1=omega[0] # in rad/s
		self.w2=omega[1] # in rad/s
		self.m1=mass[0] # in Kg
		self.m2=mass[1] # in Kg
		self.l1=length[0] # in meter
		self.l2=length[1] # in meter
		self.MinE=-Pendulum.g*(self.l1*(self.m1+self.m2)+self.l2*self.m2)
		self.Peninfo=(Pendulum.g,self.m1,self.m2,self.l1,self.l2)
		self.H0=self.GetH()
		self.time=0
		self.PSPath=np.array([[self.t1,self.t2,self.w1,self.w2]])# Phase space path

	def GetThetaOmega(self):
		return np.array([[self.t1,self.w1],[self.t2,self.w2]])

	def GetXY(self):
		x1=self.l1*cos(self.t1)
		y1=self.l1*sin(self.t1)
		x2=x1+self.l2*cos(self.t2)
		y2=y1+self.l2*sin(self.t2)
		return np.array([[x1,y1],[x2,y2]])

	def NextStep(self):
		self.time+=Pendulum.dt
		dt=Pendulum.dt
		U=(self.t1,self.t2,self.w1,self.w2)
		Unext=U+F1(U,dt,F,self.Peninfo)/6+2/6*(F2(U,dt,F,self.Peninfo)+F3(U,dt,F,self.Peninfo))+F4(U,dt,F,self.Peninfo)/6
		(self.t1,self.t2,self.w1,self.w2)=Unext
		self.PSPath=np.concatenate((self.PSPath,[Unext]))

	def GetNextStep(self,dt):
		U=(self.t1,self.t2,self.w1,self.w2)
		Unext=U+F1(U,dt,F,self.Peninfo)/6+2/6*(F2(U,dt,F,self.Peninfo)+F3(U,dt,F,self.Peninfo))+F4(U,dt,F,self.Peninfo)/6
		return Unext

	def SetPhaseSpace(self,U):
		self.t1=U[0]
		self.t2=U[1]
		self.w1=U[2]
		self.w2=U[3]
		self.PSPath=np.concatenate((self.PSPath,np.array([U])))
		#self.H0=self.GetH()# we will also be resseting H0

	def Solve(self,method):
		U_0=(self.t1,self.t2,self.w1,self.w2)
		if method=='RK4':
			t,U=RK4(Pendulum.dt,Pendulum.Tmax,F,U_0,self.Peninfo)
		elif method=='Euler':
			t,U=euler(Pendulum.dt,Pendulum.Tmax,F,U_0,self.Peninfo)
		(self.t1,self.t2,self.w1,self.w2)=U[-1]
		self.time+=t[-1]
		self.PSPath=np.concatenate((self.PSPath[:-1],U))# Everything except the last one since this is the first element of U

	def ShowPath(self):
		path=self.GetPath()
		plt.ylim([-2.5,2.5])
		plt.xlim([-2.5,2.5])
		plt.grid()
		plt.plot(path[:,0],path[:,1])
		plt.show()

	def GetPath(self):
		x2,y2=ThetatoXY(self.PSPath[:,0],self.PSPath[:,1],self.l1,self.l2)
		Path=np.zeros((len(self.PSPath),2))
		Path[:,0]=y2
		Path[:,1]=-x2
		return Path
		
	def GetPath1(self):
		x1,y1=ThetatoXY1(self.PSPath[:,0],self.PSPath[:,1],self.l1,self.l2)
		Path1=np.zeros((len(self.PSPath),2))
		Path1[:,0]=y1
		Path1[:,1]=-x1
		return Path1

	def GetV(self,PhaseSpace=0):
		if type(PhaseSpace) is int:
			PhaseSpace=np.array([[self.t1,self.t2,self.w1,self.w2]])
		MinE=self.MinE
		E1=Pendulum.g*self.l1*(self.m1+self.m2)*cos(PhaseSpace[:,0])
		E2=Pendulum.g*self.l2*self.m2*cos(PhaseSpace[:,1])
		return -MinE-E1-E2

	def GetT(self,PhaseSpace=0):
		if type(PhaseSpace) is int:
			PhaseSpace=np.array([[self.t1,self.t2,self.w1,self.w2]])
		term1=self.l1**2*PhaseSpace[:,2]**2*(self.m1+self.m2)/2
		term2=self.l2**2*PhaseSpace[:,3]**2*self.m2/2
		term3=self.m2*self.l1*self.l2*PhaseSpace[:,2]*PhaseSpace[:,3]*cos(PhaseSpace[:,0]-PhaseSpace[:,1])
		return term1+term2+term3

	def GetL(self,PhaseSpace=0):
		return self.GetT(PhaseSpace)-self.GetV(PhaseSpace)

	def GetH(self,PhaseSpace=0):
		return self.GetT(PhaseSpace)+self.GetV(PhaseSpace)

	def ShowH(self):
		plt.plot(np.linspace(0,self.time,len(self.PSPath)),self.GetH(self.PSPath))
		plt.show()

	def ShowV(self):
		plt.plot(np.linspace(0,self.time,len(self.PSPath)),self.GetV(self.PSPath))
		plt.show()

	def ShowT(self):
		plt.plot(np.linspace(0,self.time,len(self.PSPath)),self.GetT(self.PSPath))
		plt.show()

	def LogDiffH(self,PhaseSpace=0):
		return np.log10(self.H0-self.GetH(PhaseSpace))
