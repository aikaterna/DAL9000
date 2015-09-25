# Dragon Ansestry and Linages (DAL9000)
This is the as yet unamed dragon tracking application of Flight Rising user TheLegoLady.  
This is the Alpha version, and is by no means a finished product.  Loads of new features will be added.
All dragon species, colors, genes, and ideas © Stormlight Workshop.

Requirements:
Python 2.7  
Python 3.x might work, but is untested.
The TKinter package should come automatically with python.

How to launch application:
using the terminal console, or whatever the command line application is for your system, set your active directory to the Dragon Tracker folder.  
Type the comand: python display.py
The application should now launch.  

Using the application:
To select a dragon, double click on it.  It will be boxed green and stats will show up in the side bar.  The exalt and edit buttons will become active.
To compare potental mates, hover over another dragon.  It will be outlined in greed as well.  If the match is compatable, the various color outcomes are displayed in the sidebar.  If the match is not possible, either both dragons are the same sex, or there have common ansestors.  The sidebar will display the appropriate error, and common ansestors will be highlighted red.  All other ansestors will be yellow.  

Adding dragons:
All dragon information is added manually using the add dragon button.  This is in line with the Flight Rising terms of Use.
Make sure information is as accurate as possible when entering it, some information cannot be changed via the edit button.
In order for for the program to recognize dragons as being related, their common ansestor must be present in the tree-structure.
Therefor, when selecting a dragon to be 'first-gen' (not selecting any parents in the parent selection box), be sure that the dragon is not related to any other 'first-gen' dragons.
Currently, parents must be selected by selecting their ID from a drop-down menue.  I know this is a pain, and will be fixed ASAP.  
A box at the bottom of the add dragon dialog is available for you to put any notes you want.

Dragon images:
Currently, the application only works with .gif filetype images.
To have a dragon display it's image, grab it's avatar image.  These images can be found by using Flight Rising's 'change Avatar' feature, and saving the images.
Use a free program like GIMP to convert the images to .gif.  Also, be sure to add a white background layer first for added prettyness.
Save the new image as <dragon ID>.gif where you replace <dragon ID> with the dragon's ID number.
One dragon image is provided for you as a substitute for any dragon images you do not have gifs of, and will be used whenever the application cannot find a certain dragon's image.
It can be found at https://cloud.githubusercontent.com/assets/8117715/10091551/e1a0f466-630a-11e5-8276-297444b964c6.gif
Save it in the Dragon Tracker folder as MissingNo.gif

I think that's it.  Happy Dragon Tracking!
