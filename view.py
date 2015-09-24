# Lizzie Tonkin
# CS 251 2014
# Project 3
# veiw class makes view matricies so we can put data in the GUI.	Yay!



import numpy as np
import math



# View class, which creates and maintains the viewing matrix, so we can view stuff.
class View:
	def __init__(self):
		self.reset()
		
	#Reset case, which resets the view fields to standard viewing.
	def reset(self):
		self.vrp = np.matrix([[0.5, 0.5, 1]])
		self.vpn = np.matrix([[0, 0, -1]])
		self.vup = np.matrix([[0, 1, 0]])
		self.u = np.matrix([[-1, 0, 0]])
		
		self.extent = [1, 1, 1]
		self.screen = [400, 400]
		self.offset = [20, 20]
	
	#takes in a vector, normalizes it, and returns it
	def normalize(self,vector):
		length = math.sqrt(vector[0,0]*vector[0,0]+vector[0,1]*vector[0,1]+vector[0,2]*vector[0,2])
		vector[0,0] = vector[0,0]/length
		vector[0,1] = vector[0,1]/length
		vector[0,2] = vector[0,2]/length
		return vector
		
	# returns a rotation matrix based on the rotation angles given as paramiters.
	# angleVUP: rotation angle around the y axis
	# anfle U: rotation angle around the x axis
	def rotateVRC(self,angleVUP, angleU):

		# a translation matrix to move the point ( VRP + VPN * extent[Z] * 0.5 ) to the origin.
		t1 = np.matrix([[1, 0, 0, -( self.vrp[0,0] + self.vpn[0,0] * self.extent[2] * 0.5 )],
						[0, 1, 0, -( self.vrp[0,1] + self.vpn[0,1] * self.extent[2] * 0.5 )],
						[0, 0, 1, -( self.vrp[0,2] + self.vpn[0,2] * self.extent[2] * 0.5 )],
						[0, 0, 0, 1] ] )
		
		#axis alignment matrix Rxyz using u, vup and vpn.
		Rxyz = np.matrix([[self.u[0,0], self.u[0,1], self.u[0,2], 0],
						  [self.vup[0,0], self.vup[0,1], self.vup[0,2], 0], # in the notes, it's vup`, IDK if I did this right 
						  [self.vpn[0,0], self.vpn[0,1], self.vpn[0,2], 0],
						  [0, 0, 0, 1] ] )

		# rotation matrix about the Y axis by the VUP angle
		r1 = np.matrix([[math.cos(angleVUP), 0, math.sin(angleVUP), 0],
						[0, 1, 0, 0],
						[-math.sin(angleVUP), 0, math.cos(angleVUP), 0],
						[0, 0, 0, 1] ] )

		# rotation matrix about the X axis by the U angle.
		r2 = np.matrix([[1, 0, 0, 0],
						[0, math.cos(angleU), -math.sin(angleU), 0],
						[0, math.sin(angleU), math.cos(angleU), 0],
						[0, 0, 0, 1] ] )

		# translation matrix that moves ( VRP + VPN * extent[Z] * 0.5 ) back from the origin
		t2 = np.matrix([[1, 0, 0, ( self.vrp[0,0] + self.vpn[0,0] * self.extent[2] * 0.5 )],
						[0, 1, 0, ( self.vrp[0,1] + self.vpn[0,1] * self.extent[2] * 0.5 )],
						[0, 0, 1, ( self.vrp[0,2] + self.vpn[0,2] * self.extent[2] * 0.5 )],
						[0, 0, 0, 1] ] )


		# a numpy matrix where the VRP is on the first row, with a 1 in the homogeneous coordinate, and u, vup, and vpn are the next three rows, with a 0 in the homogeneous coordinate.
		tvrc = np.matrix([[self.vrp[0,0], self.vrp[0,1], self.vrp[0,2], 1],
						  [self.u[0,0], self.u[0,1], self.u[0,2], 0],
						  [self.vup[0,0], self.vup[0,1], self.vup[0,2], 0],
						  [self.vpn[0,0], self.vpn[0,1], self.vpn[0,2], 0]])

		# the actual matrix multiplication
		tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T).T
		
		# put everything where it belongs
		self.vrp = np.matrix([[tvrc[0,0],tvrc[0,1],tvrc[0,2]]])
		self.u = np.matrix([[tvrc[1,0],tvrc[1,1],tvrc[1,2]]])
		self.vup = np.matrix([[tvrc[2,0],tvrc[2,1],tvrc[2,2]]])
		self.vpn = np.matrix([[tvrc[3,0],tvrc[3,1],tvrc[3,2]]])
		self.u = self.normalize(self.u)
		self.vup = self.normalize(self.vup)
		self.vpn = self.normalize(self.vpn)
		
		
	# builds a view transfomation matrix and returns it
	def build(self):
		vtm = np.identity( 4, float )
		t1 = np.matrix([[1, 0, 0, -self.vrp[0, 0]],
						[0, 1, 0, -self.vrp[0, 1]],
						[0, 0, 1, -self.vrp[0, 2]],
						[0, 0, 0, 1] ] )
		vtm = t1 * vtm
		tu = np.cross(self.vup, self.vpn)
		tvup = np.cross(self.vpn, tu)
		tvpn = self.vpn.copy()
		self.u = self.normalize(tu)
		self.vup = self.normalize(tvup)
		self.vpn = self.normalize(tvpn)
		
		# align the axes
		r1 = np.matrix( [[ tu[0, 0], tu[0, 1], tu[0, 2], 0.0 ],
						 [ tvup[0, 0], tvup[0, 1], tvup[0, 2], 0.0 ],
						 [ tvpn[0, 0], tvpn[0, 1], tvpn[0, 2], 0.0 ],
						 [ 0.0, 0.0, 0.0, 1.0 ] ] );
		vtm = r1 * vtm
		
		# translate lower left corner to the origin
		t2 = np.matrix( [[1, 0, 0, 0.5*self.extent[0]],
						 [0, 1, 0, 0.5*self.extent[1]],
						 [0, 0, 1, 0],
						 [0, 0, 0, 1] ] )
		vtm = t2 * vtm
		
		# scale values to screen
		s1 = np.matrix( [[ -self.screen[0] / self.extent[0], 0, 0, 0],
						 [0, -self.screen[1] / self.extent[1], 0, 0],
						 [0, 0,  1.0 / self.extent[2], 0],
						 [0, 0, 0, 1] ] )
		vtm = s1 * vtm
		
		#translate lower left corner to the origin and add veiw offset
		t3 = np.matrix( [[1, 0, 0, self.screen[0] + self.offset[0]],
						 [0, 1, 0, self.screen[1] + self.offset[1]],
						 [0, 0, 1, 0],
						 [0, 0, 0, 1] ] )
		vtm = t3 * vtm
		return vtm
		
	# returns a copy of the current view object
	def clone(self):
		clone=  View()
		clone.vrp = self.vrp.copy()
		clone.vpn = self.vpn.copy()
		clone.vup = self.vup.copy()
		clone.u = self.u.copy()
		
		clone.extent = list(self.extent)
		clone.screen = list(self.screen)
		clone.offset = list(self.offset)
		return clone
		
		
		
	
# test function which tests that the VTM is being properly built.
def test():
	quiteA = View()
	print quiteA.build()




if __name__ == "__main__":
	test()



















