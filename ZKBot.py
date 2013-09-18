# Runs the bot through a series of games with all nump and diff settings
# Then reports results using ZKTestAnalysis

from ZKEngine import *
from ZKTestAnalysis import *

i = 1
for p in range(2,7):
	for d in range(1,4):
		for g in range(100):
			game = BotGame(i, p, d)
			game.play()
			i += 1

analyzelog()