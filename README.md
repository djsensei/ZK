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
ZKEngine.py
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
ZKBot.py
	Instructs the bot to play tons of games and report the results. 
========== /Files ==========

========== Global Variables ==========
All global variables are imported by ZKEngine from ZKCards and ZKSettings.

Card Variables (dictionaries which contain all information about a given card):
	ingdata    = ingredients
	cakedata   = cakes
	zombiedata = zombies
	
Card Helper Variables
	ingnamenum  = converts an ingredient name to its array reference number
	ingabbvnum  = converts an ingredient abbreviation " " "
	ingnumname  = converts an ingredient number to its name
	ingnumabbv  = converts an ingredient number to its abbreviation
	ingabbvname = converts an ingredient abbreviation to its name
	
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
	empupcost        = dictionary of employee upgrade costs
	empnames         = array of employee names
	empdiff          = array of how many employees you get at each difficulty level
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
	
9/8/13 - Version 0.3
	Employees are now integrated!
	Ingredient-drawing bugs may appear when deck empties, but ingreshuffle()
	*should* work. 
	
9/18/13 - Version 0.4
	The autobot has been built! It plays through a game automatically, generating
	winrate data for balance testing. 
	To play a live (text input) game, run ZKGame.py.
	To run a series of bot games, use ZKBot.py.
	Game engine moved from ZKClasses to ZKEngine. Inherited classes now used to distinguish
	between bot and live games. The BotGame and LiveGame classes both inherit from the 
	standard Game class, providing the necessary prompt and display functions for it to work. 
	Game logging now enabled: results go to ZKtestlog.txt.
	ZKTestAnalysis reads from ZKtestlog and analyze results. 
	
TODO:
	Investigate using pygame for GUI
========== /Versions, Updates ==========