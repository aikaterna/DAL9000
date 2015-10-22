# Lizzie Tonkin
# Last edited: Oct 8, 2015
# Based on:
#	CS 251 2014
#	Project 5
# allows data to be read in and stored, and accessed and referenced accordingly


import displayData as d
import string
import xml.etree.ElementTree as ET

'''
# stuff that needs to be looked into / bugs
### need to fix the tree issues, and make the tree more intigrated
## tree issues is that if the dragons in not created in this program, things will go weird
### some inconsistency with the rest print and what is shown in the display.  Display is right, the check() function is wrong.  
'''



# dragon class
# stores all the information in a nice fields
# see comments next to each field 
# this class will eventually have to be entirely re-written, to make proper use of the new ElementTree
# why did I not write Accessor and Mutator functions when I had the chance? WHY?  There is a lesson here kids, do more code earlier to save time later.
class Dragon:
	def __init__(self, id, name, gen, ansestors, decendants, exalt, matingType, species, colors, genes, notes, treeNode=None):
		self.id = id # integer, id number
		self.name = name # string, name of the dragon
		self.gen = gen # integer, generation within the clan (starting at 1).  Not generation within Flight Rising.
		self.motherDragon = None #reference to mother Dragon object, added later
		self.fatherDragon = None #reference to father Dragon object, added later
		
		self.ansestors = ansestors # five level list, containing list of ancestor Id numbers.  0 is parents, 4 is the greatgreatgreatgreandparents.  Ids themselves in no particular order within the list.  Sub lists can be empty
		self.decendants = decendants # five level list, containing list of descendant Id numbers.  0 is children, 4 is the greatgreatgreatgrandchildren.  Ids themselves in no particular order within the list.  Sub lists can be empty
		
		self.exalt = exalt # boolean, true if exalted, false if still around
		self.matingType = matingType # boolean, true if female, false if male
		
		self.species = species # string, species
		self.colors = colors # list of strings, color names in order primary secondary tertiary 
		self.genes = genes # list of strings, color names in order primary secondary tertiary 
		self.notes = notes # string, notes.  Can include newline characters?
		
		self.treeNode = treeNode #ElementTreeElement, I forget the official object name and am on a plaine with no internet right now.  Anyway, is the <Dragon> tag, so any information of other programs is preserved
		
		self.visuals = d.DisplayData(self) #empty displayData object, which is activated later
		
	
	# To string function returns the name of the dragon.  Can be altered to show all of the information
	def __repr__(self):
		#return "<"+str(self.id) + ", " + self.name + ", " + str(self.gen) + ", " + str(self.motherID) + ", " + str(self.fatherID) + ", " + str(self.exalt) + ", " + str(self.matingType) + ", " + self.species + ", " + str(self.colors) + ", " + str(self.genes) + ", " + self.notes+">"
		return self.name
	
		
	# prints a nice easy to read version for fact checking
	def fancyPrint(self):
		return "<"+str(self.id) + ", " + self.name + ", " + str(self.gen) + ", " + \
			str(self.ansestors).replace(',','') + ", " + str(self.decendants).replace(',','') + ", " + str(self.exalt) + ", " + \
			str(self.matingType) + ", " + self.species + ", " + str(self.colors) + ", " + \
			str(self.genes) + ", " + notes+">"
	
	
	
	
	
	
	
	
	
	
	
	
	
	
# Data class
# holds all the Dragon objects within a few easy to acces lists, which are used for different purposes.  
# is also in charge of makine sure dragons are kept up to date, such as adding children, adding direct parent links, exalting, saving and reading files, the list goes on.  Actually no that's it.  	
class Data:

	#creates a Data object based on a filename.	 The file must be in .drg format.
	def __init__(self, filename = None):
		self.DRG= None # ElementTree object, root I think, the one that encompasses the entire file read in.
		self.IDmap = {} # dictionary, where the dragon's ID is the key, and the Dragon object is the value.  Used for all sorts of things
		self.genMap = {} # dictionary, where the generation within the clan is the key, and the value is a list of Dragon objects in that generation.  Used for ordering initial displays.  
		
		# if this is an empty file, make an empty dragon list and return.  
		if filename == None:
			self.dragonList = []
			return
		
		# otherwise, make a dragon list from the file.  
		# dragon list is just that, a unordered list of Dragon objects.  Used to calculate the offset (a display value), and for finding all the dragon objects when moving them around, and for the initial dragon linking
		self.dragonList = self.readFromFile(filename)
		
		# attach parents and add all dragons to ALL the lists/dictionaries
		for dragon in self.dragonList:
			if dragon.gen != 1:
				for parent in dragon.ansestors[0]:
					# assign proper parents to parental roles
					if self.IDmap[parent].matingType==True:
						dragon.motherDragon = self.IDmap[parent]
					else:
						dragon.fatherDragon = self.IDmap[parent]
			self.IDmap[dragon.id] = dragon
			if not(dragon.gen in self.genMap):
				self.genMap[dragon.gen] = [dragon]
			else:
				self.genMap[dragon.gen].append(dragon)
		
		# check that everything loaded nicely with a nice print
		print
		print self.dragonList
		print
		print self.IDmap
		print 
		print self.genMap
		print 
		
	
		
	#assumes the dragon is a full dragon object, previously created, mother and father full object too, or None
	# for dragon just make the ancestors and descendants None, We'll replace it for you, also we will determine Gen, you put whatever you like
	def add(self, dragon, mother, father):
		
		# fix up the dragon with some data that it needs to get from other dragons
		dragon.ansestors = [[],[],[],[],[]]
		dragon.decendants = [[],[],[],[],[]]
		
		# first gen, so no ancestors, and no descendants yet.
		if mother == None:	
			dragon.gen = 1
			
		# non first gen, assign the parents and ancestors and gen and stuff
		else: #dragon.gen != 1:
			
			# assign proper parents to parental roles
			dragon.motherDragon = mother
			dragon.fatherDragon = father
			dragon.ansestors[0]=[mother.id, father.id]
			
			# gen is the greater of the parental gens plus one
			dragon.gen = max(mother.gen+1,father.gen+1)
			
			# take parents' ancestors and make them our own (with proper tweaks)
			for parent in dragon.ansestors[0]:
				dragon.ansestors[1] = dragon.ansestors[1]+self.IDmap[parent].ansestors[0]
				dragon.ansestors[2] = dragon.ansestors[2]+self.IDmap[parent].ansestors[1]
				dragon.ansestors[3] = dragon.ansestors[3]+self.IDmap[parent].ansestors[2]
				dragon.ansestors[4] = dragon.ansestors[4]+self.IDmap[parent].ansestors[3]
			
			# add self as a child to all ancestors
			for i in range (5):
				for ansestor in dragon.ansestors[i]:
					self.IDmap[ansestor].decendants[i].append(dragon.id)
					
		# add dragon to the support data structures
		self.dragonList.append(dragon)
		self.IDmap[dragon.id]=dragon
		if not(dragon.gen in self.genMap):
			self.genMap[dragon.gen] = [dragon]
		else:
			self.genMap[dragon.gen].append(dragon)
	
		
	#assumes the dragon is a full dragon object, previously created.
	# makes it so that from a visual perspective the dragon does not exist, but it remains in all the data
	def exault(self, dragon):
		dragon.exalt = True
		self.dragonList.remove(dragon)
		# yes, that was horrifically simple.  It used to be more complicated.
		
	
	# takes a filename, string, of a file which must be in DRG format, and reads it in to creat a list
	# The data is then put into a Dragon object, for slightly better OO design
	# will need to re-do for to make use of the XML tree for even BETTER OO design
	def readFromFile(self, filename):
		self.DRG = ET.parse(filename)
		mainFamily = self.DRG.find('Family') # right now settle for first family.  Will have to change.
		allDragons = mainFamily.findall('Dragon')
		
		# list of dragons we will return
		table = []
		
		# all the dragon tags
		for aDragon in allDragons:
		
			if aDragon.find('DAL9000') == None:
				print 'I am a terrible person and don\'t actually support dragons created in other programs yet.  Sorry.'
				quit()
			
			# harvest common values and in some cases cast to proper type
			id = int(aDragon.find('id').text)
			name = aDragon.find('name').text
			value = aDragon.find('exalted').text
			if value == 'True':
				exalt = True
			else:
				exalt = False
			value = aDragon.find('matingType').text
			if value == 'True':
				matingType = True
			else:
				matingType = False
			species = aDragon.find('species').text
			primary = aDragon.find('primary').text.split(' ')
			secondary = aDragon.find('secondary').text.split(' ')
			tertiary = aDragon.find('tertiary').text.split(' ')
			genes = [primary[1], secondary[1], tertiary[1]]
			colors = [primary[0], secondary[0], tertiary[0]]
			notes = aDragon.find('comment').text
			
			##############
			# stuff that will hav to change for compatibility
			# harvest values from personal notes
			myTag = aDragon.find('DAL9000')
			gen = int(myTag.find('gen').text)
			
			ansesestors1 = aDragon.find('parents').text
			ansesestors2 = myTag.find('anestors2').text
			ansesestors3 = myTag.find('anestors3').text
			ansesestors4 = myTag.find('anestors4').text
			ansesestors5 = myTag.find('anestors5').text
			ansestors = [ansesestors1,ansesestors2,ansesestors3,ansesestors4,ansesestors5]
			
			decendants1 = aDragon.find('parents').text
			decendants2 = myTag.find('decendants2').text
			decendants3 = myTag.find('decendants3').text
			decendants4 = myTag.find('decendants4').text
			decendants5 = myTag.find('decendants5').text
			decendants = [decendants1,decendants2,decendants3,decendants4,decendants5]
			
			# need to make Nones into empty lists, and convert strings to ints
			for i in range(4,-1,-1):
				if decendants[i] != None:
					decendants[i]=decendants[i].split(' ')
					decendants[i] = [ int(x) for x in decendants[i] ]
				else: 
					decendants[i] = []
				
				if ansestors[i] != None:
					ansestors[i]=ansestors[i].split(' ')
					ansestors[i] = [ int(x) for x in ansestors[i] ]
				else: 
					ansestors[i] = []
			
			# make a dragon and add it to the table	
			table.append(Dragon(id,name,gen,ansestors,decendants,exalt,matingType,species,colors,genes,notes,aDragon))
		
		# don't forget to return the table!
		return table
		
		
	# saves the current dragons in a fancy file, that can be reopened!	
	# Now in DRG format! (Or as close as I can get to my own impossible standards)
	# takes in filename, a string which is what you want to call the file
	def saveInFile(self,filename):
		
		# if this is a new file, make the base enclosing tags and Element Tree
		# will need to revisit once something happens with families (right now assuming one family per file)
		if self.DRG == None:
			root = ET.Element('drg') #create root element
			family = ET.SubElement(root, 'Family') #create sub elements
			title = ET.SubElement(family, 'title')
			title.text = "A Family"
			self.DRG = ET.ElementTree(element=root) # put it all in an ElementTree wrapper
			
		# go through all the dragons (even exalted) to make sure they are up to date
		keys = self.IDmap.keys()
		for key in keys:
			dragon  = self.IDmap[key]
			
			# if the dragon does not have a node, make one, and fill it with sub nodes
			if dragon.treeNode == None:
				mainFamily = self.DRG.find('Family')
				print mainFamily
				new = ET.SubElement(mainFamily, 'Dragon')
				print new
				dragon.treeNode = new
				
				ET.SubElement(new, 'id')
				dragon.treeNode.find('id').text = str(dragon.id) # add the unchangeable
				ET.SubElement(new, 'name')
				
				ET.SubElement(new, 'parents')
				ET.SubElement(new, 'children')
				
				ET.SubElement(new, 'exalted')
				ET.SubElement(new, 'matingType')
				dragon.treeNode.find('matingType').text = str(dragon.matingType) # add the unchangeable
				ET.SubElement(new, 'species')
				
				ET.SubElement(new, 'primary')
				ET.SubElement(new, 'secondary')
				ET.SubElement(new, 'tertiary')
				ET.SubElement(new, 'comment')
				
				# stuff in just my tag
				myTag = ET.SubElement(new, 'DAL9000')
				ET.SubElement(myTag, 'gen')
				ET.SubElement(myTag, 'anestors2')
				ET.SubElement(myTag, 'anestors3')
				ET.SubElement(myTag, 'anestors4')
				ET.SubElement(myTag, 'anestors5')
				ET.SubElement(myTag, 'decendants2')
				ET.SubElement(myTag, 'decendants3')
				ET.SubElement(myTag, 'decendants4')
				ET.SubElement(myTag, 'decendants5')
			
			
			# make sure stuff in node is up to date, properly formatted.  Any changes will therefor be saved
			dragon.treeNode.find('name').text = dragon.name
			dragon.treeNode.find('exalted').text = str(dragon.exalt)
			dragon.treeNode.find('species').text = dragon.species
			dragon.treeNode.find('primary').text = dragon.colors[0]+" "+dragon.genes[0]
			dragon.treeNode.find('secondary').text = dragon.colors[1]+" "+dragon.genes[1]
			dragon.treeNode.find('tertiary').text = dragon.colors[2]+" "+dragon.genes[2]
			dragon.treeNode.find('comment').text = dragon.notes
			
			myTag = dragon.treeNode.find('DAL9000')
			myTag.find('gen').text = str(dragon.gen)
			
			# need to re-convert ints to strings.  What a pain
			for i in range(5):
				dragon.ansestors[i] = [ str(x) for x in dragon.ansestors[i] ]
				dragon.decendants[i] = [ str(x) for x in dragon.decendants[i] ]
				
			dragon.treeNode.find('parents').text = ' '.join(dragon.ansestors[0])
			myTag.find('anestors2').text = ' '.join(dragon.ansestors[1])
			myTag.find('anestors3').text = ' '.join(dragon.ansestors[2])
			myTag.find('anestors4').text = ' '.join(dragon.ansestors[3])
			myTag.find('anestors5').text = ' '.join(dragon.ansestors[4])
			
			dragon.treeNode.find('children').text = ' '.join(dragon.decendants[0])
			myTag.find('decendants2').text = ' '.join(dragon.decendants[1])
			myTag.find('decendants3').text = ' '.join(dragon.decendants[2])
			myTag.find('decendants4').text = ' '.join(dragon.decendants[3])
			myTag.find('decendants5').text = ' '.join(dragon.decendants[4])
		
		# use the build in write line to write to the file, using the html format, because it has better empty tags		
		self.DRG.write(filename, method = 'html')
		
		# to add the first line, which is nice to have.  
		with file(filename, 'r') as original: data = original.read()
		with file(filename, 'w') as modified: modified.write("<?xml version='1.0' encoding='UTF-8'?> \n" + data)		
		
		
	# check it all worked without the display, buy printing a bunch of dragon information.  
	# used exclusively for testing
	# right now something is wrong with offspring, and it is different than what is shown in the display.  Panic.
	# anyone who figures it out gets a prize
	def check(self):
		print "###"
		for dragon in self.dragonList:
			print dragon.id
			print dragon.name
			print dragon.gen
			print dragon.ansestors[0]
			print dragon.motherDragon
			print dragon.fatherDragon
			print dragon.ansestors
			print dragon.decendants
			print 'ans:'+str(dragon.ansestors).replace(',','')
			print 'des:'+str(dragon.decendants).replace(',','')
			print		

	
	
	
	

# Tests stuff
# right now tests exalting.  Edit as you please  
def test():
	dataThing = Data("demo.drg")
	
	dataThing.check()
	print dataThing.dragonList
	print dataThing.IDmap
	print dataThing.genMap
	
	derg = dataThing.IDmap[3]
	dataThing.exault(derg)
	print
	print "###########################################################"
	print
	
	dataThing.check()
	print dataThing.dragonList
	print dataThing.IDmap
	print dataThing.genMap
	



# this code is only run if this file is.  
if __name__ == "__main__":
	test()
