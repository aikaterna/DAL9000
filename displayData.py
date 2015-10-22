# Lizzie Tonkin
# Last edited: Oct 3, 2015
# Class that organizes all display related stuff into one place.


"""
No known bugs or issues
"""
import Tkinter as tk

# display data class
# is meant to be attached to a dragon
class DisplayData:
	# really really lazy class, since everything starts uninitiallized.  This is mostly for organizational purposes.
	# dragon is a Dragon object that will be associated with this DisplayData
	def __init__(self, dragon):
		# reference to it's dragon here, for convenience maybe
		self.derg = dragon
		# display stuff that is filled in later
		self.rect = None # the outline (black, sometimes green or yellow or red)
		self.image = None # the image on the canvas, which is inside the rectangle
		self.photo = None # a PhotoImage object which is connected to the image object
		
		self.leftLine = None # the line that connects to the mother
		self.rightLine = None # the line that connects to the father
		
		self.x = None # not used yet.
		self.y = None
		
		self.selected = False
		self.related = False
		
	
	# uses the data the dragon has stored to created the visual structure of the dragon and add it to the canvas.
	# this is not done at the beginning so we can be sure that the dragon is properly constructed with proper parents
	# returns the image object, which is used in important things, mainly determining which dragon is being hovered over.
	def assemble(self, x,y,canvas):
		
		# try to find the image based on the id (will be changed to be based on an image location)
		try:
			self.photo = tk.PhotoImage(file=str(self.derg.id)+".gif")
		# otherwise, use the backup image
		except:
			self.photo = tk.PhotoImage(file="MissingNo.gif")
		
		# created the image and rectangle objects on the canvas 
		self.image = canvas.create_image( x,y, image = self.photo,anchor=tk.NW)
		self.rect = canvas.create_rectangle( x,y , x+75,y+75, outline = "black" )
		
		#If fist get, just mage the lines start and end on the same point to make them non visible
		if self.derg.gen == 1:
			curLoc = canvas.coords(self.rect)
			self.leftLine = canvas.create_line(curLoc[0],curLoc[1] , curLoc[2],curLoc[1], fill='black' )
			self.rightLine = canvas.create_line(curLoc[0],curLoc[1] , curLoc[2],curLoc[1], fill='black' )
			
		#if normal gen, take the lines and connect them from the appropriate corner to the center of the appropriate parent
		else:
			momLoc = canvas.coords(self.derg.motherDragon.visuals.rect)
			dadLoc = canvas.coords(self.derg.fatherDragon.visuals.rect)
			curLoc = canvas.coords(self.rect)
			self.leftLine = canvas.create_line( (momLoc[0]+momLoc[2])/2,momLoc[3] , curLoc[0],curLoc[1], fill='black', width=2 )
			self.rightLine = canvas.create_line( (dadLoc[0]+dadLoc[2])/2,dadLoc[3] , curLoc[2],curLoc[1], fill='black', width=2 )
		
		# make the rectangle on tope ot make it slightly prettier
		canvas.lift(self.rect)
		
		# return the image so it can be added to a list of images
		return self.image
	
	# function to call if this dragon's mother has been removed
	# set the line pointing to the mother to nothing, so it exists but is not displayed
	def removeMother(self, canvas):
		curLoc = canvas.coords(self.rect)
		canvas.coords(self.leftLine, curLoc[0],curLoc[1] , curLoc[0],curLoc[1])
	
	# function to call if this dragon's father has been removed
	# set the line pointing to the father to nothing, so it exists but is not displayed
	def removeFather(self, canvas):
		curLoc = canvas.coords(self.rect)
		canvas.coords(self.rightLine, curLoc[0],curLoc[1] , curLoc[0],curLoc[1])
	
	# removed all the canvas objects this dragon is associated with.
	# specifically, the lines pointing to it's mother and father, the rectangle, the image,e and the PhotoImage
	def remove(self, canvas):
		canvas.delete(self.rect)
		canvas.delete(self.image)
		canvas.delete(self.photo)
		canvas.delete(self.leftLine)
		canvas.delete(self.rightLine)	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
