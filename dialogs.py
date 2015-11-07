# Author: Lizzie Tonkin
# Last edited: Oct 3, 2015
# Setup for the various dialog boxes in their own file to prevent clutter in other files.  



import Tkinter as tk
import datetime

##########################
# Dialog box class
# coppied from effbot, modified to personal use.
# I have no idee what most of this means anyway, so no comments besides what was originally there
class Dialog(tk.Toplevel):

	def __init__(self, parent, title = None):

		tk.Toplevel.__init__(self, parent)
		self.transient(parent)

		if title:
			self.title(title)

		self.parent = parent
		body = tk.Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)

		self.buttonbox()

		self.grab_set()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))

		self.initial_focus.focus_set()
		self.maxsize( 16000, 9000 )
		self.wait_window(self)

	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden

		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = tk.Frame(self)

		w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()

		self.apply()

		self.cancel()

	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	#
	# command hooks

	def validate(self):

		return 1 # override

	def apply(self):

		pass # override


################







# The dialog box that allows users to add a new dragon
# dragonData is the Data object from dragonData2
# results are placed in the result field, which is a list
#	results is structured as follows []
class AddDragonDialog(Dialog):
	def __init__(self, parent, dragonData, title = "Dragon Adder 9000"):
		self.dragonData=dragonData # dragon data structure
		self.listboxList = [] # list of all the option boxes
		self.result = [] # where results are stored
		Dialog.__init__(self, parent, title)
		
	# we need a different then default bottonbox because the silly OK event binding was causing havoc on the enter key in the notes section 
	# just stops the return button from being bound to the OK button
	def buttonbox(self):
		box = tk.Frame(self)

		w = tk.Button(box, text="OK", width=10, command=self.ok)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		#self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()
	
	
	# builds what the dialog box looks like.
	def body(self, master):
		# due to legacy reasons the parental options are doen first, and then the other options in the order they appear on the box.
		# they are stored in the result section the same way.  I am sorry for the confusion
		
		# Set up potential parents:
		# lists of female and male dragon IDs, with labels as the first entries.
		females = ["Mother:"]
		males = ["Father:"]
		# sort all dragons into the two lists
		for dragon in self.dragonData.dragonList:
			if dragon.matingType:
				females.append(dragon.id)
			else:
				males.append(dragon.id)
		parents = [females,males]
		
		# i is five because parental options will end up starting in the fifth row
		i =6
		
		# for both of the lists of parents
		for list in parents:
			# create and display a label using the first entry in the list
			label = tk.Label( master, text=list[0], width=10 )
			label.grid( row=i, column=0 )
			
			# create the dropdown menue variables and set the initial value to 0
			parentOption = tk.StringVar( master )
			parentOption.set(0)
			
			if len(list) < 2:
				# if a list is less than two, there are no dragons of the matingType being looked at
				# so create a parent menue with only 0 as an option, signifying no dragon
				parentMenu = tk.OptionMenu (master, parentOption,"0")
			else:
				# otherwise, set the OptionMenu options to be the parent list (sans the first entry, of course)
				parentMenu = apply(tk.OptionMenu, (master, parentOption) + tuple(list[1:]))
			
			# add the option to the places it needs to be (displayed in the grid and in the list of option thingies)
			parentMenu.grid( row=i, column=1, columnspan=2,sticky="ew")
			self.listboxList.append(parentOption)
			i+=1
			
		# goodness this is a mess, but for some reason it was not working in the loop
		# This is stuff so that the name of dragon of the selected ID shows up shows up beside it, because we do not have our dragon's IDs memorized
		
		# set up the string variables and make the initial value None
		motherName = tk.StringVar( master )
		motherName.set("None")
		fatherName = tk.StringVar( master )
		fatherName.set("None")
		
		# I have no idea what is going on here anymore.  I should have left comments originally
		# I think we are creating a function which takes in a list of arguments, and then 
		# Changes the corresponding StringVar to the Name of whatever ID has been selected by the optionMenues above
		def showName(*args):
			print "variable changed to "+str(self.listboxList[0].get())
			motherName.set(self.dragonData.IDmap[int(self.listboxList[0].get())].name)
		
		def showName2(*args):
			print "variable changed to "+str(self.listboxList[1].get())
			fatherName.set(self.dragonData.IDmap[int(self.listboxList[1].get())].name)
		
		# Set the optionMenues so that every time they change they call the proper showName function
		self.listboxList[0].trace("w", showName)
		self.listboxList[1].trace("w", showName2)
		
		# place the darn things in their proper places in the grid
		label = tk.Label( master, width=10, textvariable=motherName )
		label.grid( row=i-2, column=3)
		
		label = tk.Label( master, width=10, textvariable=fatherName )
		label.grid( row=i-1, column=3)
			
			
			
		# OK, we are back to creating and adding things in the order they are displayed
			
		# Name with free entry
		label = tk.Label( master, text="Name:", width=10 )
		label.grid( row=0, column=0)
		name = tk.Entry(master, width = 10)
		name.grid( row=0, column=1, columnspan=2)
		self.listboxList.append(name)
		
		# ID with free entry
		label = tk.Label( master, text="ID number:", width=10 )
		label.grid( row=1, column=0)
		id = tk.Entry(master, width = 10)
		id.grid( row=1, column=1, columnspan=2)
		self.listboxList.append(id)
		
		
		# hatchday, the day the dragon was born
		date = datetime.date.today()
		
		label = tk.Label( master, text="Hatch Day:", width=10 )
		label.grid( row=2, column=0)
		hatchMonthOption = tk.StringVar( master )
		hatchMonthOption.set(date.month)
		hatchMonthMenu = tk.OptionMenu( master, hatchMonthOption, 
			"1","2","3","4",'5',"6",'7','8','9','10','11','12' ) # Note to self, can add a command to the menu.  Just a thought for the future. 
		hatchMonthMenu.config(width=5)
		hatchMonthMenu.grid( row=2, column=1)
		
		hatchDayOption = tk.StringVar( master )
		hatchDayOption.set(date.day)
		hatchDayMenu = tk.OptionMenu( master, hatchDayOption, 
			"1","2","3","4",'5',"6",'7','8','9','10',"11","12","13","14",'15',"16",'17','18','19','20',"21","22","23","24",'25',"26",'27','28','29','30','31' ) # Note to self, can add a command to the menu.  Just a thought for the future. 
		hatchDayMenu.config(width=5)
		hatchDayMenu.grid( row=2, column=2)
		
		allYears = range(2010,int(date.year)+1)
		hatchYearOption = tk.StringVar( master )
		hatchYearOption.set(date.year)
		hatchYearMenu = apply(tk.OptionMenu, (master, hatchYearOption) + tuple(allYears))
		hatchYearMenu.grid( row=2, column=3)
		
		# Postpone adding to listbox list for minimal disruption
		#self.listboxList.append(matingTypeOption)
				
		
		
		# matingType, with a drop-down menue with two options, Male and Female
		label = tk.Label( master, text="Mating Type:", width=10 )
		label.grid( row=3, column=0)
		matingTypeOption = tk.StringVar( master )
		matingTypeOption.set("Female")
		matingTypeMenu = tk.OptionMenu( master, matingTypeOption, 
			"Female","Male" ) # Note to self, can add a command to the menu.  Just a thought for the future. 
		matingTypeMenu.grid( row=3, column=1, columnspan=2,sticky="ew")
		self.listboxList.append(matingTypeOption)
		
		# breed, with dropdown menue listing all the current breeds, in order like at predict Morphology
		label = tk.Label( master, text="Breed:", width=10 )
		label.grid( row=4, column=0)
		breedOption = tk.StringVar( master )
		breedOption.set("Fae")
		breedMenu = tk.OptionMenu( master, breedOption, 
			"Fae","Guardian","Mirror","Pearlcatcher","Ridgeback","Tundra","Spiral","Imperial","Snapper","Wildclaw","Nocturne","Coatl","Skydancer" )
		breedMenu.grid( row=4, column=1, columnspan=2,sticky="ew")
		self.listboxList.append(breedOption)
		
		# add a line separating the above from the the next set of info
		sep = tk.Frame( master, height=2, width = 300, bd=1, relief=tk.SUNKEN )
		sep.grid(row=5,columnspan=4)	
		
		# parent selection happens here
		
		# add a divider between the parent information and the gene information
		sep = tk.Frame( master, height=2, width = 300, bd=1, relief=tk.SUNKEN )
		sep.grid(row=i,columnspan=4)
		i+=1
		
		# make primary, secondary, and tertiary sections for and genes.  Not colors because they are always the same.
		titleList = ["Primary:","Secondary:","Tertiary:"]
		geneListList = [["Basic","Iridescent","Tiger","Clown","Speckle","Ripple","Bar","Crystal","Vipera","Piebald","Cherub"],
						["Basic","Shimmer","Stripes","Eye Spots","Freckle","Seraph","Current","Daub","Facet","Hypnotic","Paint","Peregrine"],
						["Basic","Circuit","Gembond","Underbelly","Crackle","Smoke","Spines","Okapi","Glimmer"]]
		
		# for the three levels
		for title in titleList:
			# make a nice label and display it
			label = tk.Label( master, text=title, width=10 )
			label.grid( row=i, column=0)
			# create the color option menue, display it, and save it in the list of listboxes
			colorOption = tk.StringVar( master )
			colorOption.set("Maize")
			colorMenu = tk.OptionMenu( master, colorOption, 
				"Maize","White","Ice","Platinum","Silver","Gray","Charcoal","Coal","Black","Obsidian","Midnight","Shadow","Mulberry","Thistle","Lavender","Purple","Violet","Royal","Storm","Navy","Blue","Splash","Sky","Stonewash","Steel","Denim","Azure","Caribbean","Teal","Aqua","Seafoam","Jade","Emerald","Jungle","Forest","Swamp","Avocado","Green","Leaf","Spring","Goldenrod","Lemon","Banana","Ivory","Gold","Sunshine","Orange","Fire","Tangerine","Sand","Beige","Stone","Slate","Soil","Brown","Chocolate","Rust","Tomato","Crimson","Blood","Maroon","Red","Carmine","Coral","Magenta","Pink","Rose" ) # can add a command to the menu
			colorMenu.grid( row=i, column=1, columnspan=2,sticky="ew")
			self.listboxList.append(colorOption)
			
			# do the same thing with the genes, but with the already created lists!
			geneOption = tk.StringVar( master )
			geneOption.set("Basic")
			geneMenu = apply(tk.OptionMenu, (master, geneOption) + tuple(geneListList[i%3]))
			geneMenu.grid( row=i, column=3,sticky="ew")
			self.listboxList.append(geneOption)
			i+=1
		
		# add another divider
		sep = tk.Frame( master, height=2, width = 300, bd=1, relief=tk.SUNKEN)
		sep.grid(row=i,columnspan=4)
		i+=1
		
		# add another divider, but we are going to put the textbox inside this one, so it looks pretty
		sep = tk.Frame( master, height=200, width = 300, bd=1, relief=tk.SUNKEN )
		sep.grid(row=i,columnspan=4)
		i+=1
		
		# the afore mentioned textbox
		self.text = tk.Text(sep, height=10, width =40,wrap=tk.WORD,takefocus=True,relief = tk.SUNKEN)
		self.text.grid(row=i, column=0, columnspan=4)
		
		
		#add the date and times now
		self.listboxList.append(hatchDayOption)
		self.listboxList.append(hatchMonthOption)
		self.listboxList.append(hatchYearOption)
		
	# send the results to a place where they can be retrieved.
	def apply(self):
		# get the value of all the listboxes and put them in the results field
		for box in self.listboxList:
			self.result.append(box.get())
		# text is weird, so get a string of all of it and put that in the results too 
		self.result.append(str(self.text.get("0.0",tk.END)))
		



		


# The dialog box that allows users to change the changeable information of their dragon
# some information is not changeable, such as ID and mating type, so that cannot be changed here.
class EditDragonDialog(Dialog):
	def __init__(self, parent, dragonData, curDrag, title = "Dragon Editer 9000"):
		self.dragonData=dragonData
		self.curDrag = curDrag
		self.listboxList = []
		self.result = []
		Dialog.__init__(self, parent, title)
		
	# we need a different then default bottonbox because the silly OK event binding was causing havoc on the enter key in the notes section 
	# just stops the return button from being bound to the OK button
	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = tk.Frame(self)

		w = tk.Button(box, text="OK", width=10, command=self.ok)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		#self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()
	
	# builds what the dialog box looks like.
	def body(self, master):
		
		# pretty much the same procedure as above, except we skip all the fields that cannot be changed
		# (ID, Mating Type, Birthday, Parents)
		
		# Name with free entry
		label = tk.Label( master, text="Name:", width=10 )
		label.grid( row=0, column=0)
		name = tk.Entry(master, width = 10)
		name.insert(0, self.curDrag.name)
		name.grid( row=0, column=1, columnspan=2,sticky="ew")
		self.listboxList.append(name)
		
		# ID, which we show because we are polite.  You cannot change it.
		label = tk.Label( master, text="ID number:", width=10 )
		label.grid( row=1, column=0)
		label = tk.Label( master, text=self.curDrag.id, width=10 )
		label.grid( row=1, column=1, columnspan=2,sticky="ew")
		
		
		# hatchday, the day the dragon was born
		date = self.curDrag.hatchDay.split('-')
		today = datetime.date.today()
		
		label = tk.Label( master, text="Hatch Day:", width=10 )
		label.grid( row=2, column=0)
		hatchMonthOption = tk.StringVar( master )
		hatchMonthOption.set(date[1])
		hatchMonthMenu = tk.OptionMenu( master, hatchMonthOption, 
			"1","2","3","4",'5',"6",'7','8','9','10','11','12' ) # Note to self, can add a command to the menu.  Just a thought for the future. 
		hatchMonthMenu.config(width=5)
		hatchMonthMenu.grid( row=2, column=1)
		
		hatchDayOption = tk.StringVar( master )
		hatchDayOption.set(date[0])
		hatchDayMenu = tk.OptionMenu( master, hatchDayOption, 
			"1","2","3","4",'5',"6",'7','8','9','10',"11","12","13","14",'15',"16",'17','18','19','20',"21","22","23","24",'25',"26",'27','28','29','30','31' ) # Note to self, can add a command to the menu.  Just a thought for the future. 
		hatchDayMenu.config(width=5)
		hatchDayMenu.grid( row=2, column=2)
		
		allYears = range(2010,int(today.year)+1)
		hatchYearOption = tk.StringVar( master )
		hatchYearOption.set(date[2])
		hatchYearMenu = apply(tk.OptionMenu, (master, hatchYearOption) + tuple(allYears))
		hatchYearMenu.grid( row=2, column=3)
		
		# Postpone adding to listbox list for minimal disruption
		#self.listboxList.append(matingTypeOption)
		
		
		# Mating Type, which we show because we are polite.  You cannot change it.
		label = tk.Label( master, text="Mating Type:", width=10 )
		label.grid( row=3, column=0)
		if self.curDrag.matingType:
			matingType = "Female"
		else:
			matingType = "Male"
		label = tk.Label( master, text=matingType, width=10 )
		label.grid( row=3, column=1, columnspan=2,sticky="ew")
		
		# breed, with dropdown menue listing all the current breeds, in order like at predict Morphology
		label = tk.Label( master, text="Breed:", width=10 )
		label.grid( row=4, column=0)
		breedOption = tk.StringVar( master )
		breedOption.set(self.curDrag.species)
		breedMenu = tk.OptionMenu( master, breedOption, 
			"Fae","Guardian","Mirror","Pearlcatcher","Ridgeback","Tundra","Spiral","Imperial","Snapper","Wildclaw","Nocturne","Coatl","Skydancer" ) # can add a command to the menu
		breedMenu.grid( row=4, column=1, columnspan=2,sticky="ew")
		self.listboxList.append(breedOption)
		
		i=5 # Because I coppied code, we still do the i thing, still starting at 5
		# divider between the above and the gene color stuff
		sep = tk.Frame( master, height=2, width = 300, bd=1, relief=tk.SUNKEN )
		sep.grid(row=i,columnspan=4)
		i+=1
		
		# make primary, secondary, and tertiary sections for and genes.  Not colors because they are always the same.
		titleList = ["Primary:","Secondary:","Tertiary:"]
		geneListList = [["Basic","Iridescent","Tiger","Clown","Speckle","Ripple","Bar","Crystal","Vipera","Piebald","Cherub"],
						["Basic","Shimmer","Stripes","Eye Spots","Freckle","Seraph","Current","Daub","Facet","Hypnotic","Paint","Peregrine"],
						["Basic","Circuit","Gembond","Underbelly","Crackle","Smoke","Spines","Okapi","Glimmer"]]
						
		# for the three levels
		for title in titleList:
			# make a nice label and display it
			label = tk.Label( master, text=title, width=10 )
			label.grid( row=i, column=0)
			# create the color option menue, display it, and save it in the list of listboxes
			colorOption = tk.StringVar( master )
			colorOption.set(self.curDrag.colors[i%3])
			colorMenu = tk.OptionMenu( master, colorOption, 
				"Maize","White","Ice","Platinum","Silver","Gray","Charcoal","Coal","Black","Obsidian","Midnight","Shadow","Mulberry","Thistle","Lavender","Purple","Violet","Royal","Storm","Navy","Blue","Splash","Sky","Stonewash","Steel","Denim","Azure","Caribbean","Teal","Aqua","Seafoam","Jade","Emerald","Jungle","Forest","Swamp","Avocado","Green","Leaf","Spring","Goldenrod","Lemon","Banana","Ivory","Gold","Sunshine","Orange","Fire","Tangerine","Sand","Beige","Stone","Slate","Soil","Brown","Chocolate","Rust","Tomato","Crimson","Blood","Maroon","Red","Carmine","Coral","Magenta","Pink","Rose" ) # can add a command to the menu
			colorMenu.grid( row=i, column=1, columnspan=2,sticky="ew")
			self.listboxList.append(colorOption)
			
			# do the same thing with the genes, but with the already created lists!
			geneOption = tk.StringVar( master )
			geneOption.set(self.curDrag.genes[i%3])
			geneMenu = apply(tk.OptionMenu, (master, geneOption) + tuple(geneListList[i%3]))
			geneMenu.grid( row=i, column=3,sticky="ew")
			self.listboxList.append(geneOption)
			i+=1
		
		# add another divider
		sep = tk.Frame( master, height=2, width = 300, bd=1, relief=tk.SUNKEN)
		sep.grid(row=i,columnspan=4)
		i+=1
		
		# add another divider, but we are going to put the textbox inside this one, so it looks pretty
		sep = tk.Frame( master, height=200, width = 300, bd=1, relief=tk.SUNKEN )
		sep.grid(row=i,columnspan=4)
		i+=1
		
		# the afore mentioned textbox
		self.text = tk.Text(sep, height=10, width =40,wrap=tk.WORD,takefocus=True,relief = tk.SUNKEN)
		self.text.insert(tk.END,self.curDrag.notes)
		self.text.grid(row=i, column=0, columnspan=4)
		
		#add the date and times now
		self.listboxList.append(hatchDayOption)
		self.listboxList.append(hatchMonthOption)
		self.listboxList.append(hatchYearOption)
		
	# send the results to a place where they can be retrieved.
	def apply(self):
		for box in self.listboxList:
			self.result.append(box.get())
		self.result.append(str(self.text.get("0.0",tk.END)))
		#print self.result
		#print self.result[0].gen
		#print self.text.get("0.0",tk.END)		
		
		
		
		
		
		
		
		
		
# The dialog box that appears when you want to exalt a dragon, asking if you are sure. 
# input curDrag the currently selected Dragon object
# the result field is false if the user decides not to exalt the dragon, true otherwise.
class ExaultDragonDialog(Dialog):
	def __init__(self, parent, curDrag, title = "Dragon Exaulter 9000"):
		self.curDrag = curDrag
		self.result = False
		Dialog.__init__(self, parent, title)
		
	# builds what the dialog box looks like.
	def body(self, master):
		# display only a warning that is modeled after the standard FR warning.
		# Except our patron deity is the DataMuncher.  She gave rise to the PerlCatcher dragon.
		warning = "Exalting " +self.curDrag.name+" to the service of the\nDatamuncher will remove them from your lair\nforever. They will leave behind no riches\nwhatsoever.  This action is irreversible.\n\nDo you wish to continue?"
		label = tk.Label( master, text=warning )
		label.grid( row=0, column=0)
		
	# If Ok, is selected, set the result to true
	def apply(self):
		self.result = True
		
		
		
		
