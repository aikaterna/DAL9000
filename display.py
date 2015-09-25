# Author: Lizzie Tonkin
# Last edited: July 31, 2015
# Based on:
#	CS 251 2014
#	Project 5
# GUI display, with ability to read in a dragon list, add new dragons, and family planning!

# special thanks to Flight Rising user Resonance, 381, for the color hex values

import Tkinter as tk
import tkFileDialog
import dragonData2 as dd
import dialogs
import view as v

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
		1.0 = first working version, as application
			has an icon, launches on click, bonus: launches a file when you click it.
		1.1 = user preferences
			save from session to session, maybe even release to release
			also, add the non-image square format, so 
			add zooming in and out
		1.2 ect: = user requested features and optimizations
			yay!
		2.0 = the dredded UI overhaul to make things pretty
"""

'''
version 0.4
known bugs
	clicking on selected dragon does not un-select (this may end up being a feature due to poor coding method)
	if you click open and then cancel, things go weird if you try to start from blank
unkown bug:
	did i fix the thing with loading dragon sets of different sizes?  I think i did
features lacking
	right clicking on a dragon while having one selected shows offspring ranges and such
		also shows if there is a common ansestor
	click a dragon in a certain way, maybe normal, to track liniage and offspring through the tree.
	'exalted' dragons do not show, but still factor into tree
	ability delete dragons completely
Work on once 1.0 has been 'released'
	square mode: dragons not showing a headshot, but three color bars in a square 
	user preferences (square vs image, distance of dragons from one another, ext)
	ability to rearrange order dragons within layers
'''


"""
		################################################
							TO DO 
		Then either move on with development or, maybe,
		take some time to make things better organized
		to prevent another mess like this happening.
		
		Idea, display object like dragon object, but
		just contains all sorts of things for displaying
						 *hint hint*
		################################################
		"""


	
		
	
#######################


# create a class to build and manage the display
class DisplayApp:

	def __init__(self, width, height):

		# create a tk object, which is the root window
		self.root = tk.Tk()

		# width and height of the window
		self.initDx = width
		self.initDy = height
		
		#important feilds.	I am sorry there are so many, but they make life so much easier
		self.view = v.View()	# view object
		#self.axisPoints = np.matrix([[]]) # matrix for points for axis, axes, why is pluralizing words in English so stupid?
		#self.axisLines = []		# Line objects for Axes
		#self.axisLabels = []	# Text Labels objects for Axes
		self.axisIndicator=tk.StringVar()	# used to display current axis values
		self.dataList = {}	# dictionary of all data objects gathered from opened files and PCSData objects created.  The key is the string name of the object
		self.dataSelect ='' # dictionary key of data set which is currently active
		self.xDat = None	# DataColID of column currently used for x axis
		self.yDat = None	# DataColID of column currently used for y axis
		self.zDat = None	# DataColID of column currently used for z axis
		self.sizeDat = None # DataColID of column currently used for size axis
		self.sizeList = []	# List of sizes
		self.colorDat = None# DataColID of column currently used for color axis
		self.colorList = [] # List of color strings
		self.data = None	# np matrix of the x, y and z data currently being displayed
		self.dataPoints = []# List of Oval Objects representing the data which is being displayed
		self.dataListbox = None # Listbox containing the names of the files which are currently open
		self.PCAListbox = None	# Listbox containing the names of the PCAs
		self.pointSelect = None # index of point currently selected
		self.pointSelText = tk.StringVar()	# text representing the data values of a certain point
		self.hoverDrag = None # dragon you hover over when comparing liniages n stuff
		self.horizontalGap = 160/2 +20
		self.verticalGap = 180/2 + 10
		
		"""###################"""
		self.dragons = dd.Data()
		self.imageKey = {} #key, the dragon image objects (numbers), result, the dragon objects (objects)
		self.colorData = {} # all colors, with string names as keys [Oficial num int, string hex value]
		self.colorList = ["Maize","White","Ice","Platinum","Silver","Gray","Charcoal","Coal","Black","Obsidian","Midnight","Shadow","Mulberry","Thistle","Lavender","Purple","Violet","Royal","Storm","Navy","Blue","Splash","Sky","Stonewash","Steel","Denim","Azure","Caribbean","Teal","Aqua","Seafoam","Jade","Emerald","Jungle","Forest","Swamp","Avocado","Green","Leaf","Spring","Goldenrod","Lemon","Banana","Ivory","Gold","Sunshine","Orange","Fire","Tangerine","Sand","Beige","Stone","Slate","Soil","Brown","Chocolate","Rust","Tomato","Crimson","Blood","Maroon","Red","Carmine","Coral","Magenta","Pink","Rose"]
		self.photo = []
		self.totalX = 0
		self.totalY = 0
		self.frame=None
		self.panelCanvas = None
		self.selectedColor = []
		self.posibleColor = [[],[],[]]
		self.offset = 0 #for opening different sets when adding stuff because ness
		self.rarityTable = [["50/50","70/30","85/15","97/3","99/1"],
							["30/70","50/50","75/25","90/10","99/1"],
							["15/85","25/75","50/50","85/15","98/2"],
							["3/97","10/90","15/85","50/50","97/3"],
							["1/99","1/99","2/98","3/97","50/50"]]
		
		# set up the geometry for the window
		self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

		# set the title of the window
		self.root.title("Dragon Datatron 9000")# May it's reign of terror be merciful

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
		
		"""
		#############################################
		"""
		# load color data
		fobj = file("colorInfo.txt")
		lines = fobj.readlines()
		fobj.close()
		
		if len(lines) == 1:
			lines = lines[0].split("\r")
		for line in lines:
			words = line.strip().split(",")
			words[0] = int(words[0])
			self.colorData[words[1]] = [words[0],words[2]]
		print self.colorData
		
		#self.dragonRects.append(self.canvas.create_rectangle( 10,200 , 30,220, fill='#AAAAAA'))
		#self.dragonRects.append(self.canvas.create_image( 100,200, image=photo1, anchor=tk.NE))
		self.frame = self.canvas.create_rectangle( 100,100 , 175,175,outline="green", width = 10,state=tk.HIDDEN)
		
		
		
	
		# not sure about how to access dragon object when clicking rect either.
		# Yet another hash map?
		# long drawn out coordinate searching?
		#	Probably this as a current measure to get things working
		
		# Oh my god it's full of numbers!
		# when you get a shape object it's just a number referring to when it was made!
		# so assosiating numbers and dragons should be easy, just requiring braining
		
		# so long strate up in order list for getting the dragon from being clicked on
		# one dictionary with gen keys for initial display making and additions
		# one dictionary by ID just in case I'm sure there is a reason I am not remembering.
		
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
		# the second sublist is the set of items for the option menu
		menutext = [ [ 'Open	\xE2\x8C\x98-O', '-', 'Save	\xE2\x8C\x98-S', '-', 'Quit	\xE2\x8C\x98-Q' ],
					 [ 'Reset		\xE2\x8C\x98-R','Center X	\xE2\x8C\x98-X', 'Center Y	\xE2\x8C\x98-Y', 'Center Z	\xE2\x8C\x98-Z' ]]

		# menu callback functions (note that some are left blank,
		# so that you can add functions there if you want).
		# the first sublist is the set of callback functions for the file menu
		# the second sublist is the set of callback functions for the option menu
		menucmd = [ [self.handleOpen, None, self.handleSave, None, self.handleQuit],
					[self.reset, self.centerX, self.centerY, self.centerZ]]
		
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

		### Control ###
		# make a control frame on the right
		rightcntlframe = tk.Frame(self.root)
		rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

		# make a separator frame
		sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Control Panel", width=20, font = ("arial",18) )
		label.pack( side=tk.TOP, pady=10 )
		
		button5 = tk.Button( rightcntlframe, text="Add Dragon", 
							   command=self.handleNewDragon )
		button5.pack(side=tk.TOP)
		
		# Moderatly useless
		button4 = tk.Button( rightcntlframe, text="Do Not Click", 
							   command=self.handleButton4 )
		button4.pack(side=tk.TOP, pady=5)
		
		
		
		self.button3 = tk.Button( rightcntlframe, text="Edit Dragon", 
							   command=self.handleEditDragon ,state=tk.DISABLED)
		self.button3.pack(side=tk.TOP, pady=5)
		
		self.button2 = tk.Button( rightcntlframe, text="Exault Dragon", 
							   command=self.handleExaultDragon ,state=tk.DISABLED)
		self.button2.pack(side=tk.TOP, pady=5)
		
		# Selected Point section contains information pertaining to a selected point
		self.pointSelText.set("No Dragon selected")
		label = tk.Label( rightcntlframe, width=20, textvariable=self.pointSelText,justify=tk.LEFT )
		label.pack( side=tk.TOP)
		
		self.panelCanvas = tk.Canvas(rightcntlframe, width=186, height=96,bg="white")
		self.panelCanvas.pack(side=tk.TOP, pady=5)
		
		self.selectedColor.append(self.panelCanvas.create_rectangle( 10,10 , 60,90, fill='blue',state=tk.HIDDEN))
		self.selectedColor.append(self.panelCanvas.create_rectangle( 70,10 , 120,90, fill='blue',state=tk.HIDDEN))
		self.selectedColor.append(self.panelCanvas.create_rectangle( 130,10 , 180,90, fill='blue',state=tk.HIDDEN))
		
		#self.panelCanvas.create_rectangle( 10,10 , 60,30, fill='blue')
		#self.panelCanvas.create_rectangle( 10,40 , 60,60, fill='blue')
		#self.panelCanvas.create_rectangle( 10,70 , 60,90, fill='blue')
		#34
		
		
		for i in range(34):
			self.posibleColor[0].append(self.panelCanvas.create_rectangle( 10+5*i,10 , 13+5*i,30, fill="blue",outline='blue',state=tk.HIDDEN))
			self.posibleColor[1].append(self.panelCanvas.create_rectangle( 10+5*i,40 , 13+5*i,60, fill="blue",outline='blue',state=tk.HIDDEN))
			self.posibleColor[2].append(self.panelCanvas.create_rectangle( 10+5*i,70 , 13+5*i,90, fill="blue",outline='blue',state=tk.HIDDEN))
		
		
		
		
		self.dragonText = tk.Text(rightcntlframe, height=10, width =20,wrap=tk.WORD,takefocus=True,relief = tk.SUNKEN)
		self.dragonText.pack(side=tk.TOP, pady=5)
		
		
		
		
		
		
		return
		
		
		
		
		
		
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
		self.root.bind( '<Command-y>', self.centerY )
		self.root.bind( '<Command-x>', self.centerX )
		self.root.bind( '<Command-z>', self.centerZ )




###############################
#stuff related to data and display and data display

	# This functon should be called whenever the view is changed and there is data, as it changes the data to reflect the view.
	def updataData(self):
		vtm = self.view.build()
		newPoints =(vtm*self.data.T).T
		for i in range(len(self.dataPoints)):
			self.canvas.coords(self.dataPoints[i], newPoints[i,0]-self.sizeList[i],newPoints[i,1]-self.sizeList[i] , newPoints[i,0]+self.sizeList[i],newPoints[i,1]+self.sizeList[i])

			
	
	#This function handles the opening of a data file, and the storage of the information in that file
	def handleOpen(self, event = None):
		#delete previous stuff, if any
		
		self.offset+=len(self.dragons.dragonList)
		self.canvas.lower(self.frame)
		allStuff=self.canvas.find_all()
		for item in allStuff[1:]:
			self.canvas.delete(item)
		
		self.dragonRects = [] #obsolete, kept for testing purposes
		self.linkLines = [] # lines linking dragon squares.	 All come in pairs, linking a dragon to it's mother and father
		self.photo = []
		self.totalX = 0
		self.totalY = 0
		
		# reset selected dragon
		self.handleMouseButton1()
		
		fn = tkFileDialog.askopenfilename( parent=self.root, title='Choose a data file', 
					 initialdir='.' )
		if fn == '':
			return
		name = fn.split('/')[-1]
		
		# import starting dragons and build beginning tree.
		
		self.dragons = dd.Data(name)
		
		#photo1 = tk.PhotoImage(file="1.gif")
		#self.photo.append(photo1)
		
		# add the rectangles, and make a plain list of dragons, which is important for rect drawing, and line linking?
		levels = self.dragons.genMap.keys()
		levels.sort()
		
		for i in range(len(levels)):
			for j in range(len(self.dragons.genMap[levels[i]])):
				self.imageKey[self.dragons.genMap[levels[i]][j].visuals.assemble(100+self.horizontalGap*j,100+self.verticalGap*i, self.canvas)]=self.dragons.genMap[levels[i]][j]
		
		#stop displating exalted dragons
		keys = self.dragons.IDmap.keys()
		for key in keys:
			if self.dragons.IDmap[key].exalt:
				self.removeDragonFromDisplay(self.dragons.IDmap[key])
		
	def handleSave(self, event = None):
		print "Save!"
		
		fn = tkFileDialog.asksaveasfilename( defaultextension = ".drg",parent=self.root, title='Choose a data file', 
					 initialdir='.' )
		if fn == '':
			return
		
		self.dragons.saveInFile(fn)
		
		
		
		
	
	#This function allows the user to choose what column of data is desplayed on what axis
	# it then prosses those choices in ways that allows the data to easily be displayed
	def handleNewDragon(self, event = None):
		box = dialogs.AddDragonDialog(self.root, self.dragons)
		par = box.result
		print par
		if (box.result[2]=="" or box.result[3]==""):
			print "ERROR: Please include a name and ID number"
			return
		print "Everything checks out."
		
		# assigne gender
		if par[4] == "Female":
			gender = True
		else:
			gender = False
		
		
		#I'm moving dragon creation out here for now, for more sensible stuff
		if (int(par[0]) == 0) or (int(par[1]) == 0):
			mother = None
			father = None
		else:
			mother = self.dragons.IDmap[int(par[0])]
			father = self.dragons.IDmap[int(par[1])]
		
		
		new = dd.Dragon( int(par[3]), par[2], 1, None, None, False, gender, par[5], [par[6],par[8],par[10]], [par[7],par[9],par[11]], par[12])
		self.dragons.add(new, mother, father)
		
		i = new.gen-1
		j = len(self.dragons.genMap[new.gen])-1 
		
		self.imageKey[new.visuals.assemble(100+self.horizontalGap*j+self.totalX, 100+self.verticalGap*i+self.totalY, self.canvas)] = new
		
		
	
	def handleEditDragon(self, event = None):
		box = dialogs.EditDragonDialog(self.root, self.dragons, self.pointSelect)
		par = box.result
		print par
		if box.result[0]=="":
			print "ERROR: Please include a name"
			return
		self.pointSelect.name = box.result[0]
		self.pointSelect.species = box.result[1]
		self.pointSelect.colors[0] = box.result[2]
		self.pointSelect.genes[0] = box.result[3]
		self.pointSelect.colors[1] = box.result[4]
		self.pointSelect.genes[1] = box.result[5]
		self.pointSelect.colors[2] = box.result[6]
		self.pointSelect.genes[2] = box.result[7]
		self.pointSelect.notes = box.result[8]
		print box.result
		
		self.updateDragonSide()
			
	def handleExaultDragon(self, event = None):
		box = dialogs.ExaultDragonDialog(self.root, self.pointSelect)
		if box.result:
			self.removeDragonFromDisplay(self.pointSelect)
		
	def removeDragonFromDisplay(self, dragon):
		for child in dragon.decendants[0]:
			# was a mother
			if dragon.gender:
				child = self.dragons.IDmap[child]
				if not child.exalt:
					child.visuals.removeMother(self.canvas)
			# was a father
			else:
				child = self.dragons.IDmap[child]
				if not child.exalt:
					child.visuals.removeFather(self.canvas)
		'''Issues with fully removing object, neet to resolve with better algorithm'''
		self.dragons.exault(dragon)
		
		del self.imageKey[dragon.visuals.image]
		dragon.visuals.remove(self.canvas)
		
		self.pointSelect = None
		self.resetDragonSide()

##########################
# interaction functions bound to the root

	
	# Quit
	def handleQuit(self, event=None):
		print 'Terminating'
		self.root.destroy()

	# resets the view to the origional view.
	def reset(self, event = None):
		self.view.reset()
		#self.updateAxes()
		if self.data != None:
			self.updataData()
		
	# centers the Z axis, giving a 2D view along the x and y
	def centerZ(self, event = None):
		self.view.vpn = np.matrix([[0, 0, -1]])
		self.view.vup = np.matrix([[0, 1, 0]])
		self.view.u = np.matrix([[-1, 0, 0]])
		#self.updateAxes()
		if self.data != None:
			self.updataData()
		
	# centers the X axis, giving a 2D view along the z and y
	def centerX(self, event = None):
		self.view.vpn = np.matrix([[1, 0, 0]])
		self.view.vup = np.matrix([[0, 1, 0]])
		self.view.u = np.matrix([[0, 0, -1]])
		#self.updateAxes()
		if self.data != None:
			self.updataData()
		
	# centers the Y axis, giving a 2D view along the x and z
	def centerY(self, event = None):
		self.view.vpn = np.matrix([[0, -1, 0]])
		self.view.vup = np.matrix([[1, 0, 0]])
		self.view.u = np.matrix([[0, 0, -1]])
		#self.updateAxes()
		if self.data != None:
			self.updataData()
	
	
	
############################
# interaction functions bound to buttons or menues
	
	
		
	

	# When this button is pressed, a sarcastic message appears on the screen and in the terminal
	def handleButton4(self):
		w = tk.Message(self.canvas, text="Now look what you've done",width=100)
		w.config(background="red")
		w.pack(side=tk.TOP)
		print 'Your inability to follow simple instructions has been noted.'
		
	

############################
# interaction functions bound to the canvas, mostly pertaining to the mouse and it's motion

	def updateDragonSide(self):
		for i in range(len(self.posibleColor)):
			for j in range(len(self.posibleColor[i])):
				self.panelCanvas.itemconfig(self.posibleColor[i][j], state = tk.HIDDEN)
		if self.hoverDrag != None:
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
			
			self.hoverDrag.visuals.related = False
			self.canvas.itemconfig(self.hoverDrag.visuals.rect, outline="black",width=1)
			self.hoverDrag = None
			
			
		if self.pointSelect.motherDragon == None:
			motherName = "None"
		else:
			motherName = self.pointSelect.motherDragon.name
			
		if self.pointSelect.fatherDragon == None:
			fatherName = "None"
		else:
			fatherName = self.pointSelect.fatherDragon.name
			
		if self.pointSelect.gender:
			gender = "Female"
		else:
			gender = "Male"
		
			
		self.pointSelText.set("Dragon Info\r\rName: %s" %(self.pointSelect.name)+
										  "\rID: %d" %(self.pointSelect.id)+
										  "\rName: %s" %(gender)+
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

		self.panelCanvas.itemconfig(self.selectedColor[0], fill=self.colorData[self.pointSelect.colors[0]][1],state = tk.NORMAL)
		self.panelCanvas.itemconfig(self.selectedColor[1], fill=self.colorData[self.pointSelect.colors[1]][1],state = tk.NORMAL)
		self.panelCanvas.itemconfig(self.selectedColor[2], fill=self.colorData[self.pointSelect.colors[2]][1],state = tk.NORMAL)
		
		self.dragonText.config(state=tk.NORMAL)
		self.dragonText.delete(1.0, tk.END)
		self.dragonText.insert(tk.END,self.pointSelect.notes)
		self.dragonText.config(state=tk.DISABLED)
		
	def compareDragonSide(self):
		self.panelCanvas.itemconfig(self.selectedColor[0], state = tk.HIDDEN)
		self.panelCanvas.itemconfig(self.selectedColor[1], state = tk.HIDDEN)
		self.panelCanvas.itemconfig(self.selectedColor[2], state = tk.HIDDEN)
		
		for i in range(3):
			# re set previous, so no old color range is showing (can be a problem with quick switches that do not trigger re-set)
			for j in range(len(self.posibleColor[i])):
				self.panelCanvas.itemconfig(self.posibleColor[i][j], state = tk.HIDDEN)
		
			if (self.pointSelect.gender == self.hoverDrag.gender):
				self.pointSelText.set("Imcompatible match:\nGender mismatch.")
				return 
				
			ansestorClash = ""
			
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
			
			if ansestorClash != "":
				self.pointSelText.set("Imcompatible match:\nCommon ansestors:\n"+ansestorClash)
				return
			
			else:
				self.pointSelText.set("Compatible match!")
				up = max(self.colorData[self.pointSelect.colors[i]][0],self.colorData[self.hoverDrag.colors[i]][0])
				low = min(self.colorData[self.pointSelect.colors[i]][0],self.colorData[self.hoverDrag.colors[i]][0])
		
				if (up - low) > 33:
					start = low
					end = up
				else:
					start = up
					end = low
				j = 0
				# count down colors from the higher one, sort of
				while self.colorData[self.colorList[end-1]][1] != self.colorData[self.colorList[start-j-1]][1]:
					self.panelCanvas.itemconfig(self.posibleColor[i][j], outline = "black",fill=self.colorData[self.colorList[start-j-1]][1],state = tk.NORMAL)
					j+=1
				# be sure to include the last one
				self.panelCanvas.itemconfig(self.posibleColor[i][j], outline = "black",fill=self.colorData[self.colorList[start-j-1]][1],state = tk.NORMAL)
		
		
	# blanks the side panel, for when no dragon is selected
	def resetDragonSide(self):
		self.pointSelText.set("No Dragon selected")
		for i in range(len(self.posibleColor)):
			for j in range(len(self.posibleColor[i])):
				self.panelCanvas.itemconfig(self.posibleColor[i][j], state = tk.HIDDEN)
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
			self.hoberDrag = None
		self.panelCanvas.itemconfig(self.selectedColor[0], state = tk.HIDDEN)
		self.panelCanvas.itemconfig(self.selectedColor[1], state = tk.HIDDEN)
		self.panelCanvas.itemconfig(self.selectedColor[2], state = tk.HIDDEN)
	
		self.dragonText.config(state=tk.NORMAL)
		self.dragonText.delete(1.0, tk.END)
		self.dragonText.config(state=tk.DISABLED)
		self.button3.config(state=tk.DISABLED)
		self.button2.config(state=tk.DISABLED)
	
	
	# when you move around the mouse, if a dragon is selected, hover over a dragon to see mating result.	
	def handleMouseMotion(self, event):
		# hovering over something and  dragon is selected
		if (self.canvas.find_overlapping(event.x,event.y,event.x,event.y) != ()) and (self.pointSelect != None):
			point = self.canvas.find_overlapping(event.x,event.y,event.x,event.y)[-1]
			# hovering over a dragon, wow!
			if point in self.imageKey:
				# hovering over original dragon
				if self.pointSelect.id == self.imageKey[point].id:
					return
				# actually two dragons, so display results (add compatibility test in here somewhere)
				else:
					#hypothetically, preform history/gender analysis here, then act on results.  right now, working on positive 
					self.hoverDrag = self.imageKey[point]
					self.compareDragonSide()
		# not hovering over a dragon or no dragon is currently selected
		else:
			if self.pointSelect == None:
				self.resetDragonSide()
			else:
				self.updateDragonSide()
		#print 'not fancy'
			
	# records the base click for moving the view
	# also handles the selection of a point of data
	# this is actually what is triggered on double click.  
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
			if point in self.imageKey:
				self.pointSelect = self.imageKey[point]
				self.canvas.itemconfig(self.pointSelect.visuals.rect, outline="green",width=10)	
				self.updateDragonSide()
				self.button3.config(state=tk.NORMAL)
				self.button2.config(state=tk.NORMAL)
	
	#helper, since mouse button 1 is now a double click really
	def handleMouseButton1MotionStart(self, event):
		self.baseClick = (event.x, event.y)
	
	# moves the data on the screen as the mouse is moved.
	def handleMouseButton1Motion(self, event):
		dx = event.x - self.baseClick[0]
		dy = event.y - self.baseClick[1]
		du = float(dx)/self.view.screen[0]*self.view.extent[0]
		dup =float(dy)/self.view.screen[1]*self.view.extent[1]
		self.view.vrp = self.view.vrp + du * self.view.u + dup * self.view.vup
		self.baseClick = event.x,event.y
		#self.updateAxes()
		if self.data != None:
			self.updataData()
		
		"""########################"""
		
		self.totalX+=dx
		self.totalY+=dy
		print self.totalX
		print self.totalY
		
		loc = self.canvas.coords(self.frame)
		self.canvas.coords( self.frame, loc[0] + dx, loc[1] + dy, loc[2] + dx, loc[3] + dy )
		
		# move the dragons, frames, and the link lines
		for drag in self.dragons.dragonList:
			point = drag.visuals.rect
			loc = self.canvas.coords(point)
			self.canvas.coords( point, 
						loc[0] + dx, 
						loc[1] + dy, 
						loc[2] + dx,
						loc[3] + dy )
			
			point = drag.visuals.image
			loc = self.canvas.coords(point)
			self.canvas.coords( point, 
						loc[0] + dx, 
						loc[1] + dy )
			
			line = drag.visuals.leftLine
			loc = self.canvas.coords(line)
			self.canvas.coords( line, 
						loc[0] + dx, 
						loc[1] + dy, 
						loc[2] + dx,
						loc[3] + dy )
			
			line = drag.visuals.rightLine
			loc = self.canvas.coords(line)
			self.canvas.coords( line, 
						loc[0] + dx, 
						loc[1] + dy, 
						loc[2] + dx,
						loc[3] + dy )
	
		
	# records base click and base view for zooming
	def handleMouseButton3(self, event):
		self.baseClick = (event.x, event.y)
		self.baseView = self.view.clone()
			
	# zooming
	# moving the mouse up the screen makes things bigger, moving it down the screen makes them smaller.
	def handleMouseButton3Motion(self, event):
		dy = float(event.y-self.baseClick[1])
		scale_factor = 1 + dy*.005
		if scale_factor > 3:
			scale_factor = 3
		if scale_factor < .1:
			scale_factor = .1
		self.view.extent[0] = self.baseView.extent[0] * scale_factor
		self.view.extent[1] = self.baseView.extent[1] * scale_factor
		#self.updateAxes()
		if self.data != None:
			self.updataData()


	# records base click and base view for rotation
	def handleMouseButton2(self, event):
		self.baseClick = (event.x, event.y)
		self.baseView = self.view.clone()
	
	# handles the acutall rotation of the view.
	# moving the mouse horizontally rotates around the VUP view axis, moving it vertically rotates around the U view axis
	def handleMouseButton2Motion(self, event):
		dx = event.x - self.baseClick[0]
		dy = event.y - self.baseClick[1]
		delta0 = dx*3.1415/500
		delta1 = dy*3.1415/500
		self.view=self.baseView.clone()
		self.view.rotateVRC(-delta0,delta1)
		#self.updateAxes()
		if self.data != None:
			self.updataData()
	

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
		
		
		

		
		
		

		



