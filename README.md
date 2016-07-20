# Tec360ZoneStyleChange
A very simple Python script that allows for super quick design of functions to change Tecplot zone styles based on zone name. You could just as easily be changed to do it based on some others own property other than its name.

Not a lot of explanation here. See the Tecplot reference manual for help on scripting, and look in the documentation folder in the main Tecplot installation directory for the index.html file which contains a complete function reference. Everything's fairly straightforward.

Remember when you go to use these, that you first have to add  the directory in which you have the script saved to the Python search path and Tecplot, then you can browse for, open, and load the script and run its functions in Tecplot. Also remember that each function that you want to be visible in Tecplot needs to start with TP_.