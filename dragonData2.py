# Lizzie Tonkin
# Last edited: Oct 8, 2015
# Based on:
#	CS 251 2014
#	Project 5
# allows data to be read in and stored, and accessed and referenced accordingly



import displayData as d
import string
import xml.etree.ElementTree as ET


"""
Dragon object/ csv file order

int id (also used to find the image)
string name
int generation level
int mother ID
int father ID
boolean exalted (is it still available for breeding (true means exalted and not displayed))
matingType (boolean true female, false male)
species, string
int list 3 colors (using position on color wheel), edit: no use string name, later we will have dictionary of name to position and hex
string list 3 genes
string notes no commas please
"""

## need to fix the tree issues, and make the tree more intigrated
## tree issues is that if the dragons in not created in this program, things will go weird

"""
Ancestry map (not drawn to implementation)

Parents
[[5]
 [4]
 [3]
 [2]
 [1]]
 
Dragon

children
[[1]
 [2]
 [3]
 [4]
 [5]]
"""




# dragon class
# stores all the information in a nice feild
# see above for format
# no special accessors or mutators yet, but there will be some cool ones soon!
class Dragon:
	def __init__(self, id, name, gen, ansestors, decendants, exalt, matingType, species, colors, genes, notes, treeNode=None):
		self.id = id
		self.name = name
		self.gen = gen
		self.motherDragon = None #OK, got rid of individual ID references, but kept direct parent object references because they are important.
		self.fatherDragon = None
		
		self.ansestors = ansestors
		self.decendants = decendants
		
		self.exalt = exalt
		self.matingType = matingType
		self.species = species
		self.colors = colors
		self.genes = genes
		self.notes = string.replace(notes , "\\n" , "\n")  # fixes bug where where newlines display as literal '\n'  See below for reason.
		
		self.treeNode = treeNode
		
		# display stuff that is filled in later
		self.rect = None
		self.image = None
		self.photo = None
		self.visuals = d.DisplayData(self)
		
	# we do have a ugly print to string though, because
	# I'll add a nice printing version later.
	# since no one will see it even if it does go public, whatever	
	
	def __repr__(self):
	# To string function returns the name of the tile
		#return "<"+str(self.id) + ", " + self.name + ", " + str(self.gen) + ", " + str(self.motherID) + ", " + str(self.fatherID) + ", " + str(self.exalt) + ", " + str(self.matingType) + ", " + self.species + ", " + str(self.colors) + ", " + str(self.genes) + ", " + self.notes+">"
		return self.name
		
	# prints a nice easy to read version for fact checking
	def fancyPrint(self):
		return "<"+str(self.id) + ", " + self.name + ", " + str(self.gen) + ", " + \
		str(self.ansestors).replace(',','') + ", " + str(self.decendants).replace(',','') + ", " + str(self.exalt) + ", " + \
		str(self.matingType) + ", " + self.species + ", " + str(self.colors) + ", " + \
		str(self.genes) + ", " + notes+">"
	
	
	# prints the version of the dragon which is stored in a file for later use.
	def saveFormat(self):
		notes = string.replace(self.notes , "\n" , "\\n") #so that these do not cause unwanted newlines in the file, comment newlines are made literal until reloaded, when they are transformed.
		return str(self.id) + ", " + self.name + ", " + str(self.gen) + ", " + \
			str(self.ansestors).replace(',','') + ", " + str(self.decendants).replace(',','') + ", " + str(self.exalt) + ", " + \
			str(self.matingType) + ", " + self.species + ", " + str(self.colors[0])+ " " + \
			str(self.colors[1])+ " " + str(self.colors[2])+ ", " + str(self.genes[0]) + " " + \
			str(self.genes[1]) + " " + str(self.genes[2]) + ", " + notes
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
class Data:

	#creates a Data object based on a filename.	 The file must be in .csv format.
	def __init__(self, filename = None, enums = False, data= None):
		self.DRG= None
		self.IDmap = {}
		self.genMap = {}
		if filename == None:
			self.dragonList = []
			return
		self.dragonList = self.readFromFile(filename)
		
		
		# attach parents and add all dragons to ALL the lists/dictionaries
		parented = []
		notExaulted = []
		for dragon in self.dragonList:
			#print dragon.gen
			#print dragon.name
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
		'''	
			# set up a list of exalted dragons to remove from the dragon list (list is used for dragon display, but not family linkages)
			if not dragon.exalt:
				notExaulted.append(dragon)
		self.dragonList = notExaulted
		'''
		
		print
		print self.dragonList
		print
		print self.IDmap
		print 
		print self.genMap
		print 
		
	# check it all worked
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
		
	#assumes the dragon is a full dragon object, previously created, mother and father full object too, or None
	# for that dragon just make the ancestors and descendants None, We'll replace it for you, also we will determine Gen, you put whatever you like
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
			
			# gen
			dragon.gen = max(mother.gen+1,father.gen+1)
			
			# take parents ancestors and make them our own (with proper tweaks)
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
	def exault(self, dragon):
		# the dragon holds all the info necessary to get rid of itself.
		'''
		# need a better algorithm 
		
		for level in range (5):
			for ansestor in dragon.ansestors[level]:
				print str(ansestor) + 'removed'
				self.IDmap[ansestor].decendants[level].remove(dragon.id)
		
		for level in range (5):
			for decendant in dragon.decendants[level]:
				print str(decendant) + 'removed'
				self.IDmap[decendant].ansestors[level].remove(dragon.id)
				if level == 0:
					if dragon.matingType:
						self.IDmap[decendant].motherDragon = None
					else:
						self.IDmap[decendant].fatherDragon = None
		'''
		dragon.exalt = True
		self.dragonList.remove(dragon)
		#del self.IDmap[dragon.id]
		#self.genMap[dragon.gen].remove(dragon)
		
	
	#takes a filename, which must be in DRG format, and reads it in to creat a list
	# The data is then put into a Dragon object, for slightly better OO design
	# will need to re-do for to make use of the XML tree for even BETTER OO design
	def readFromFile(self, filename):
		self.DRG = ET.parse(filename)
		mainFamily = self.DRG.find('Family')
		allDragons = mainFamily.findall('Dragon')
		
		# list of dragons we will return
		table = []
		
		# all the dragon tags
		for aDragon in allDragons:
		
			if aDragon.find('DAL9000') == None:
				print 'I am a terrible person and don\'t actually support dragons created in other programs yet.  Sorry.'
				quit()
			
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
			# stuff that will hav to change
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
	def saveInFile(self,filename):
		
		# if this is a new file, make the base enclosing tags and Element Tree
		# will need to revisit once something happens with families
		if self.DRG == None:
			root = ET.Element('drg')
			family = ET.SubElement(root, 'Family')
			title = ET.SubElement(family, 'title')
			title.text = "A Family"
			self.DRG = ET.ElementTree(element=root)
			
		# going through all the dragons
		for dragon in self.dragonList:
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
				
				
				
				
			# make sure stuff in node is up to date
			dragon.treeNode.find('name').text = dragon.name
			dragon.treeNode.find('exalted').text = str(dragon.exalt)
			dragon.treeNode.find('species').text = dragon.species
			dragon.treeNode.find('primary').text = dragon.colors[0]+" "+dragon.genes[0]
			dragon.treeNode.find('secondary').text = dragon.colors[1]+" "+dragon.genes[1]
			dragon.treeNode.find('tertiary').text = dragon.colors[2]+" "+dragon.genes[2]
			dragon.treeNode.find('comment').text = dragon.notes
			
			myTag = dragon.treeNode.find('DAL9000')
			myTag.find('gen').text = str(dragon.gen)
			
			# need to re-convert to strings.  What a pain
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
				
		self.DRG.write(filename, method = 'html')
		
		# to add the first line.  I like 'em
		with file(filename, 'r') as original: data = original.read()
		with file(filename, 'w') as modified: modified.write("<?xml version='1.0' encoding='UTF-8'?> \n" + data)		
		
		


	

# Tests stuff
def test():
	dataThing = Data("00converted.csv")
	
	dataThing.check()
	print dataThing.dragonList
	print dataThing.IDmap
	print dataThing.genMap
	
	derg = dataThing.IDmap[5]
	dataThing.exault(derg)
	print
	print "###########################################################"
	print
	
	dataThing.check()
	print dataThing.dragonList
	print dataThing.IDmap
	print dataThing.genMap
	#dataThing.saveInFile("00converted.csv")



	
if __name__ == "__main__":

	test()
