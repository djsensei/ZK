README!

"Someone's in the Kitchen With Zombies!" is a cooperative card game created by
Dan Morris (daniel.e.morris@gmail.com) in 2013. This codebase seeks to replicate 
the game virtually, primarily for playtesting but also potentially for adaptation 
to a playable online version. 

========== Rules + Gameplay ==========
Between 2 and 6 players can play, and all players work together as a team. The
players work at a bakery, and use the ingredients in their hands to bake cakes
which can stave off waves of zombies. Each player holds their own hand of
ingredient cards, but once a cake is baked it is shared with the whole team. The
team also has some number of 'employees', which are non-player character cards that 
offer special abilities (and can be fed to a zombie in a pinch). 

There are 3 'days' of play, and if the team can survive all 3 they win. 
Each 'day' is broken down into a number of 'rounds', in which each player gets one
'turn'. The first round(s) of each day are the 'morning', in which no zombies come.
The players may use these rounds to stock up on ingredients and cakes. After the
morning, a certain number of rounds are played in which a zombie arrives at the
beginning of the round. The players must work together to ensure that each zombie
can be 'satisfied' with an appropriate cake or cakes. If a zombie cannot be satisfied
with available cakes, then an employee must be sacrificed. If all employees have been
sacrificed and a zombie cannot be satisfied, then the team itself is eaten and the
game is over. 

Each player gets one turn per round, and has a variety of options at his or her disposal.
1) Draw more ingredients into his hand
2) Bake one of the cakes on the 'menu'
3) Deliver some of his ingredients to a teammate
4) Swap out some of the cakes on the menu for new ones
========== /Rules + Gameplay ==========

========== Files ==========
ZKClasses.py
	The meat and potatoes. Contains the essential Player and Game classes, as well
	as all game functions. 
ZKCards.py
	Contains the specific details and data of every card in the game: Ingredients,
	Cakes, Zombies, and Employees. Also contains some helpful dictionaries for
	converting an ingredient number to an abbreviation (or name) or vice versa.
ZKSettings.py
	Contains adjustable game settings. To adjust game balance for testing purposes,
	alter the numbers in this file. 
ZKGame.py
	A simple script that ties it all together. Run this script to play the game!
ZKTester.py
	This script exists to test individual functions without having to play through 
	an entire game.
========== /Files ==========

========== Global Variables ==========
All global variables are imported by ZKClasses from ZKCards and ZKSettings.

Card Variables (dictionaries which contain all information about a given card):
	ingdata    = ingredients
	cakedata   = cakes
	zombiedata = zombies
	empdata    = employees
	
Card Helper Variables
	ingnamenum = converts an ingredient name to its array reference number
	ingabbvnum = converts an ingredient abbreviation " " "
	ingnumname = converts an ingredient number to its name
	ingnumabbv = converts an ingredient number to its abbreviation
	
Game Settings Variables
	morninglength    = # zombie-free rounds to start each day (array length 3)
	zombieload       = # zombie rounds per day (array length 3)
	startinghand     = # ingredient cards in hand to start game
	maxhandsizeround = maximum hand size at the end of a round
	endrounddiscard  = # cards you can keep at the end of a day
	playernames      = a silly array of player names for use in playtesting
	cardsperdraw     = # cards a player takes per ingredient draw
	discardsperdraw  = # cards a player must immediately discard after drawing
	deliverylimit    = # cards a player can deliver to another during his turn
========== /Global Variables ==========

========== Versions, Updates ==========
8/28/13 - Version 0.1
	Text input playthrough should work mostly (bugs may still arise). Employees have 
	not yet been added in, neither has dying (failing to feed a zombie will result in
	getting stuck). Text input is not especially robust, so be careful about typos!
	
9/3/13 - Version 0.2
	All code updated for Python 3.3.
	cardsperdraw is now an array to allow for differences based on number of players.
	discardsperdraw added to allow "draw 2 choose 1" options.
	Ingredient drawing all moved to the draw() function.
	All text (print() and input() statements) moved to their own functions.
	Cosmetic improvements in text functions.
	
TODO:
	Add Employees, integrate them into the game functions
	Add Death (once there is no employee to consume)
	Add logging capabilities for postgame data analysis. 
	Investigate using pygame for GUI
========== /Versions, Updates ==========