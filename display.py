# Author: Lizzie Tonkin
# Last edited: Oct 9, 2015
# Based on:
#	CS 251 2014
#	Project 5
# GUI display, with ability to read in a dragon list, add new dragons, and family planning!
# a bit of a mess as it was converted from an old school project.  Slowly making it less messy

# special thanks to Flight Rising user Resonance, 381, for the color hex values

import Tkinter as tk
import tkFileDialog
import dragonData2 as dd
import dialogs

"""
dragon tree, because it's my pet project
	release notes
		0.0 = python command line version, with features as i add them
			test version, thrown out to beta testers of exceptional worth
			try and get things working here, so next fase can just be trying to create the application with an icon
		0.1 ect = features as i add them
			the tree
			loading/ saving different trees without problems
			mate compatability checking
			offspring predictor
			exalt/delete dragons
		1.0 = New DRG/xml file format.
		1.1 = bug fixes and quality of life
			more predictions and features stuff
		2.0 = re-write in a better language to prepare for 3,0
		2.1 = user preferences
			also, add the non-image square format, so 
			add zooming in and out
		3.0 = first working version as application
			has an icon, launches on click, bonus: launches a file when you click it.
		
		x.x = the dredded UI overhaul to make things pretty
			don't know if to work on this first or user requested features
"""

'''
version 1.2
known bugs
	if you click open and then cancel, things go weird if you try to start from blank on a second chart.  
	edit dragon dialog box does not show current data in color, gene and notes fields
features lacking
	ability delete dragons completely
	square mode: dragons not showing a headshot, but three color bars in a square 
	user preferences (square vs image, distance of dragons from one another, ext)
	ability to rearrange order dragons within layers
	Also see thread for list of things suggested to add
'''


"""
		################################################
							TO DO 
		Then either move on with development or, maybe,
		take some time to make things better organized
		to prevent another mess like this happening.
		
		Mess prevention by good OO design (accessors and
		mutators) and model-view-controller separation
		
		Idea, display object like dragon object, but
		just contains all sorts of things for displaying
						 *hint hint*
		################################################
"""


	
		
	
#######################


# create a class to build and manage the display
# and everything.  This is the read deal, the one true class
# I should change that for the mvc thing
class DisplayApp:

	def __init__(self, width, height):

		# create a tk object, which is the root window
		self.root = tk.Tk()

		# width and height of the window
		self.initDx = width
		self.initDy = height
		
		#important feilds.	I am sorry there are so many, but they make life so much easier
		self.horizontalGap = 160/2 +20 # horizontal distance between dragons
		self.verticalGap = 180/2 + 10 # vertical distance between dragons
		
		self.pointSelect = None # dragon object that is selected (green outline, via double click)
		self.pointSelText = tk.StringVar()	# text on the side window, often relating to the dragon selected
		self.hoverDrag = None # dragon you hover over when comparing liniages n stuff
		
		self.dragons = dd.Data() # dragon data object holding all the dragons
		self.imageKey = {} #key, the dragon image objects (numbers), result, the dragon objects (objects)
		self.colorData = {} # all colors, with string names as keys, returning [int number in spectrum, string hex value]
		self.colorList = ["Maize","White","Ice","Platinum","Silver","Gray","Charcoal","Coal","Black","Obsidian","Midnight","Shadow","Mulberry","Thistle","Lavender","Purple","Violet","Royal","Storm","Navy","Blue","Splash","Sky","Stonewash","Steel","Denim","Azure","Caribbean","Teal","Aqua","Seafoam","Jade","Emerald","Jungle","Forest","Swamp","Avocado","Green","Leaf","Spring","Goldenrod","Lemon","Banana","Ivory","Gold","Sunshine","Orange","Fire","Tangerine","Sand","Beige","Stone","Slate","Soil","Brown","Chocolate","Rust","Tomato","Crimson","Blood","Maroon","Red","Carmine","Coral","Magenta","Pink","Rose"] # this is a list of color names as strings you dummy
		self.totalX = 0 # how much the thing is off zero from the x perspective.  So new dragons are added in a reasonable location
		self.totalY = 0 # how much the thing is off zero from the y perspective.  So new dragons are added in a reasonable location
		
		self.panelCanvas = None # mini canvas on the side where the colors and potential ranges are displayed
		self.selectedColor = [] # holds rectangles which show the color of the selected dragon
		self.posibleColor = [[],[],[]] # three lists of rectangles showing potential colors of offspring (primary, secondary, tertiary)
		
		# all genes and breeds with their relative rarity
		# a dictionary, key is string capitalized name, result is integer used to index into the rarity table
		# 0 = plentiful, 1 = common, 2 = uncommon, 3 = limited, 4 = rare
		self.rarityIndex = {"Fae":0,"Guardian":0,"Mirror":0,"Pearlcatcher":1,"Ridgeback":1,"Tundra":0,"Spiral":1,"Imperial":3,"Snapper":1,"Wildclaw":4,"Nocturne":3,"Coatl":4,"Skydancer":2, \
							"Basic":0,"Iridescent":4,"Tiger":1,"Clown":1,"Speckle":1,"Ripple":2,"Bar":2,"Crystal":4,"Vipera":2,"Piebald":1,"Cherub":2, \
							"Shimmer":4,"Stripes":1,"Eye Spots":1,"Freckle":1,"Seraph":2,"Current":1,"Daub":1,"Facet":4,"Hypnotic":1,"Paint":1,"Peregrine":1, \
							"Circuit":4,"Gembond":3,"Underbelly":1,"Crackle":2,"Smoke":2,"Spines":3,"Okapi":2,"Glimmer":4}
		# use the relative rarity of two genes or breeds to find the odds of each one in a cross
		self.rarityTable = [["50/50","70/30","85/15","97/3","99/1"], 
							["30/70","50/50","75/25","90/10","99/1"],
							["15/85","25/75","50/50","85/15","98/2"],
							["3/97","10/90","15/85","50/50","97/3"],
							["1/99","1/99","2/98","3/97","50/50"]]
							
		# set up the geometry for the window
		self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

		# set the title of the window
		self.root.title("Dragon Ancestry and Lineages 9000")# May it's reign of terror be merciful

		# set the maximum size of the window for resizing
		self.root.maxsize( 1600, 900 )

		# setup the menus
		self.buildMenus()

		# build the controls
		self.buildControls()

		# build the Canvas
		self.buildCanvas()

		# bring the window to the front
		self.root.lift()

		# - do idle events here to get actual canvas size
		self.root.update_idletasks()

		# now we can ask the size of the canvas
		print self.canvas.winfo_geometry()
		
		# set up the key bindings
		self.setBindings()
		
		# set up the application state
		self.baseClick = None # used to keep track of mouse movement
		self.baseView = None
		
		# load color data from the color file
		fobj = file("colorInfo.txt")
		lines = fobj.readlines()
		fobj.close()
		
		# newline characters are tricky, make sure not reading it as one big line
		if len(lines) == 1:
			lines = lines[0].split("\r")
		# every color is on a line
		for line in lines:
			# split the line into it's parts, and make the colorData dictionary described above.
			words = line.strip().split(",")
			words[0] = int(words[0])
			self.colorData[words[1]] = [words[0],words[2]]
		print self.colorData
		
		
##############################
#setup related stuff
		
	# build the menues
	def buildMenus(self):
		
		# create a new menu
		menu = tk.Menu(self.root)

		# set the root menu to our new menu
		self.root.config(menu = menu)

		# create a variable to hold the individual menus
		menulist = []

		# create a file menu
		filemenu = tk.Menu( menu )
		menu.add_cascade( label = "File", menu = filemenu )
		menulist.append(filemenu)

		# create another menu for View
		cmdmenu = tk.Menu( menu )
		menu.add_cascade( label = "View", menu = cmdmenu )
		menulist.append(cmdmenu)
		
		# menu text for the elements
		# the first sublist is the set of items for the file menu
		# the second sublist is the set of items for the view menu
		menutext = [ [ 'Open	\xE2\x8C\x98-O', '-', 'Save	\xE2\x8C\x98-S', '-', 'Quit	\xE2\x8C\x98-Q' ],
					 [ 'Reset		\xE2\x8C\x98-R']]

		# menu callback functions (note that some are left blank,
		# so that you can add functions there if you want).
		# the first sublist is the set of callback functions for the file menu
		# the second sublist is the set of callback functions for the view menu
		menucmd = [ [self.handleOpen, None, self.handleSave, None, self.handleQuit],
					[self.reset]]
		
		# build the menu elements and callbacks
		for i in range( len( menulist ) ):
			for j in range( len( menutext[i]) ):
				if menutext[i][j] != '-':
					menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
				else:
					menulist[i].add_separator()


	# create the canvas object
	def buildCanvas(self):
		self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
		self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
		return


	# build a frame and put controls in it
	def buildControls(self):
		# make a control frame on the right
		rightcntlframe = tk.Frame(self.root)
		rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

		# make a separator frame
		sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Control Panel", width=20, font = ("arial",18) )
		label.pack( side=tk.TOP, pady=10 )
		
		# button for adding new dragons
		button5 = tk.Button( rightcntlframe, text="Add Dragon", 
							   command=self.handleNewDragon )
		button5.pack(side=tk.TOP)
		
		# Moderatly useless button
		button4 = tk.Button( rightcntlframe, text="Do Not Click", 
							   command=self.handleButton4 )
		button4.pack(side=tk.TOP, pady=5)
		
		# button to edit a dragon.  Starts disabled, and is enabled when a dragon is selected
		self.button3 = tk.Button( rightcntlframe, text="Edit Dragon", 
							   command=self.handleEditDragon ,state=tk.DISABLED)
		self.button3.pack(side=tk.TOP, pady=5)
		
		# button to exalt a dragon.  Starts disabled, and is enabled when a dragon is selected
		self.button2 = tk.Button( rightcntlframe, text="Exault Dragon", 
							   command=self.handleExaultDragon ,state=tk.DISABLED)
		self.button2.pack(side=tk.TOP, pady=5)
		
		# Selected Dragon section contains information pertaining to a selected dragon
		self.pointSelText.set("No Dragon selected")
		label = tk.Label( rightcntlframe, width=20, textvariable=self.pointSelText,justify=tk.LEFT )
		label.pack( side=tk.TOP)
		
		# add a mini canvas to display colored rectangles representing colors
		self.panelCanvas = tk.Canvas(rightcntlframe, width=186, height=96,bg="white")
		self.panelCanvas.pack(side=tk.TOP, pady=5)
		
		# create those rectangles.  They start hidden.
		self.selectedColor.append(self.panelCanvas.create_rectangle( 10,10 , 60,90, fill='blue',state=tk.HIDDEN))
		self.selectedColor.append(self.panelCanvas.create_rectangle( 70,10 , 120,90, fill='blue',state=tk.HIDDEN))
		self.selectedColor.append(self.panelCanvas.create_rectangle( 130,10 , 180,90, fill='blue',state=tk.HIDDEN))
		
		# three rows of smaller rectangles for offspring potential color range.  They start hidden.
		for i in range(34):
			self.posibleColor[0].append(self.panelCanvas.create_rectangle( 10+5*i,10 , 13+5*i,30, fill="blue",outline='blue',state=tk.HIDDEN))
			self.posibleColor[1].append(self.panelCanvas.create_rectangle( 10+5*i,40 , 13+5*i,60, fill="blue",outline='blue',state=tk.HIDDEN))
			self.posibleColor[2].append(self.panelCanvas.create_rectangle( 10+5*i,70 , 13+5*i,90, fill="blue",outline='blue',state=tk.HIDDEN))
		
		# add a place for text to appear below the rectangles.  These are the notes.
		self.dragonText = tk.Text(rightcntlframe, height=10, width =20,wrap=tk.WORD,takefocus=True,relief = tk.SUNKEN)
		self.dragonText.pack(side=tk.TOP, pady=5)
		
		
	# Bind things to other things
	def setBindings(self):
		# bind mouse motions to the canvas
		self.canvas.bind( '<Button-1>', self.handleMouseButton1MotionStart )
		self.canvas.bind( '<Double-Button-1>', self.handleMouseButton1 )
		self.canvas.bind( '<Button-2>', self.handleMouseButton3 )
		self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
		self.canvas.bind( '<Motion>', self.handleMouseMotion )
		self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )
		self.canvas.bind( '<B2-Motion>', self.handleMouseButton3Motion )
		self.canvas.bind( '<Control-B1-Motion>', self.handleMouseButton2Motion )
		
		# bind command sequences to the root window
		self.root.bind( '<Command-q>', self.handleQuit )
		self.root.bind( '<Command-o>', self.handleOpen )
		self.root.bind( '<Command-s>', self.handleSave )
		self.root.bind( '<Command-r>', self.reset )




###############################
#stuff related to data and display and data display

	# This functon should be called whenever the view is changed and there is data, as it changes the data to reflect the view.
	def updataData(self):
		# actually I have no idea why this function still exists.  Keeping it for the print statement.  
		print 'data has been outlawed by the freedom of non-infomration act'
			
	
	#This function handles opening a new file
	def handleOpen(self, event = None):
		#delete previous stuff, if any
		allStuff=self.canvas.find_all()
		for item in allStuff:
			self.canvas.delete(item)
		
		# reset x and y offset
		self.totalX = 0
		self.totalY = 0
		
		# reset selected dragon
		self.handleMouseButton1()
		
		# the file opening thingy
		fn = tkFileDialog.askopenfilename( parent=self.root, title='Choose a data file', 
					 initialdir='.' )
		if fn == '':
			return
		name = fn.split('/')[-1]
		
		# import starting dragons and build beginning tree.
		self.dragons = dd.Data(name)
		
		# get a list of levels
		levels = self.dragons.genMap.keys()
		levels.sort()
		
		# draw each dragon component in a grid determined by it's level and position within the level
		# dragon component is the image, the rectangle, and lines pointing to mother and father
		for i in range(len(levels)):
			for j in range(len(self.dragons.genMap[levels[i]])):
				self.imageKey[self.dragons.genMap[levels[i]][j].visuals.assemble(100+self.horizontalGap*j,100+self.verticalGap*i, self.canvas)]=self.dragons.genMap[levels[i]][j]
		
		#stop displaying exalted dragons
		keys = self.dragons.IDmap.keys()
		for key in keys:
			if self.dragons.IDmap[key].exalt:
				self.removeDragonFromDisplay(self.dragons.IDmap[key])
		
	
	# function that saves the current dragon tree state
	def handleSave(self, event = None):
		# file opening thingy
		fn = tkFileDialog.asksaveasfilename( defaultextension = ".drg",parent=self.root, title='Choose a data file', 
					 initialdir='.' )
		if fn == '':
			return
		# save those dragons!
		self.dragons.saveInFile(fn)
		print "Saved!"
		
		
##########################
# interaction functions bound to the root

	
	# Quit
	def handleQuit(self, event=None):
		print 'Terminating'
		self.root.destroy()

	# resets the view to the origional view.
	def reset(self, event = None):
		print 'no reset for you'
		
	
############################
# interaction functions bound to buttons or menues
	

	# When this button is pressed, a sarcastic message appears on the screen and in the terminal
	def handleButton4(self):
		w = tk.Message(self.canvas, text="Now look what you've done",width=100)
		w.config(background="red")
		w.pack(side=tk.TOP)
		print 'Your inability to follow simple instructions has been noted.'
		
	
	# This function adds a new dragon to the family
	def handleNewDragon(self, event = None):
		# all data is entered in the dialog box, and then stored in the result feild
		box = dialogs.AddDragonDialog(self.root, self.dragons)
		par = box.result
		
		# make sure that the free entry fields have been filled to prevent errors
		if (box.result[2]=="" or box.result[3]==""):
			print "ERROR: Please include a name and ID number"
			return
		
		# assigne matingType, from string to boolean (no not the familiar, the data type)
		if par[4] == "Female":
			matingType = True
		else:
			matingType = False
		
		# Either it has two parents or has none.  No halvesies.
		if (int(par[0]) == 0) or (int(par[1]) == 0):
			mother = None
			father = None
		else:
			mother = self.dragons.IDmap[int(par[0])]
			father = self.dragons.IDmap[int(par[1])]
		
		# create the new dragon object, and then add it to the tree
		new = dd.Dragon( int(par[3]), par[2], 1, None, None, False, matingType, par[5], [par[6],par[8],par[10]], [par[7],par[9],par[11]], par[12])
		self.dragons.add(new, mother, father)
		
		# place the dragon in the appropriate grid space
		i = new.gen-1
		j = len(self.dragons.genMap[new.gen])-1 
		
		# add the visual components of the dragon to the display, and we are done!
		self.imageKey[new.visuals.assemble(100+self.horizontalGap*j+self.totalX, 100+self.verticalGap*i+self.totalY, self.canvas)] = new
	
	
	# this is the function called when the edit dragon button is pushed.  Allows the user to edit the information that can be changed
	def handleEditDragon(self, event = None):
		# dialog box that allows user to change some of the dragon's current values, and stores them in the results feild
		box = dialogs.EditDragonDialog(self.root, self.dragons, self.pointSelect)
		par = box.result
		
		# make sure the name is not left blank.  
		if box.result[0]=="":
			print "ERROR: Please include a name"
			return
			
		# change the dragon's fields appropriately.  Thank goodness they are already strings
		self.pointSelect.name = box.result[0]
		self.pointSelect.species = box.result[1]
		self.pointSelect.colors[0] = box.result[2]
		self.pointSelect.genes[0] = box.result[3]
		self.pointSelect.colors[1] = box.result[4]
		self.pointSelect.genes[1] = box.result[5]
		self.pointSelect.colors[2] = box.result[6]
		self.pointSelect.genes[2] = box.result[7]
		self.pointSelect.notes = box.result[8]
		
		# update the display data one the side to reflect the new dragon appearance
		self.updateDragonSide()
		
		
	# the function called when the exalt button is clicked.
	def handleExaultDragon(self, event = None):
		# show the exalt dialog box, and if verified, exalt the dragon (remove from display)	
		box = dialogs.ExaultDragonDialog(self.root, self.pointSelect)
		if box.result:
			self.removeDragonFromDisplay(self.pointSelect)


############################
# helper functions from all walks of life
	
	
	# removes visual markers of a dragon.  Dragon still exists in tree structure
	def removeDragonFromDisplay(self, dragon):
		# stop children from pointing to parent
		for child in dragon.decendants[0]:
			# was a mother
			if dragon.matingType:
				child = self.dragons.IDmap[child]
				if not child.exalt:
					child.visuals.removeMother(self.canvas)
			# was a father
			else:
				child = self.dragons.IDmap[child]
				if not child.exalt:
					child.visuals.removeFather(self.canvas)
		
		# do the exalt thing
		self.dragons.exault(dragon)
		
		# remove it from the visual reference list
		del self.imageKey[dragon.visuals.image]
		
		# remove the dragon images and pointers to parents
		dragon.visuals.remove(self.canvas)
		
		# stop selecting this point
		self.pointSelect = None
		self.resetDragonSide()


	# function that updates the side display to represent a selected dragon
	def updateDragonSide(self):
		# make sure the possible colors of potential offspring are hidden since we are not using them
		for i in range(len(self.posibleColor)):
			for j in range(len(self.posibleColor[i])):
				self.panelCanvas.itemconfig(self.posibleColor[i][j], state = tk.HIDDEN)
		# if we there is a 'hoverDrag' selected, we're not doing that any more so stop it
		if self.hoverDrag != None:
			# remove the hilighting of the selected dragon's ancestors
			for level in self.pointSelect.ansestors:
				for id in level:
					ansestor = self.dragons.IDmap[id]
					ansestor.visuals.related = False
					self.canvas.itemconfig(ansestor.visuals.rect, outline="black",width=1)
			# remove the hilighting of the dragon formerly being hovered over's ancestors
			for level in self.hoverDrag.ansestors:
				for id in level:
					ansestor = self.dragons.IDmap[id]
					ansestor.visuals.related = False
					self.canvas.itemconfig(ansestor.visuals.rect, outline="black",width=1)
			# stop hilighting the formerly hovered dragon
			self.hoverDrag.visuals.related = False
			self.canvas.itemconfig(self.hoverDrag.visuals.rect, outline="black",width=1)
			# finally, dispence with this hover dragon nonsence
			self.hoverDrag = None
			
		# now, update the side display to reflect the selected dragon
		
		# extract parent names, if you have any.
		if self.pointSelect.motherDragon == None:
			motherName = "None"
		else:
			motherName = self.pointSelect.motherDragon.name
			
		if self.pointSelect.fatherDragon == None:
			fatherName = "None"
		else:
			fatherName = self.pointSelect.fatherDragon.name
		
		# find the making type	
		if self.pointSelect.matingType:
			matingType = "Female"
		else:
			matingType = "Male"
		
		# set the text to something that shows ALL the data
		self.pointSelText.set("Dragon Info\r\rName: %s" %(self.pointSelect.name)+
										  "\rID: %d" %(self.pointSelect.id)+
										  "\rMating Type: %s" %(matingType)+
										  "\rGeneration: %d" %(self.pointSelect.gen)+
										  "\r\rMother: %s"%(motherName)+
										  "\rFather: %s"%(fatherName)+
										  "\r\rSpecies: %s"%(self.pointSelect.species)+
										  "\r\rPrimary: %s"%(self.pointSelect.genes[0])+
										  "\r     %s"%(self.pointSelect.colors[0])+
										  "\rSecondary: %s"%(self.pointSelect.genes[1])+
										  "\r     %s"%(self.pointSelect.colors[1])+
										  "\rTertiary: %s"%(self.pointSelect.genes[2])+
										  "\r     %s"%(self.pointSelect.colors[2])+"")
	
		# make the color boxes the appropriate color and set them to visible
		self.panelCanvas.itemconfig(self.selectedColor[0], fill=self.colorData[self.pointSelect.colors[0]][1],state = tk.NORMAL)
		self.panelCanvas.itemconfig(self.selectedColor[1], fill=self.colorData[self.pointSelect.colors[1]][1],state = tk.NORMAL)
		self.panelCanvas.itemconfig(self.selectedColor[2], fill=self.colorData[self.pointSelect.colors[2]][1],state = tk.NORMAL)
		
		# displaying the notes
		self.dragonText.config(state=tk.NORMAL) # set the text thing to be editable
		self.dragonText.delete(1.0, tk.END) # delete the old text
		self.dragonText.insert(tk.END,self.pointSelect.notes) # set the text to what is in the dragon's notes
		self.dragonText.config(state=tk.DISABLED) # set the text to uneditable
		
		# unlock the buttons associated with selected dragons
		self.button3.config(state=tk.NORMAL)
		self.button2.config(state=tk.NORMAL)
		
	
	# sets the side of the dragon panel for when comparing two dragons, wether or not they are compatible
	def compareDragonSide(self):
		
		# make sure that the squares used for displaying a selected dragon's color are hidden
		self.panelCanvas.itemconfig(self.selectedColor[0], state = tk.HIDDEN)
		self.panelCanvas.itemconfig(self.selectedColor[1], state = tk.HIDDEN)
		self.panelCanvas.itemconfig(self.selectedColor[2], state = tk.HIDDEN)
		
		# if the dragon currently being hovered over has the same mating type as the current dragon, state the match is impossible and return
		if (self.pointSelect.matingType == self.hoverDrag.matingType):
			self.pointSelText.set("Imcompatible match:\nMating type mismatch.")
			return 
		
		ansestorClash = "" # list of problematic ancestors, if any
			
		# highlight the ancestors of the selected dragon
		for level in self.pointSelect.ansestors:
			for id in level:
				ansestor = self.dragons.IDmap[id]
				ansestor.visuals.related = True
				self.canvas.itemconfig(ansestor.visuals.rect, outline="yellow",width=10)
		
		# highlight the ancestors of the hover dragon
		for level in self.hoverDrag.ansestors:
			for id in level:
				ansestor = self.dragons.IDmap[id]
				if ansestor.visuals.related:
					# if an ansestor has already been highlighted, outline in red and add to a list of problematic ancestors
					self.canvas.itemconfig(ansestor.visuals.rect, outline="red",width=10)
					ansestorClash+= ", "+ansestor.name
				else:
					self.canvas.itemconfig(ansestor.visuals.rect, outline="yellow",width=10)
		
		# hi-light the hover dragon, we can't forget that!
		if self.hoverDrag.visuals.related:
			self.canvas.itemconfig(self.hoverDrag.visuals.rect, outline="red",width=10)
			ansestorClash+= ", "+self.hoverDrag.name
		else:
			self.canvas.itemconfig(self.hoverDrag.visuals.rect, outline="green",width=10)
		
		# if the list of problematic ancestors is not empty, then we have a problem.  Display who they are and return
		if ansestorClash != "":
			self.pointSelText.set("Imcompatible match:\nCommon ansestors:\n"+ansestorClash)
			return
		
		# finally, we have something that works!
		self.pointSelText.set("Compatible match!")
		
		# for primary, secondary, and tertiary
		for i in range(3):
			
			# re set previous, so no old color range is showing (can be a problem with quick switches that do not trigger any of the re-set functions)
			for j in range(len(self.posibleColor[i])):
				self.panelCanvas.itemconfig(self.posibleColor[i][j], state = tk.HIDDEN)
			
			# now for the fun color data stuff!  With math I don't understand!  Which is weird since I wrote it.
			
			# ok, fund the higher and the lower of the two colors being compared.  Remember, the colors are numbers starting a Maize
			up = max(self.colorData[self.pointSelect.colors[i]][0],self.colorData[self.hoverDrag.colors[i]][0])
			low = min(self.colorData[self.pointSelect.colors[i]][0],self.colorData[self.hoverDrag.colors[i]][0])
			
			# if the range of colors between the two is greater than 33
			if (up - low) > 33:
				# we start with the low one and go to the high one
				start = low
				end = up
			# otherwise, the range is the other way
			else:
				# so start at the high one and go to the low one
				start = up
				end = low
			
			# because python can handle negative indexes like a taurus
			# start at the start color, and then go down through the color list until he hit the next one, 
			# going to the end of the list and then coming back from there if necessary.
			# trust me it is weird but works.  Until the color wheel extension that is.  
			j = 0
			while self.colorData[self.colorList[end-1]][1] != self.colorData[self.colorList[start-j-1]][1]:
				self.panelCanvas.itemconfig(self.posibleColor[i][j], outline = "black",fill=self.colorData[self.colorList[start-j-1]][1],state = tk.NORMAL)
				j+=1
			# be sure to include the last one
			self.panelCanvas.itemconfig(self.posibleColor[i][j], outline = "black",fill=self.colorData[self.colorList[start-j-1]][1],state = tk.NORMAL)
		
		
	# blanks the side panel, for when no dragon is selected
	def resetDragonSide(self):
		# fix up the text
		self.pointSelText.set("No Dragon selected")
		
		# clear stuff
		
		# clear the possible color ranges
		for i in range(len(self.posibleColor)):
			for j in range(len(self.posibleColor[i])):
				self.panelCanvas.itemconfig(self.posibleColor[i][j], state = tk.HIDDEN)
		
		# clear hilighted ancestors if necessary
		if (self.hoverDrag != None) and (self.pointSelect != None):
			for level in self.pointSelect.ansestors:
				for id in level:
					ansestor = self.dragons.IDmap[id]
					ansestor.visuals.related = False
					self.canvas.itemconfig(ansestor.visuals.rect, outline="black",width=1)
			for level in self.hoverDrag.ansestors:
				for id in level:
					ansestor = self.dragons.IDmap[id]
					ansestor.visuals.related = False
					self.canvas.itemconfig(ansestor.visuals.rect, outline="black",width=1)
		# clear the selected dragon colors	
		self.panelCanvas.itemconfig(self.selectedColor[0], state = tk.HIDDEN)
		self.panelCanvas.itemconfig(self.selectedColor[1], state = tk.HIDDEN)
		self.panelCanvas.itemconfig(self.selectedColor[2], state = tk.HIDDEN)
		# clear the dragon's text
		self.dragonText.config(state=tk.NORMAL)
		self.dragonText.delete(1.0, tk.END)
		self.dragonText.config(state=tk.DISABLED)
		# lock the buttons that need to be locked
		self.button3.config(state=tk.DISABLED)
		self.button2.config(state=tk.DISABLED)


############################
# interaction functions bound to the canvas, mostly pertaining to the mouse and it's motion


	# when you move around the mouse, if a dragon is selected, hover over a dragon to see mating result.	
	def handleMouseMotion(self, event):
		# hovering over something and  dragon is selected
		if (self.canvas.find_overlapping(event.x,event.y,event.x,event.y) != ()) and (self.pointSelect != None):
			# get the thing you are hovering over
			point = self.canvas.find_overlapping(event.x,event.y,event.x,event.y)[-1]
			# if the thing you are hoving over is a dragon
			if point in self.imageKey:
				# hovering over original dragon
				if self.pointSelect.id == self.imageKey[point].id:
					return
				# actually two dragons, so display results 
				else:
					# set the dragon being hovered over to the hoverDragon and begin compatibility analysis and display
					self.hoverDrag = self.imageKey[point]
					self.compareDragonSide()
		# if instead we are not hovering over anything
		else:
			# if no point is selected
			if self.pointSelect == None:
				self.resetDragonSide()
			# if a point is selected
			else:
				self.updateDragonSide()
		
			
	# When you double click, this happens
	# it clears the side display, and then if you double clicked on something, sets it to that
	def handleMouseButton1(self, event=None):
		# resets any previous selection to nothing
		if self.pointSelect != None:
			self.canvas.itemconfig(self.pointSelect.visuals.rect, outline="black",width=1)	
			self.pointSelect = None
			self.resetDragonSide()
		
		# for reset use
		if event == None:
			return
			
		# if something new is selected, it is handled
		if (self.canvas.find_overlapping(event.x,event.y,event.x,event.y) != ()):
			point = self.canvas.find_overlapping(event.x,event.y,event.x,event.y)[-1]
			# only if that something is a dragon, of course
			if point in self.imageKey:
				self.pointSelect = self.imageKey[point]
				self.canvas.itemconfig(self.pointSelect.visuals.rect, outline="green",width=10)	
				self.updateDragonSide()
				
	
	# when you single click
	# it records the starting position, so you can get the difference when moving the mouse around
	def handleMouseButton1MotionStart(self, event):
		self.baseClick = (event.x, event.y)
	
	# when you click and move the mouse with the click down
	# moves the stuff on the canvas around!
	def handleMouseButton1Motion(self, event):
		# find the difference since the last call
		dx = event.x - self.baseClick[0]
		dy = event.y - self.baseClick[1]
		# set a new base click
		self.baseClick = event.x,event.y
		
		# reset the offset, and print it for fun
		self.totalX+=dx
		self.totalY+=dy
		print self.totalX
		print self.totalY
		
		# for each dragon, move it's...
		for drag in self.dragons.dragonList:
			# rectangle frame
			point = drag.visuals.rect
			loc = self.canvas.coords(point)
			self.canvas.coords( point, 
						loc[0] + dx, 
						loc[1] + dy, 
						loc[2] + dx,
						loc[3] + dy )
			# picture
			point = drag.visuals.image
			loc = self.canvas.coords(point)
			self.canvas.coords( point, 
						loc[0] + dx, 
						loc[1] + dy )
			# the left line leading to that parent
			line = drag.visuals.leftLine
			loc = self.canvas.coords(line)
			self.canvas.coords( line, 
						loc[0] + dx, 
						loc[1] + dy, 
						loc[2] + dx,
						loc[3] + dy )
			# that right line leading to it's other parent
			line = drag.visuals.rightLine
			loc = self.canvas.coords(line)
			self.canvas.coords( line, 
						loc[0] + dx, 
						loc[1] + dy, 
						loc[2] + dx,
						loc[3] + dy )
	
	# these functions do nothing but are a reminder to myself to add them back in.  Maybe not rotation though, that does not really apply here.
	
	# records base click and base view for zooming
	def handleMouseButton3(self, event):
		print 'no zoom for you'
			
	# zooming
	# moving the mouse up the screen makes things bigger, moving it down the screen makes them smaller.
	def handleMouseButton3Motion(self, event):
		print 'no zoom for you'

	# records base click and base view for rotation
	def handleMouseButton2(self, event):
		print 'no rotation for you'
	
	# handles the acutall rotation of the view.
	# moving the mouse horizontally rotates around the VUP view axis, moving it vertically rotates around the U view axis
	def handleMouseButton2Motion(self, event):
		print 'no rotation for you'
	

#########################
#main program related stuff
		
		
	# Main program
	def main(self):
		print 'Entering main loop'
		self.root.mainloop()


# call the main program if this file is run
if __name__ == "__main__":
	dapp = DisplayApp(1200, 675)
	dapp.main()
	
	

# The end, nothing more.  
		
		
		

		
		
		

		



