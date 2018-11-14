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
	Tmax=20
	dt=0.01

	def __init__(self,angle=(pi/100,-pi/100),omega=(0,0),mass=(1,2),length=(1,1)):
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
		self.path=np.array([self.GetXY()[1]])

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
		self.path=np.concatenate((self.path,np.array([self.GetXY()[1]])))
    

	def Solve(self):
		Peninfo=(Pendulum.g,self.m1,self.m2,self.l1,self.l2)
		U_0=(self.t1,self.t2,self.w1,self.w2)
		t,U=RK4(Pendulum.dt,Pendulum.Tmax,F,U_0,Peninfo)
		(self.t1,self.t2,self.w1,self.w2)=U[-1]
		self.time=t[-1]
		x2,y2=ThetatoXY(U[:,0],U[:,1],self.l1,self.l2)
		self.path=np.stack((x2,y2),axis=-1)

	def ShowPath(self):
		x2=self.path[:,0]
		y2=self.path[:,1]
		plt.ylim([-2.5,2.5])
		plt.xlim([-2.5,2.5])
		plt.grid()
		plt.plot(y2,-x2)
		plt.show()

	def GetPath(self):
		return self.path

	def GetV(self):
		MinE=self.MinE
		E1=Pendulum.g*self.l1*(self.m1+self.m2)*cos(self.t1)
		E2=Pendulum.g*self.l2*self.m2*cos(self.t2)
		return -MinE-E1-E2

	def GetT(self):
		term1=self.l1**2*self.w1**2*(self.m1+self.m2)/2
		term2=self.l2**2*self.w2**2*self.m2/2
		term3=self.m2*self.l1*self.l2*self.w1*self.w2
		return term1+term2+term3

	def GetL(self):
		return self.GetT()-self.GetV()

	def GetH(self):
		return self.GetT()+self.GetV()

	def LogDiffH(self):
		return np.log10(self.H0-self.GetH())

DB=Pendulum()
DB.Solve()
DB.ShowPath()