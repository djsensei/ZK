# - This file contains initial game settings.
# - To test game balance, tweak them!

# morninglength = number of zombie-free rounds to start each day
morninglength = [3,2,1]

# zombieload = number of zombie rounds per day
zombieload = [5,6,7]

# startinghand = number of ingredient cards in hand to start game
startinghandsize = 4

# maxhandsizeround = maximum hand size at the end of a round
maxhandsizeround = 100

# endrounddiscard = number of cards you can keep at the end of a day
endrounddiscard = 100

# playernames = an array of player names for use in playtesting
defaultplayernames = ['Crank', 'Stepho', 'Dmo', 'Ethan', 'K2', 'Erin']

# cardsperdraw = how many cards a player takes per ingredient draw
# discardsperdraw = how many of those cards a player must discard immediately
# arrays per number of players
cardsperdraw = [2,2,2,2,1,1]
discardsperdraw = [0,0,0,1,0,0]

# deliverylimit = how many cards a player can deliver to another during his turn
deliverylimit = 100

# empupcost = a dict of upgrade costs for employees [1->2, 2->3]
empupcost = {
'stocker':[5,8],
'delivery':[5,8],
'security':[5,8],
'lookout':[5,8],
'janitor':[5,8]}

# empnames = a list of employee names to choose from
empnames = ['stocker', 'delivery', 'security', 'lookout', 'janitor']

# empdiff = how many employees you get if difficulty is [easy, med, hard]
empdiff = [4,3,2]