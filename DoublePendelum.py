#!/usr/bin/env python3
##############################################
## Project DoublePendulum by Lennart & Yens
##############################################
import numpy as np 
import matplotlib.pyplot as plt
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

class Pendulum:
	g=9.81
	Tmax=2.4
	dt=0.0005

	def __init__(self,angle=(pi/2,0),omega=(0,0),mass=(1,2),length=(1,1)):
		self.t1=angle[0] # in rad
		self.t2=angle[1] # in rad
		self.w1=omega[0] # in rad/s
		self.w2=omega[1] # in rad/s
		self.m1=mass[0] # in Kg
		self.m2=mass[1] # in Kg
		self.l1=length[0] # in meter
		self.l2=length[1] # in meter
		self.MinE=-Pendulum.g*(self.l1*(self.m1+self.m2)+self.l2*self.m2)
		self.H0=self.GetH()
		self.time=0
		#self.path=np.array([self.GetXY()[1]])
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
		Peninfo=(Pendulum.g,self.m1,self.m2,self.l1,self.l2)
		U=(self.t1,self.t2,self.w1,self.w2)
		dt=Pendulum.dt
		Unext=U+F1(U,dt,F,Peninfo)/6+2/6*(F2(U,dt,F,Peninfo)+F3(U,dt,F,Peninfo))+F4(U,dt,F,Peninfo)/6
		(self.t1,self.t2,self.w1,self.w2)=Unext
		#self.path=np.concatenate((self.path,np.array([self.GetXY()[1]])))
		print(Unext)
		self.PSPath=np.concatenate((self.PSPath,[Unext]))

	def Solve(self,method):
		Peninfo=(Pendulum.g,self.m1,self.m2,self.l1,self.l2)
		#print(Peninfo)
		U_0=(self.t1,self.t2,self.w1,self.w2)

		if method=='RK4':
			t,U=RK4(Pendulum.dt,Pendulum.Tmax,F_internet,U_0,Peninfo)#F_internet
		elif method=='Euler':
			t,U=euler(Pendulum.dt,Pendulum.Tmax,F_internet,U_0,Peninfo)#F_internet

		(self.t1,self.t2,self.w1,self.w2)=U[-1] #Current phasespace coords = last element of U
		self.time+=t[-1] 
		#x2,y2=ThetatoXY(U[:,0],U[:,1],self.l1,self.l2)
		#self.path=np.stack((x2,y2),axis=-1)
		self.PSPath=np.concatenate((self.PSPath[:-1],U))# Everything except the last one since this is the first element of U

	def ShowPath(self):
		path=self.GetPath()
		plt.ylim([-2.5,2.5])
		plt.xlim([-2.5,2.5])
		plt.grid()
		plt.plot(path[:,1],-path[:,0])
		plt.show()
	def GetPath(self):
		x2,y2=ThetatoXY(self.PSPath[:,0],self.PSPath[:,1],self.l1,self.l2)
		Path=np.zeros((len(self.PSPath),2))
		Path[:,0]=x2
		Path[:,1]=y2
		return Path

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

DP=Pendulum()
DP.Solve('RK4')
DP.ShowPath()
DP.ShowH()
