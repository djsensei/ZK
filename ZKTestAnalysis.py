# Contains data analysis functions

# standard analysis. Defaults to ZKtestlog.txt but can be called with other filenames
def analyzelog(filename = 'ZKtestlog.txt'):
	games = open(filename).readlines()

	# winper = dict of winning percentages, indexed to 'nump+diff'
	winper = {}
	ng = {}
	nw = {}
	rtot = {}
	ravg = {}
	for g in range(len(games)):
		games[g] = games[g][:len(games[g])-1].split()
		i = str(games[g][1]) + str(games[g][2])
		last = len(games[g])-1
		if i in ng:
			ng[i] += 1
		else:
			ng[i] = 1
			nw[i] = 0.
			rtot[i] = 0.
		rtot[i] += len(games[g]) - 5
		if games[g][last] == 'win':
			nw[i] += 1

	for p in range(2,7):
		for d in range(3):
			i = str(p)+str(d+1)
			winper[i] = nw[i] / ng[i] * 100
			ravg[i] = rtot[i] / ng[i]
			print("%s play %s diff: winper %s, avgrounds %s" % (i[0], i[1], int(winper[i]), int(ravg[i])))
		print()