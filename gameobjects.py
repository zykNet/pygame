# -*- coding: utf-8 -*-
__author__ = 'zyk'
import math
class vector2(object):
	def __init__(self,x=0.0,y=0.0):
		self.x=x
		self.y=y 
	def __str__(self):
		return "(%s,%s)"%(self.x,self.y)
	@classmethod
	def from_points(cls,p1,p2):
		return cls(p2[0]-p1[0], p2[1]-p1[1])
	def get_magnitude(self):
		return math.sqrt( self.x **2+self.y **2)
	def get_normalized(self):
		magnitude = self.get_magnitude()
		self.x /= magnitude
		self.y /= magnitude
	def __add__(self, rhs):
		return vector2(self.x + rhs.x, self.y + rhs.y)
	def __sub__(self, rhs):
		return vector2(self.x - rhs.x, self.y - rhs.y)
	def __mul__(self, scalar):
		return vector2(self.x * scalar, self.y * scalar)
	def __div__(self, scalar):
		return vector2(self.x / scalar, self.y / scalar)
A = (10.0,20.0)
B = (30.0,50.0)
print vector2.from_points(A, B)