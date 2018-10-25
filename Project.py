#!/usr/bin/env python3
##############################################
## Project DoublePendulum by Lennart & Yens
##############################################

import numpy as np 
import matplotlib.pyplot as py 


# we should make some class pendulum which should have te following funtionality:
# call and set the phasespace of a pendulum
# it should be able to do this with using different coordinates:
# eg. get back coordinates in terms of x and y. 
# set it with polar coordinates

accronim=('single','double','triple','quadruple','quintuple','sextuple','septuple','octuple','nonuple','decuple','hendecuple','duodecuple')

class Pendulum:

	def __init__(self,angle=(90,0),mass=(1,2),length=(1,1),velocity=(0,0)):
		self.angle=angle
		self.mass=mass
		self.length=length
		self.velocity=velocity
		self.number=len(angle)


	def Print(self):
		print('A '+ accronim[self.number-1]+' pendulum:')
		for i in range(self.number):
			print('Weight ' + str(i+1) + ': Angle='+str(self.angle[i])+', Mass='+str(self.mass[i])+', Length='+str(self.length[i])+ ', Velocity='+str(self.velocity[i]))

	def Advance(self,number=1):
		# move number of steps forward in the phase space:
		# aka this is where the real physics takes place. 
		pass

	def Animate(self):
		# here we should call some kind of animate class that takes care of the rest. 
		pass

	def GetXcoord(self):
		# this function should return a tuple with all the x-coordinates of the different weights
		pass

	def GetYcoord(self):
		# Analoge as that of the X one.
		pass

pendum=Pendulum()
pendum.Print()


class animate:

	timestep=1/60# 60 fps pc master race
	def __init__(self,pendulum):
		self.pendulum=pendulum
	
	def Draw(self):
		pass

	def 

# We should have a physics physics class which tells us how to advance in time
# However, should give this class as togheter with the pendulum in the initialisation. 
# The class pendulum should then have a function 'advance', updating the phasespace to the next stage. 
# this physics class is maybe a bit to advanced. 

# We should make an animate class. 
# here in we say what we want to draw. 
# we can maybe nest this. (make parent classes and so on) for different GUI's on screen. 


# Also we should have some functionality that we can draw the pendulum for a given phase space.

