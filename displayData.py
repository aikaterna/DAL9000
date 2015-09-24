# Lizzie Tonkin
# Last edited: July 31, 2015
# Class that organizes all display related stuff into one place.


"""
Here's my latest brilliant idea.  Since we are storign the image data here, it's all fine and 
dandy, except when we need to find a dragon based on hovering over the dragon's image.
Well, as we all know, the images are just refered to by a number.
So, wait for it
DICTIONARY!
"""
import Tkinter as tk

# display data class
# is meant to be attached to a dragon
class DisplayData:
	# really really lazy class, since everything starts uninitiallized.  This is mostly for organizational purposes.
	# I'll probably add some mutators.  Eventually.
	def __init__(self, dragon):
		# reference to it's dragon here, for convenience maybe
		self.derg = dragon
		# display stuff that is filled in later
		self.rect = None
		self.image = None
		self.photo = None
		
		self.leftLine = None
		self.rightLine = None
		
		self.x = None
		self.y = None
		
		self.selected = False
		self.related = False
		
		print 
		print "#####"
		print self.derg.name
		print "#####"
	
	# uses the data the dragon has stored to created the visual structure of the dragon and add it to the canvas.
	def assemble(self, x,y,canvas):
		
		try:
			self.photo = tk.PhotoImage(file=str(self.derg.id)+".gif")
		except:
			self.photo = tk.PhotoImage(file="MissingNo.gif")

		self.image = canvas.create_image( x,y, image = self.photo,anchor=tk.NW)
		self.rect = canvas.create_rectangle( x,y , x+75,y+75, outline = "black" )
		
		#self.image = canvas.create_image( 100+self.horizontalGap*j+self.totalX,100+self.verticalGap*i+self.totalY, image = new.visuals.photo,anchor=tk.NW)
		#self.rect = canvas.create_rectangle( 100+self.horizontalGap*j+self.totalX,100+self.verticalGap*i+self.totalY , 175+self.horizontalGap*j+self.totalX,self.verticalGap*i+175+self.totalY, outline = "black" )
		
		#image and display stuff first gen
		if self.derg.gen == 1:
			#lines		
			curLoc = canvas.coords(self.rect)
			self.leftLine = canvas.create_line(curLoc[0],curLoc[1] , curLoc[2],curLoc[1], fill='black' )
			self.rightLine = canvas.create_line(curLoc[0],curLoc[1] , curLoc[2],curLoc[1], fill='black' )
			
		#image stuff; normal gen
		else:
			#lines		
			momLoc = canvas.coords(self.derg.motherDragon.visuals.rect)
			dadLoc = canvas.coords(self.derg.fatherDragon.visuals.rect)
			curLoc = canvas.coords(self.rect)
			self.leftLine = canvas.create_line( (momLoc[0]+momLoc[2])/2,momLoc[3] , curLoc[0],curLoc[1], fill='black', width=2 )
			self.rightLine = canvas.create_line( (dadLoc[0]+dadLoc[2])/2,dadLoc[3] , curLoc[2],curLoc[1], fill='black', width=2 )
		
		canvas.lift(self.rect)
		
		return self.image
	
	def removeMother(self, canvas):
		curLoc = canvas.coords(self.rect)
		canvas.coords(self.leftLine, curLoc[0],curLoc[1] , curLoc[0],curLoc[1])
		
	def removeFather(self, canvas):
		curLoc = canvas.coords(self.rect)
		canvas.coords(self.rightLine, curLoc[0],curLoc[1] , curLoc[0],curLoc[1])
		
	def remove(self, canvas):
		canvas.delete(self.rect)
		canvas.delete(self.image)
		canvas.delete(self.photo)
		canvas.delete(self.leftLine)
		canvas.delete(self.rightLine)
		'''
		# was a mother
		if self.derg.gender:
			for child in self.derg.decendants[0]:
				curLoc = canvas.coords(child.visuals.rect)
				canvas.coords(child.visuals.leftLine, curLoc[0],curLoc[1] , curLoc[2],curLoc[1])
		# was a father:
		else:
			for child in self.derg.decendants[0]:
				curLoc = canvas.coords(child.visuals.rect)
				canvas.coords(child.visuals.rightLine, curLoc[0],curLoc[1] , curLoc[2],curLoc[1])
		'''
		"""ok, now somehow need to change children's lines"""
		
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
