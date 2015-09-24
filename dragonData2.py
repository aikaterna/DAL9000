# Lizzie Tonkin
# Last edited: July 31, 2015
# Based on:
#	CS 251 2014
#	Project 5
# allows data to be read in and stored, and accessed and referenced accordingly



import displayData as d
import string



"""
Dragon object/ csv file order

int id (also used to find the image)
string name
int generation level
int mother ID
int father ID
boolean exalted (is it still available for breeding (true means exalted and not displayed))
gender (boolean true female, false male)
species, string
int list 3 colors (using position on color wheel), edit: no use string name, later we will have dictionary of name to position and hex
string list 3 genes
string notes no commas please
"""



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
	def __init__(self, id, name, gen, ansestors, decendants, exalt, gender, species, colors, genes, notes):
		self.id = id
		self.name = name
		self.gen = gen
		self.motherDragon = None #OK, got rid of individual ID references, but kept direct parent object references because they are important.
		self.fatherDragon = None
		
		self.ansestors = ansestors
		self.decendants = decendants
		
		self.exalt = exalt
		self.gender = gender
		self.species = species
		self.colors = colors
		self.genes = genes
		self.notes = string.replace(notes , "\\n" , "\n")  # fixes bug where where newlines display as literal '\n'  See below for reason.
		
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
		#return "<"+str(self.id) + ", " + self.name + ", " + str(self.gen) + ", " + str(self.motherID) + ", " + str(self.fatherID) + ", " + str(self.exalt) + ", " + str(self.gender) + ", " + self.species + ", " + str(self.colors) + ", " + str(self.genes) + ", " + self.notes+">"
		return self.name
		
	# prints a nice easy to read version for fact checking
	def fancyPrint(self):
		return "<"+str(self.id) + ", " + self.name + ", " + str(self.gen) + ", " + \
		str(self.ansestors).replace(',','') + ", " + str(self.decendants).replace(',','') + ", " + str(self.exalt) + ", " + \
		str(self.gender) + ", " + self.species + ", " + str(self.colors) + ", " + \
		str(self.genes) + ", " + notes+">"
	
	
	# prints the version of the dragon which is stored in a file for later use.
	def saveFormat(self):
		notes = string.replace(self.notes , "\n" , "\\n") #so that these do not cause unwanted newlines in the file, comment newlines are made literal until reloaded, when they are transformed.
		return str(self.id) + ", " + self.name + ", " + str(self.gen) + ", " + \
			str(self.ansestors).replace(',','') + ", " + str(self.decendants).replace(',','') + ", " + str(self.exalt) + ", " + \
			str(self.gender) + ", " + self.species + ", " + str(self.colors[0])+ " " + \
			str(self.colors[1])+ " " + str(self.colors[2])+ ", " + str(self.genes[0]) + " " + \
			str(self.genes[1]) + " " + str(self.genes[2]) + ", " + notes
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
class Data:

	#creates a Data object based on a filename.	 The file must be in .csv format.
	def __init__(self, filename = None, enums = False, data= None):
		self.IDmap = {}
		self.genMap = {}
		if filename == None:
			self.dragonList = []
			return
		self.dragonList = self.readFromFile(filename)
		
		# attach parents and add all dragons to ALL the lists/dictionaries
		parented = []
		for dragon in self.dragonList:
			#print dragon.gen
			#print dragon.name
			if dragon.gen != 1:
				for parent in dragon.ansestors[0]:
					# assign proper parents to parental roles
					if self.IDmap[parent].gender==True:
						dragon.motherDragon = self.IDmap[parent]
					else:
						dragon.fatherDragon = self.IDmap[parent]
			self.IDmap[dragon.id] = dragon
			if not(dragon.gen in self.genMap):
				self.genMap[dragon.gen] = [dragon]
			else:
				self.genMap[dragon.gen].append(dragon)
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
		for level in range (5):
			for ansestor in dragon.ansestors[level]:
				print str(ansestor) + 'removed'
				self.IDmap[ansestor].decendants[level].remove(dragon.id)
		
		for level in range (5):
			for decendant in dragon.decendants[level]:
				print str(decendant) + 'removed'
				self.IDmap[decendant].ansestors[level].remove(dragon.id)
				if level == 0:
					if dragon.gender:
						self.IDmap[decendant].motherDragon = None
					else:
						self.IDmap[decendant].fatherDragon = None
		
		
		self.dragonList.remove(dragon)
		del self.IDmap[dragon.id]
		self.genMap[dragon.gen].remove(dragon)
		
	
	#takes a filename, which must be in .csv format, and reads it in to creat a 2D array of the semi-raw data
	# I say semi because the numbers will be converted to actual numbers, not just strings of numbers. #####
	# The data is then put into a Dragon object, for slightly better OO design
	def readFromFile(self, filename):
		fobj = file(filename)
		lines = fobj.readlines()
		fobj.close()
		words = []
		table = []
		if len(lines) == 1:
			lines = lines[0].split("\r")
		for line in lines:
			words = line.strip().split(",")
			
			# I was horribly lazy and parsed each line individually, instead of making an automated process.  Whatever. #####
			words[0]= int(words[0])
			words[1]= words[1].strip()
			words[2]= int(words[2])
			
			# unpacking stringified 2D arrays is hard
			parsed = words[3].strip(' [').replace(']','').split('[')
			#print parsed
			assembled = []
			for gen in parsed:
				assembled+= [gen.strip().split(' ')]
			words[3]= [[],[],[],[],[]]
			for i in range(5):
				for j in range(len(assembled[i])):
					if assembled[i][j] != '':
						words[3][i].append( int(assembled[i][j]))
			
			parsed = words[4].strip(' [').replace(']','').split('[')
			assembled = []
			for gen in parsed:
				assembled+= [gen.strip().split(' ')]
			words[4]= [[],[],[],[],[]]
			for i in range(5):
				for j in range(len(assembled[i])):
					if assembled[i][j] != '':
						words[4][i].append( int(assembled[i][j]))
			
			if words[5].strip() == "False":
				words[5] = False
			else:
				words[5]= True
			
			if words[6].strip() == "False":
				words[6] = False
			else:
				words[6]= True
			
			words[7]= words[7].strip()
			
			words[8]= words[8].strip().split(" ")
				
			words[9]= words[9].strip().split(" ")
			words[10]= words[10].strip()
			
			table.append(Dragon(words[0],words[1],words[2],words[3],words[4],words[5],words[6],words[7],words[8],words[9],words[10]))			
		
		return table
	
	# saves the current dragons in a fancy file, that can be reopened!	
	def saveInFile(self,filename):
		output = ""
		
		for j in range(len(self.genMap.keys())):
			for dragon in self.genMap[j+1]:
				output += dragon.saveFormat() + "\n"
		f = open(filename, 'w')
		print output
		f.write(output)
		f.close








	

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
