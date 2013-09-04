# - The basic classes for "Someone's in the Kitchen with Zombies"

''' 8/24/13 update: 
updated classes from old version to new cooperative version
todo: figure out employee skills - 
        list each class of skill as an individual attribute, set most to None?

'''
import random
from ZKSettings import *
from ZKCards import * 
# ingnamenum, ingabbvnum, ingnumabbv, ingnumname, ingabbvname, ingdata, cakedata, empdata, zombiedata

''' Probably obsolete, but figure out how to make employees work first
class Employee:
	def __init__(self, name, skill):
		self.name = name
		self.skill = skill # the employee's bonus skill
'''
	
class Player:
	def __init__(self, name):
		self.name = name
		self.position = None # where at the table?
		self.ingredients = [0,0,0,0,0,0,0,0,0,0] # an array of ingredients in hand
		
	def canbake(self, cake):
		for i in range(10):
			if self.ingredients[i] < cakedata[cake][2][i]:
				return False
		if cakedata[cake][2][10] > 0: # wildcard checker
			if sum(cakedata[cake][2]) > sum(self.ingredients):
				return False
		return True
		
	def ingstr(self):
		s = ""
		for i in range(10):
			for j in range(self.ingredients[i]):
				s += ingnumabbv[i] + " "
		return s
		
class Game:
	def __init__(self, id, nump):
		self.id = id
		self.nump = nump
		self.cakemenu = ['','',''] # an array of 3 face-up cake cards
		self.cakedeck = [] # a deck of cake cards, to be drawn into the menu
		self.zombiedeck = [] # a deck of zombie cards
		self.zombiedead = [] # discarded zombies
		self.ingdeck = [] # a deck of ingredients to draw from
		self.ingdiscard = [] # discarded ingredients
		self.cakediscard = [] # discarded cakes
		self.employeepile = [] # a deck of potential employees
		self.displaycase = [] # an array of baked cakes, ready to consume
		self.alive = True # if the players' brains are still intact
		self.playernames = defaultplayernames[:nump]
		random.shuffle(self.playernames)
		self.players = {} # a dict of players - 'name':Player
		j = 0
		for i in self.playernames:
			self.players[i] = Player(i)
			self.players[i].position = j
			j += 1
			
	'''
	Serious Game Functions
	'''
	def play(self):
		# create and shuffle decks
		self.formdecks()
		
		# deal starting hands
		for i in self.playernames:
			self.draw(i, 's')
				
		# deal starting cake menu
		for i in range(3):
			self.newcake(i)
		
		# three days of action!
		for i in range(3):
			self.day(i)
			
		# the endgame...
		self.endgamedisp()
			
	def day(self, n):
		if n > 0:
			self.rotateplayers()
		self.daystartdisp(n)
		
		# discard down to appropriate size hands
		for i in self.players:
			if sum(self.players[i].ingredients) > endrounddiscard:
				self.discard(self.players[i], endrounddiscard)
				
		# run through the rounds!
		r = 1
		for m in range(morninglength[n]):
			self.round(0,r,n)
			r += 1
		for z in range(zombieload[n]):
			self.round(1,r,n)
			r += 1
		
		#day cleanup stuff?
	
	def round(self, ztoggle, rnum, dnum):
		# reveal zombie (if ztoggle == 1)
		if ztoggle == 1:
			z = self.zombiedeck[0]
			self.zombiedeck = self.zombiedeck[1:]
			self.roundstartdisp(1, rnum, dnum, z)
		else:
			self.roundstartdisp(0, rnum, dnum)
		self.casedisplay()
		self.dispmenu()
		self.disphands()
		
		# take turns in order
		for i in range(self.nump):
			self.turn(self.playernames[i])
			
		# employee abilities --TODO--
		
		# feed zombie
		if ztoggle == 1:
			self.zombiefeedprompt(z)
			
	# feedzombie discards the cake(s) and the zombie and returns 1 if fed properly
	# it leaves the cake(s) and zombie and returns 0 if not fed properly
	def feedzombie(self, z, cakes):
		mmm = 0 # mmm = zombie satisfied?
		for i in range(len(cakes)):
			if cakes[i] not in cakedata:
				return 0
		if len(cakes) == 1:
			if cakes[0] == zombiedata[z][3]: # specific craving met
				mmm = 1
			elif cakedata[cakes[0]][1] >= zombiedata[z][1]: # cake is powerful enough
				mmm = 1
			elif zombiedata[z][4] in self.cakeingfull(cakes[0]): # ingredient craving met
				mmm = 1
			else: 
				mmm = 0
		else:
			power = 0
			for c in range(len(cakes)):
				power += cakedata[cakes[c]][1]
			if power >= zombiedata[z][1]:
				mmm = 1
			else: 
				mmm = 0
				
		if mmm == 1:
			self.zombiedead.append(z)
			for c in range(len(cakes)):
				self.cakediscard.append(cakes[c])
				self.displaycase.remove(cakes[c])
			return 1
		else:
			return 0
	
	def turn(self, pname):
		self.actionprompt(pname)
		
	'''
	Player Turn/Decision Functions 
	'''
	def draw(self, pname, type):
		# causes player to draw ingredients
		# type: 's' - game start, 'p' - player decision, 'e' - employee ability
		if type == 's':
			for i in range(startinghandsize):
				self.players[pname].ingredients[ingnamenum[self.ingdeck[i]]] += 1
			self.ingdeck = self.ingdeck[startinghandsize:]
		elif type == 'p':
			if len(self.ingdeck) < cardsperdraw[self.nump-1]:
				self.ingreshuffle()
			newings = self.ingdeck[:cardsperdraw[self.nump-1]]
			self.ingdeck = self.ingdeck[cardsperdraw[self.nump-1]:]
			if discardsperdraw[self.nump-1] > 0:
				newings, discs = self.discardprompt(pname, newings, discardsperdraw[self.nump-1])
				for d in range(len(discs)):
					self.ingdiscard.append(discs[d])
			for j in range(len(newings)):
				self.players[pname].ingredients[ingnamenum[newings[j]]] += 1
		elif type == 'e':
			# TODO - employee stuff!
			print('bonerjam')
	
	def bakecake(self, pname, cname):
		# returns 1 if the cake is baked, and 0 if the cake cannot be baked
		if self.players[pname].canbake(cname) == True:
			if cname in self.cakemenu:
				# spend ingredients
				for i in range(10):
					self.players[pname].ingredients[i] -= cakedata[cname][2][i]
				
				# wildcards?
				w = cakedata[cname][2][10]
				if w > 0:
					self.wildcardprompt(pname, cname, w)
							
				# place cake in case
				self.displaycase.append(cname)
				
				# replace cake in menu
				if self.cakemenu[0] == cname:
					self.newcake(0)
				elif self.cakemenu[1] == cname:
					self.newcake(1)
				else:
					self.newcake(2)
				return 1
			else:
				return 0
		else:
			return 0
			
	def swapmenu(self):
		# returns 1 after a swap, and 0 if no swap took place
		self.dispmenu()
		s = self.swapprompt()
		for i in range(len(s)):
			if s[i] not in ' 123':
				return 0
		s = s.split()
		for i in range(len(s)):
			s[i] = int(s[i])
			self.cakediscard.append(self.cakemenu[s[i]-1])
			self.newcake(s[i]-1)
		return 1
		
	def deliver(self, pname):
		# returns 1 after a successful delivery, and 0 if the player doesn't deliver anything
		recip, pay = self.deliveryprompt(pname)
		for i in pay:
			# send to recip's hand
			self.players[recip].ingredients[ingabbvnum[i]] += 1
			# remove from sender's hand
			self.players[pname].ingredients[ingabbvnum[i]] -= 1
		if len(pay) == 0:
			return 0
		return 1
		
	def discard(self, pname, handsize):
		while sum(self.players[pname].ingredients) > handsize:
			print(self.players[pname].name + ", you need to discard down to " + str(handsize) + " ingredients.")
			print("Your current hand: " + self.players[pname].ingstr())
			r = input("Enter your discards, separated by a space: ")
			disc = r.split()
			for i in range(len(disc)):
				disc[i] = ingabbnum[disc[i]]
			for i in range(len(disc)):
				self.players[pname].ingredients[disc[i]] -= 1
		print("Thank you for your cooperation.")
		
	'''
	Minor Game Functions
	'''
	def rotateplayers(self):
		# rotates players clockwise one, for the beginning of a day
		x = self.playernames[0]
		for i in range(self.nump-1):
			self.playernames[i] = self.playernames[i+1]
		self.playernames[self.nump-1] = x
		
	def formdecks(self):
		# uses data from ZKCards: ingdata, cakedata, empdata, zombiedata
		# each contains the relevant information about each card in a dict of tuples
		for i in ingdata:
			for f in range(ingdata[i][2]):
				self.ingdeck.append(i)
				self.ingdeck.append(i)
				self.ingdeck.append(i)
		random.shuffle(self.ingdeck)
		for c in cakedata:
			for f in range(cakedata[c][3]):
				self.cakedeck.append(c)
		random.shuffle(self.cakedeck)
		for z in zombiedata:
			self.zombiedeck.append(z)
		random.shuffle(self.zombiedeck)
		#for e in empdata:
		#	self.employeepile.append(e)
		#random.shuffle(self.employeepile)
			
	def ingreshuffle(self):
		# shuffles discarded ingredients back into the ingredient draw deck
		random.shuffle(self.ingdiscard)
		self.ingdeck += self.ingdiscard
		self.ingdiscard = []
		
	def cakereshuffle(self):
		# shuffles discarded cakes back into the cake draw deck
		random.shuffle(self.cakediscard)
		self.cakedeck += self.cakediscard
		self.cakediscard = []
	
	def newcake(self, n):
		# draws a new cake into slot n of the cake menu
		self.cakemenu[n] = self.cakedeck[0]
		self.cakedeck = self.cakedeck[1:]
		if len(self.cakedeck) == 0:
			self.cakereshuffle()
			
	'''
	Prompt Functions
	(Currently, all input() statements should live here.)
	'''
	def discardprompt(self, pname, ings, ndisc):
		# returns an array of kept ingredients and an array of discarded ingredients
		# ings = an array of ingredients to discard from
		# ndisc = how many must be discarded
		n = len(ings)
		nkeep = n - ndisc
		k = []
		while len(k) != nkeep:
			print("Of the following %s ingredients, you may keep %s." % (n, nkeep))
			print(self.ingname2str(ings))
			k = input("Enter the ones you want to keep: ").split()
		for i in range(len(k)):
			k[i] = ingabbvname[k[i]]
			ings.remove(k[i])
		return k, ings
	
	def actionprompt(self, pname):
		print("%s, it is your turn!" % pname)
		print("Your ingredients: " + self.players[pname].ingstr())
		print('Enter "draw" to draw ingredients.')
		if sum(self.players[pname].ingredients) > 0:
			print('Enter "del" to deliver ingredients to a teammate.')
		print('Enter "swap" to swap out cakes on the menu.')
		for i in range(3):
			if self.players[pname].canbake(self.cakemenu[i]):
				print('Enter "bake %s" to bake %s.' % (self.cakemenu[i], cakedata[self.cakemenu[i]][0]))
		good = 0
		while good == 0:
			action = input("What'll it be, chef? ")
			if action[:2] == "dr":
				self.draw(pname, 'p')
				good = 1
			elif action == "del":
				good = self.deliver(pname)
			elif action[0] == "s":
				good = self.swapmenu()
			elif action[0] == "b":
				good = self.bakecake(pname,action[5:])
			else: 
				good = 0
		print('')
	
	def deliveryprompt(self, pname):
		print("Your ingredients: " + self.players[pname].ingstr())
		print("Your friends' ingredients: ")
		for i in range(self.nump):
			if pname != self.playernames[i]:
				print("%s: " % self.playernames[i] + self.players[self.playernames[i]].ingstr())
		recip = 'BOOURNSXXXSHABLAOW'
		while recip not in self.playernames:
			recip = input("Who would you like to deliver to? ")
		pay = ['']*(deliverylimit+1)
		while len(pay) > deliverylimit:
			pay = input("Which ingredients would you like to deliver to %s? " % recip).split()
		return recip, pay
		
	def swapprompt(self):
		s = input("Enter the number(s) of the cakes to swap out: ")
		return s
		
		
	def wildcardprompt(self, pname, c, w):
		k = 0
		while k == 0:
			print("This cake has %s wildcards in the cost!" % w)
			print("Your remaining ingredients: " + self.players[pname].ingstr())
			burn = input("Which %s will you use? " % w).split()
			if len(burn) == w:
				for i in range(w):
					self.players[pname].ingredients[ingabbvnum[burn[i]]] -= 1
				k = 1

		
	def zombiefeedprompt(self, z):
		print("Time to feed the Zombie!")
		if zombiedata[z][3] != None: 
			print("Reminder: Hunger %s, Craving %s" % (zombiedata[z][1], zombiedata[z][3]))
		elif zombiedata[z][4] != None:
			print("Reminder: Hunger %s, Craving %s" % (zombiedata[z][1], zombiedata[z][4]))
		else: 
			print("Reminder: Hunger %s" % zombiedata[z][1])
		print("Your available cakes are as follows: (power) (ingredients)")
		for c in self.displaycase:
			print(cakedata[c][0], "("+str(cakedata[c][1])+")", "("+self.cakeingabbv(c)+")")
		fed = 2
		while fed != 1:
			if fed == 0:
				print("That isn't enough!")
			print("Enter the cake(s) to feed the zombie, or enter 'brains'")
			feed = input("to serve one of your employees instead: ")
			if feed == "brains":
				self.brainfeed()
				fed = 1
			else:
				fed = self.feedzombie(z, feed.split())
		print("Your guest left quite satisfied!")
	'''
	Simple Display Functions
	(Currently, all print() statements without input() should live here.)
	'''
	
	def ingname2str(self, ings):
		# converts an array of ingredient names into a string of abbreviations
		s = ""
		for i in range(len(ings)):
			s += ingdata[ings[i]][1]+ " "
		return s
		
	def cakeingfull(self, c):
		# displays the ingredients of cake c in simple form (lower case, one word)
		cakestr = ''
		for i in range(10):
			if cakedata[c][2][i] > 0:
				cakestr += ingnumname[i]
		return cakestr
		
	def cakeingabbv(self, c):
		# displays the ingredients of cake c in abbreviated form (C, B, Ca, etc.)
		cstr = ''
		for i in range(11):
			for j in range(cakedata[c][2][i]):
				cstr += ingnumabbv[i] + ' '
		return cstr
		
	def dispmenu(self):
		print("Here is the current cake menu: (cost) (power)")
		for i in range(3):
			print(str(i+1) + ": " + cakedata[self.cakemenu[i]][0] + " - ( " + self.cakeingabbv(self.cakemenu[i]) + ") (" + str(cakedata[self.cakemenu[i]][1]) + ")")
		print('')
			
	def disphands(self):
		print("Here are the current player hands:")
		for i in self.playernames:
			print( i + ": " + self.players[i].ingstr())
		print('')
		
	def casedisplay(self):
		if len(self.displaycase) == 0:
			print("Your display case is empty! You had better bake something...")
			return
		print("Here are the cakes fresh and ready in your display case:")
		for i in self.displaycase:
			print("%s - %s" % (cakedata[i][0], cakedata[i][1]))
		print("")
		
	def daystartdisp(self, n):
		print("---- Day %s ----" % (n+1))
		print("It's a new day! Not a Zombie in sight...")
		print("Let's bake some cakes!")
		print('')
		
	def roundstartdisp(self, ztoggle, r, d, zname = None):
		print("--- Day %s, Round %s ---" % (d+1, r))
		if ztoggle == 1:
			print("%s is at your door with a hunger level of %s!" % (zombiedata[zname][0], zombiedata[zname][1]))
			if zombiedata[zname][2] == 'They':
				if zombiedata[zname][3] != None:
					print("%s have a craving for %s." % (zombiedata[zname][2], cakedata[zombiedata[zname][3]][0]))
				elif zombiedata[zname][4] != None:
					print("%s have a craving for any cake with %s." % (zombiedata[zname][2], ingdata[zombiedata[zname][4]][0]))
			else:
				if zombiedata[zname][3] != None:
					print("%s has a craving for %s." % (zombiedata[zname][2], cakedata[zombiedata[zname][3]][0]))
				elif zombiedata[zname][4] != None:
					print("%s has a craving for any cake with %s." % (zombiedata[zname][2], ingdata[zombiedata[zname][4]][0]))
			print('')
		else: 
			print("Ah, the calm morning. Perfect for baking peacefully!")
			print('')
	
	def endgamedisp(self):
		if self.alive == True:
			print("You survived! Hooray!")
			print("Thanks for playing :)")
		else:
			print("Oh, I'm afraid you didn't survive...")
			print("Well, at least you made a good snack for a hungry zombie.")
	