#!/usr/bin/env python3
##############################################
## Project DoublePendulum by Lennart & Yens
##############################################
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from numpy import sin 
from numpy import cos
from numpy import pi
from RK4method import *

style.use('seaborn')

def ThetatoXY(t1,t2,l1,l2):
    x1=l1*cos(t1)
    y1=l1*sin(t1)
    x2=x1+l2*cos(t2)
    y2=y1+l2*sin(t2)
    return x2,y2

class Pendulum:
	g=9.81
	Tmax=60
	dt=0.01
	t=np.arange(0,Tmax,dt)

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
		return np.array([x1,y1]),np.array([x2,y2])

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
			t,U=RK4(Pendulum.dt,Pendulum.Tmax,F,U_0,Peninfo)#F_internet
		elif method=='Euler':
			t,U=euler(Pendulum.dt,Pendulum.Tmax,F,U_0,Peninfo)#F_internet
		(self.t1,self.t2,self.w1,self.w2)=U[-1]
		self.time+=t[-1]
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
#DP.ShowPath()
#DP.ShowH()

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal',autoscale_on=False, xlim=(-2,2),ylim=(-2,2))
ax.set_xlabel(r'$x$', fontsize=15)
ax.set_ylabel(r'$y$', fontsize=15)
#ax.grid()

ln, = ax.plot([],[], 'o-',lw=2 )
H_text=ax.text(0.75,0.95, '',transform=ax.transAxes)
#define an initial state for the animation:

def init():
	ln.set_data([],[])
	H_text.set_text('')
	return ln, H_text

#perform animation step
#print(DP.GetPath())
def animate(i):
	DP.NextStep()
	Pathm2=DP.GetPath()
	ln.set_data(Pathm2[i])
	H_text.set_text('H= %.5f J'%DP.GetH())
	return ln, H_text

from time import time
I=100
ani=animation.FuncAnimation(fig,animate,frames=1000, interval=I,init_func=init, blit=True, repeat=False)

plt.show()
	
