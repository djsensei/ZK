# - The basic classes and functions for "Someone's in the Kitchen with Zombies"

import random
from ZKSettings import *
from ZKCards import * 

class Employee:
	def __init__(self, name):
		self.name = name
		self.tier = 1
		
	def upgrade(self, cakes):
		# returns None if failed, an array of cake(s) to spend if successful.
		if self.tier == 3:
			return None
		price = empupcost[self.name][self.tier-1]
		power = 0
		for i in range(len(cakes)):
			power += cakedata[cakes[i]][1]
		if power < price:
			return None
		spend = self.upgradeprompt(price, cakes)
		self.tier += 1
		return spend
		
	def upgradeprompt(self, price, cakes):
		# returns an array of cake(s) to spend
		print("You must spend %s to upgrade your %s." % (price, self.name))
		print("Here are your available cakes:")
		for i in range(len(cakes)):
			print(cakes[i] + ' (' + str(cakedata[cakes[i]][1]) + ')')
		spend = input("Enter the cake(s) to feed him: ").split()
		sum = 0
		for j in range(len(spend)):
			sum += cakedata[spend[j]][1]
		if sum < price:
			spend = self.upgradeprompt(price, cakes)
		return spend
	
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
	def __init__(self, id, nump, diff):
		self.id = id
		self.nump = nump
		self.diff = diff # 1, 2, or 3 for easy, medium, hard
		self.cakemenu = ['','',''] # an array of 3 face-up cake cards
		self.cakedeck = [] # a deck of cake cards, to be drawn into the menu
		self.zombiedeck = [] # a deck of zombie cards
		self.zombiedead = [] # discarded zombies (unused at the moment)
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
		self.employees = {} # a dict of Employee objects
		self.actionplan = [] # an array used in the autobot for player turns
		
		# create and shuffle decks
		self.formdecks()
		
		# deal starting hands and employees
		for i in self.playernames:
			self.draw(i, 's')
		self.hireemployees()
		
		# deal starting cake menu
		for i in range(3):
			self.newcake(i)
		
	'''
	Serious Game Functions
	'''
	def play(self):
		# three days of action!
		for i in range(3):
			self.day(i)
			
		# the endgame...
		self.endgamedisp()
		
	def gameover(self):
		# you lose!
		print("dang, that's it.")
			
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
		
		# upgrade employees
		if n < 2:
			if self.employees:
				self.empupgradeprompt()
		
	
	def round(self, ztoggle, rnum, dnum):
		# reveal zombie (if ztoggle == 1)
		z = None
		if ztoggle == 1:
			z = self.zombiedeck[0]
			self.zombiedeck = self.zombiedeck[1:]
			self.roundstartdisp(1, rnum, dnum, z)
		else:
			self.roundstartdisp(0, rnum, dnum)
			
		# check for early employee abilities
		self.earlyempcheck()
		
		# display everything relevant
		self.dispemps()
		self.casedisplay()
		self.dispmenu()
		self.disphands()
		
		# take turns in order
		for i in range(self.nump):
			self.turn(self.playernames[i])
			
		# employee abilities
		z = self.empcheck(z)
		
		# feed zombie
		if z:
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
			elif zombiedata[z][4]: # ingredient craving exists
				if cakedata[cakes[0]][2][ingnamenum[zombiedata[z][4]]] > 0:
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
			if len(self.ingdeck) < 1:
				self.ingreshuffle()
			self.players[pname].ingredients[ingnamenum[self.ingdeck[0]]] += 1
			self.ingdeck = self.ingdeck[1:]
	
	def bakecake(self, pname, cname):
		# returns 1 if the cake is baked, and 0 if the cake cannot be baked
		if self.players[pname].canbake(cname) == True:
			if cname in self.cakemenu:
				# spend ingredients
				for i in range(10):
					self.players[pname].ingredients[i] -= cakedata[cname][2][i]
					for j in range(cakedata[cname][2][i]):
						self.ingdiscard.append(ingnumname[i])
				# wildcards?
				w = cakedata[cname][2][10]
				if w > 0:
					self.wildcardprompt(pname, w)
							
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
		if len(pay) == 0:
			return 0
		for i in pay:
			# send to recip's hand
			self.players[recip].ingredients[ingabbvnum[i]] += 1
			# remove from sender's hand
			self.players[pname].ingredients[ingabbvnum[i]] -= 1
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
	
	def hireemployees(self):
		random.shuffle(empnames)
		for i in range(empdiff[self.diff - 1]):
			self.employees[empnames[i]] = Employee(empnames[i])
			
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
			
	def earlyempcheck(self):
		# checks employee abilities for beginning of round
		# right now, it's just 'lookout'
		if 'lookout' in self.employees:
			self.emplookout(self.employees['lookout'].tier)
	
	def empcheck(self, z = None):
		# checks on/activates employee abilities at the end of a round
		# returns the present zombie or None if there is no zombie
		if len(self.employees) == 0:
			return z
		
		if 'delivery' in self.employees:
			self.empdeliverprompt()
		
		if 'stocker' in self.employees:
			self.empstockupprompt()
		
		if 'security' in self.employees:
			if z:
				if zombiedata[z][1] - self.employees['security'].tier < 3:
					# assumes that max bounce level = tier + 2
					self.zombiebouncedisp()
					z = None
			
		if 'janitor' in self.employees:
			self.empjanitorprompt()
			
		return z
		
	def casesort(self):
		# sorts the display case, weakest cakes to strongest
		# create tuples of display cakes and their power
		cakepowers = []
		for i in range(len(self.displaycase)):
			cakepowers.append((self.displaycase[i], cakedata[self.displaycase[i]][1]))
		# sort by power
		sorted(cakepowers, key = lambda cakepowers: cakepowers[1])
		# recreate case by name
		self.displaycase = []
		for i in range(len(cakepowers)):
			self.displaycase.append(cakepowers[i][0])
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
		
		
	def wildcardprompt(self, pname, w):
		k = 0
		while k == 0:
			print("This cake has %s wildcards in the cost!" % w)
			print("Your remaining ingredients: " + self.players[pname].ingstr())
			burn = input("Which %s will you use? " % w).split()
			if len(burn) == w:
				for i in range(w):
					self.players[pname].ingredients[ingabbvnum[burn[i]]] -= 1
					self.ingdiscard.append(ingabbvname[burn[i]])
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
				self.brainfeedprompt()
				fed = 1
			else:
				fed = self.feedzombie(z, feed.split())
		print("Your guest left quite satisfied!")
	
	def brainfeedprompt(self):
		# when cake is not enough... feed an employee or it's game over!
		if self.employees:
			for i in self.employees:
				print("To sacrifice your %s, enter '%s'." % (i,i))
			sac = 'nope'
			while sac not in self.employees:
				sac = input("Choose your fate: ")
			del self.employees[sac]
		else: 
			self.alive = False
			self.gameover()
		
	def empupgradeprompt(self):
		for e in self.employees:
			if self.employees[e].tier < 3:
				print("Do you want to upgrade your tier-%s %s?" % (self.employees[e].tier, e))
				yn = input("It will cost you %s. y/n? " % empupcost[e][self.employees[e].tier-1])
				if yn == "y":
					spend = self.employees[e].upgrade(self.displaycase)
					if spend == None:
						print("%s upgrade failed." % e)
					else:
						for i in range(len(spend)):
							self.displaycase.remove(spend[i])
							self.cakediscard.append(spend[i])
							
	def empdeliverprompt(self):
		# handles employee deliveries
		self.disphands()
		t = self.employees['delivery'].tier
		if t == 1:
			print("Your delivery crew offers you one free 1-card delivery.")
			d = input("Enter the delivering player's name or 'no' if you don't want it: ").split()
		elif t == 2:
			print("Your delivery crew offers you two free 1-card deliveries.")
			d = input("Enter the delivering players name(s) or 'no' if you don't want them: ").split()
		else:
			print("Your delivery crew offers each player one free 1-card delivery.")
			d = input("Enter the name of each player who wants to deliver a card: ").split()
		if d[0] != 'no':
			for j in range(len(d)):
				recip = 'BOOURNSXXXSHABLAOW'
				while recip not in self.playernames:
					recip = input("Who would you like to deliver to, %s? " % d[j])
				i = input("Which ingredient would you like to deliver to %s? " % recip)
				# send to recip's hand
				self.players[recip].ingredients[ingabbvnum[i]] += 1
				# remove from sender's hand
				self.players[d[j]].ingredients[ingabbvnum[i]] -= 1
	
	def empjanitorprompt(self):
		n = self.employees['janitor'].tier - 1
		if n > 0:
			if len(self.ingdiscard) > 0:
				print("One player may search the discards for %s ingredients" % n)
				self.disphands()
				who = 'jabroniXXXalert'
				while who not in self.playernames:
					who = input("Who will scavenge? ")
				for i in range(n):
					sel = ''
					while sel not in self.ingdiscard:
						sel = input("Which ingredient would you like? ")
						if sel in self.ingdiscard:
							self.players[who].ingredients[ingnamenum[sel]] += 1
							self.ingdiscard.remove(sel)
						else:
							print("%s is not available." % sel)
							
	def empstockupprompt(self):
		t = self.employees['stocker'].tier
		if t < 3:
			# 1 player, tier cards
			print("One player may draw %s ingredients from the stocker" % t)
			who = "blasfasdfadfasdds"
			while who not in self.playernames:
				who = input("Who gets to draw? ")
			for i in range(t):
				self.draw(who, 'e')
		else:
			# all players, 1 card
			for i in range(self.nump):
				self.draw(self.playernames[i],'e')
			print("The stocker provided every player with an extra ingredient!")
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
		
	def dispemps(self):
		print("Here are the current employees:")
		for i in self.employees:
			print("%s, tier %s" % (i, self.employees[i].tier))
		print("")
		
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
			
	def emplookout(self, tier):
		# displays upcoming zombies
		for i in range(tier):
			if zombiedata[self.zombiedeck[i]][3] != None:
				print("Next Zombie approaching: %s. Hunger %s. Craving %s." % (zombiedata[self.zombiedeck[i]][0], zombiedata[self.zombiedeck[i]][1], cakedata[zombiedata[self.zombiedeck[i]][3]][0]))
			elif zombiedata[self.zombiedeck[i]][4] != None:
				print("Next Zombie approaching: %s. Hunger %s. Craving a cake with %s." % (zombiedata[self.zombiedeck[i]][0], zombiedata[self.zombiedeck[i]][1], zombiedata[self.zombiedeck[i]][4]))
			else:
				print("Next Zombie approaching: %s. Hunger %s." % (zombiedata[self.zombiedeck[i]][0], zombiedata[self.zombiedeck[i]][1]))
	
	def zombiebouncedisp(self):
		# displays when your security employee bounces a zombie
		print("Your security guard bounced that punk-ass zombie!")
	
	def endgamedisp(self):
		if self.alive == True:
			print("You survived! Hooray!")
			print("Thanks for playing :)")
		else:
			print("Oh, I'm afraid you didn't survive...")
			print("Well, at least you made a good snack for a hungry zombie.")
	