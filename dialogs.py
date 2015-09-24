import Tkinter as tk

##########################
# Dialog box class
# coppied from effbot, modified to our personal use.
class Dialog(tk.Toplevel):

	def __init__(self, parent, title = None):

		tk.Toplevel.__init__(self, parent)
		self.transient(parent)

		if title:
			self.title(title)

		self.parent = parent

	#	self.result = None

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
#i'll finish it off later when I have proper references
class AddDragonDialog(Dialog):
	def __init__(self, parent, dragonData, title = "Dragon Adder 9000"):
		self.dragonData=dragonData
		self.listboxList = []
		self.result = []
		Dialog.__init__(self, parent, title)
		
	# we need a different then default bottonbox because the silly OK event binding was causing havoc on the enter key in the notes section 
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
		
		# potential parents
		females = ["Mother:"]
		males = ["Father:"]
		for dragon in self.dragonData.dragonList:
			if dragon.gender:
				females.append(dragon.id)
			else:
				males.append(dragon.id)
		parents = [females,males]
		
		i =5
		
		for list in parents:
			if len(list) < 2:
				print "no parents, ha!"
				label = tk.Label( master, text=list[0], width=10 )
				label.grid( row=i, column=0 )
			
				parentOption = tk.StringVar( master )
				parentOption.set(0)
				parentMenu = tk.OptionMenu (master, parentOption,"0")
				parentMenu.grid( row=i, column=1)
				self.listboxList.append(parentOption)
			
				i+=1
			else:
				label = tk.Label( master, text=list[0], width=10 )
				label.grid( row=i, column=0 )
			
				parentOption = tk.StringVar( master )
				parentOption.set(0)
				parentMenu = apply(tk.OptionMenu, (master, parentOption) + tuple(list[1:]))
				parentMenu.grid( row=i, column=1)
				self.listboxList.append(parentOption)
			
				i+=1
			
		# goodness this is a mess, but for some reason it was not working in the loop
		# stuff so that the name of dragon of the selected ID shows up
		
		motherName = tk.StringVar( master )
		motherName.set("None")
		fatherName = tk.StringVar( master )
		fatherName.set("None")
		
		def showName(*args):
			print "variable changed to "+str(self.listboxList[0].get())
			motherName.set(self.dragonData.IDmap[int(str(self.listboxList[0].get()))])
		
		def showName2(*args):
			print "variable changed to "+str(self.listboxList[1].get())
			fatherName.set(self.dragonData.IDmap[int(str(self.listboxList[1].get()))])
		
		self.listboxList[0].trace("w", showName)
		self.listboxList[1].trace("w", showName2)
		
		label = tk.Label( master, width=10, textvariable=motherName )
		label.grid( row=i-2, column=2)
		
		label = tk.Label( master, width=10, textvariable=fatherName )
		label.grid( row=i-1, column=2)
			
		
		# dragon constant identifying information
		# except names and breed can change, can't it?	Whatever.
		label = tk.Label( master, text="Name:", width=10 )
		label.grid( row=0, column=0)
		name = tk.Entry(master, width = 10)
		name.grid( row=0, column=1)
		#name.delete(0, tk.END)
		#name.insert(0, "a default value")
		self.listboxList.append(name)
		
		label = tk.Label( master, text="ID number:", width=10 )
		label.grid( row=1, column=0)
		id = tk.Entry(master, width = 10)
		id.grid( row=1, column=1)
		self.listboxList.append(id)
		
		label = tk.Label( master, text="Gender:", width=10 )
		label.grid( row=2, column=0)
		genderOption = tk.StringVar( master )
		genderOption.set("Female")
		genderMenu = tk.OptionMenu( master, genderOption, 
			"Female","Male" ) # can add a command to the menu
		genderMenu.grid( row=2, column=1)
		self.listboxList.append(genderOption)
		
		label = tk.Label( master, text="Breed:", width=10 )
		label.grid( row=3, column=0)
		breedOption = tk.StringVar( master )
		breedOption.set("Fae")
		breedMenu = tk.OptionMenu( master, breedOption, 
			"Fae","Guardian","Mirror","Pearlcatcher","Ridgeback","Tundra","Spiral","Imperial","Snapper","Wildclaw","Nocturne","Coatl","Skydancer" ) # can add a command to the menu
		breedMenu.grid( row=3, column=1)
		self.listboxList.append(breedOption)
		
		sep = tk.Frame( master, height=2, width = 300, bd=1, relief=tk.SUNKEN )
		sep.grid(row=4,columnspan=3)	
		
		sep = tk.Frame( master, height=2, width = 300, bd=1, relief=tk.SUNKEN )
		sep.grid(row=i,columnspan=3)
		i+=1
		
		# make primary, secondary, and tertiary sections for colors and genes.
		titleList = ["Primary:","Secondary:","Tertiary:"]
		geneListList = [["Basic","Iridescent","Tiger","Clown","Speckle","Ripple","Bar","Crystal"],
						["Basic","Shimmer","Stripes","Eye Spots","Freckle","Seraph","Current","Daub","Facet"],
						["Basic","Circuit","Gembond","Underbelly","Crackle","Smoke","Spines","Okapi"]]
		
		for title in titleList:
			label = tk.Label( master, text=title, width=10 )
			label.grid( row=i, column=0)
			colorOption = tk.StringVar( master )
			colorOption.set("Maize")
			colorMenu = tk.OptionMenu( master, colorOption, 
				"Maize","White","Ice","Platinum","Silver","Gray","Charcoal","Coal","Black","Obsidian","Midnight","Shadow","Mulberry","Thistle","Lavender","Purple","Violet","Royal","Storm","Navy","Blue","Splash","Sky","Stonewash","Steel","Denim","Azure","Caribbean","Teal","Aqua","Seafoam","Jade","Emerald","Jungle","Forest","Swamp","Avocado","Green","Leaf","Spring","Goldenrod","Lemon","Banana","Ivory","Gold","Sunshine","Orange","Fire","Tangerine","Sand","Beige","Stone","Slate","Soil","Brown","Chocolate","Rust","Tomato","Crimson","Blood","Maroon","Red","Carmine","Coral","Magenta","Pink","Rose" ) # can add a command to the menu
			colorMenu.grid( row=i, column=1)
			self.listboxList.append(colorOption)
			
			geneOption = tk.StringVar( master )
			geneOption.set("Basic")
			geneMenu = apply(tk.OptionMenu, (master, geneOption) + tuple(geneListList[i%3-2]))
			geneMenu.grid( row=i, column=2)
			self.listboxList.append(geneOption)
			i+=1
		
		sep = tk.Frame( master, height=2, width = 300, bd=1, relief=tk.SUNKEN)
		sep.grid(row=i,columnspan=3)
		i+=1
		
		sep = tk.Frame( master, height=200, width = 300, bd=1, relief=tk.SUNKEN )
		sep.grid(row=i,columnspan=3)
		i+=1
		
		self.text = tk.Text(sep, height=10, width =40,wrap=tk.WORD,takefocus=True,relief = tk.SUNKEN)
		self.text.grid(row=i, column=0, columnspan=3)
		
		# set an initial selection in order to prevent someone from crashing the program by hitting OK without selecting anything
		#self.listboxList[0].select_set(0)
		#self.listboxList[1].select_set(1)
		
		
	# send the results to a place where they can be retrieved.
	def apply(self):
		for box in self.listboxList:
			self.result.append(box.get())
		self.result.append(str(self.text.get("0.0",tk.END)))
		#print self.result
		#print self.result[0].gen
		#print self.text.get("0.0",tk.END)
		


# The dialog box that allows users to add a new dragon
#i'll finish it off later when I have proper references
class EditDragonDialog(Dialog):
	def __init__(self, parent, dragonData, curDrag, title = "Dragon Adder 9000"):
		self.dragonData=dragonData
		self.curDrag = curDrag
		self.listboxList = []
		self.result = []
		Dialog.__init__(self, parent, title)
		
	# we need a different then default bottonbox because the silly OK event binding was causing havoc on the enter key in the notes section 
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
		
		# dragon constant identifying information
		# except names and breed can change, can't it?	Whatever.
		label = tk.Label( master, text="Name:", width=10 )
		label.grid( row=0, column=0)
		name = tk.Entry(master, width = 10)
		name.insert(0, self.curDrag.name)
		name.grid( row=0, column=1)
		self.listboxList.append(name)
		
		label = tk.Label( master, text="ID number:", width=10 )
		label.grid( row=1, column=0)
		label = tk.Label( master, text=self.curDrag.id, width=10 )
		label.grid( row=1, column=1)
		
		label = tk.Label( master, text="Gender:", width=10 )
		label.grid( row=2, column=0)
		if self.curDrag.gender:
			gender = "Female"
		else:
			gender = "Male"
		label = tk.Label( master, text=gender, width=10 )
		label.grid( row=2, column=1)
		
		label = tk.Label( master, text="Breed:", width=10 )
		label.grid( row=3, column=0)
		breedOption = tk.StringVar( master )
		breedOption.set(self.curDrag.species)
		breedMenu = tk.OptionMenu( master, breedOption, 
			"Fae","Guardian","Mirror","Pearlcatcher","Ridgeback","Tundra","Spiral","Imperial","Snapper","Wildclaw","Nocturne","Coatl","Skydancer" ) # can add a command to the menu
		breedMenu.grid( row=3, column=1)
		self.listboxList.append(breedOption)
		
			
		i=7
		sep = tk.Frame( master, height=2, width = 300, bd=1, relief=tk.SUNKEN )
		sep.grid(row=i,columnspan=3)
		i+=1
		
		# make primary, secondary, and tertiary sections for colors and genes.
		titleList = ["Primary:","Secondary:","Tertiary:"]
		geneListList = [["Basic","Iridescent","Tiger","Clown","Speckle","Ripple","Bar","Crystal"],
						["Basic","Shimmer","Stripes","Eye Spots","Freckle","Seraph","Current","Daub","Facet"],
						["Basic","Circuit","Gembond","Underbelly","Crackle","Smoke","Spines","Okapi"]]
		
		for title in titleList:
			label = tk.Label( master, text=title, width=10 )
			label.grid( row=i, column=0)
			colorOption = tk.StringVar( master )
			colorOption.set(self.curDrag.colors[i%3-2])
			colorMenu = tk.OptionMenu( master, colorOption, 
				"Maize","White","Ice","Platinum","Silver","Gray","Charcoal","Coal","Black","Obsidian","Midnight","Shadow","Mulberry","Thistle","Lavender","Purple","Violet","Royal","Storm","Navy","Blue","Splash","Sky","Stonewash","Steel","Denim","Azure","Caribbean","Teal","Aqua","Seafoam","Jade","Emerald","Jungle","Forest","Swamp","Avocado","Green","Leaf","Spring","Goldenrod","Lemon","Banana","Ivory","Gold","Sunshine","Orange","Fire","Tangerine","Sand","Beige","Stone","Slate","Soil","Brown","Chocolate","Rust","Tomato","Crimson","Blood","Maroon","Red","Carmine","Coral","Magenta","Pink","Rose" ) # can add a command to the menu
			colorMenu.grid( row=i, column=1)
			self.listboxList.append(colorOption)
			
			geneOption = tk.StringVar( master )
			geneOption.set(self.curDrag.genes[i%3-2])
			geneMenu = apply(tk.OptionMenu, (master, geneOption) + tuple(geneListList[i%3-2]))
			geneMenu.grid( row=i, column=2)
			self.listboxList.append(geneOption)
			i+=1
		
		sep = tk.Frame( master, height=2, width = 300, bd=1, relief=tk.SUNKEN)
		sep.grid(row=i,columnspan=3)
		i+=1
		
		sep = tk.Frame( master, height=200, width = 300, bd=1, relief=tk.SUNKEN )
		sep.grid(row=i,columnspan=3)
		i+=1
		
		self.text = tk.Text(sep, height=10, width =40,wrap=tk.WORD,takefocus=True,relief = tk.SUNKEN)
		self.text.grid(row=i, column=0, columnspan=3)
		self.text.insert(tk.END,self.curDrag.notes)
		
		# set an initial selection in order to prevent someone from crashing the program by hitting OK without selecting anything
		#self.listboxList[0].select_set(0)
		#self.listboxList[1].select_set(1)
		
		
	# send the results to a place where they can be retrieved.
	def apply(self):
		for box in self.listboxList:
			self.result.append(box.get())
		self.result.append(str(self.text.get("0.0",tk.END)))
		#print self.result
		#print self.result[0].gen
		#print self.text.get("0.0",tk.END)		
		
		
class ExaultDragonDialog(Dialog):
	def __init__(self, parent, curDrag, title = "Dragon Exaulter 9000"):
		self.curDrag = curDrag
		self.result = False
		Dialog.__init__(self, parent, title)
		
	# we need a different then default bottonbox because the silly OK event binding was causing havoc on the enter key in the notes section 
	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = tk.Frame(self)

		w = tk.Button(box, text="OK", width=10, command=self.ok)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()
	
	# builds what the dialog box looks like.
	def body(self, master):
		
		# dragon constant identifying information
		# except names and breed can change, can't it?	Whatever.
		
		warning = "Exalting " +self.curDrag.name+" to the service of the\nDatamuncher will remove them from your lair\nforever. They will leave behind no riches\nwhatsoever.  This action is irreversible.\n\nDo you wish to continue?"
		label = tk.Label( master, text=warning )
		label.grid( row=0, column=0)
		
		
		
	# send the results to a place where they can be retrieved.
	def apply(self):
		self.result = True
		
		
		
		
