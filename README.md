# Dragon Ancestry and Lineages (DAL9000)
This is the dragon tracking application written by Flight Rising user TheLegoLady.  
This is the Alpha version, and is by no means a finished product.  Loads of new features will be added.
All dragon species, colors, genes, and ideas © Stormlight Workshop.

Requirements:
Python 2.7  
Python 3.x might work, but is untested.
The TKinter package should come automatically with python.

How to launch application:
Using the terminal console, or whatever the command line application is for your system, set your active directory to the DAL9000 folder.  
Type the comand: python display.py
The application should now launch.  

Using the application:
To select a dragon, double click on its picture.  It will be outlined in green and its stats will show up in the side bar.  The exalt and edit buttons will also become active.
To compare potential mates, hover over another dragon.  It will be outlined in green as well.  If the dragons are compatible, the color ranges for the pair are displayed in the sidebar.  If the match is not possible, either because both dragons are the same mating type or because they have common ancestors,  the sidebar will display the appropriate error, and common ancestors will be highlighted in red.  All other ancestors will be highlighted in yellow.  De-select a dragon by double clicking somewhere without a dragon, or by selecting another dragon.  You can also move the dragons on-screen by clicking and dragging with the mouse.  

Adding dragons:
All dragon information is added manually using the "Add Dragon" button, in order to comply with the Flight Rising terms of Use.
Make sure your information is as accurate as possible when entering it, as some information cannot be changed via the "Edit" button.
In order for for the program to recognize dragons as being related, their common ancestor(s) must be present in the tree-structure.
Therefore, when designating a dragon as 'first-gen' (by not selecting any parents in the parent selection box), be sure that the dragon is not related to any other 'first-gen' dragons.
Currently, a dragon's parents must be designated by selecting their ID from a drop-down menu.  I know this is a pain, and will be fixed ASAP.  
A box at the bottom of the "Add Dragon" dialog is available for you to enter any notes you want.

Dragon images:
Currently, the application only works with .gif filetype images.
To have a dragon display its image, copy its avatar image from the Flight Rising site.  These images can be found by using Flight Rising's 'Change Avatar' feature, and saving the images (generally by right- or command-clicking on the image).
Use a free program like GIMP to convert the images to .gif.  Also, be sure to add a white background layer first for added prettiness.
Save the new image as <dragon ID>.gif where you replace <dragon ID> with the dragon's ID number.
One generic dragon image is provided for you as a substitute for any dragons you do not have gifs for, and will be used whenever the application cannot find a certain dragon's image.

I think that's it.  Happy Dragon Tracking!
