''' 
This file contains the card data for all types of cards.
Dictionaries are the only elements in here:
ingnamenum, ingabbvnum, ingnumabbv, ingnumabbv, ingabbvname,
ingdata, cakedata, empdata, zombiedata
'''

ingnamenum = {
'batter':0, 
'frosting':1, 
'chocolate':2, 
'sprinkles':3, 
'creamcheese':4,
'whitechocolate':5,
'berries':6,
'nuts':7,
'dye':8,
'carrots':9,
'wildcard':10}

ingabbvnum = {
'B':0,
'F':1, 
'C':2,
'S':3,
'Ch':4,
'W':5, 
'Be':6,
'N':7,
'R':8,
'Ca':9,
'?':10}

ingnumname = dict((val,key) for key, val in ingnamenum.items())

ingnumabbv = dict((val,key) for key, val in ingabbvnum.items())

ingabbvname = {
'B':'batter',
'F':'frosting', 
'C':'chocolate',
'S':'sprinkles',
'Ch':'creamcheese',
'W':'whitechocolate', 
'Be':'berries',
'N':'nuts',
'R':'dye',
'Ca':'carrots',
'?':'wildcard'}

# ingredient cards (name, initial, frequency)
ingdata = {
'batter':('Batter', 'B', 5),
'frosting':('Frosting', 'F', 3),
'chocolate':('Chocolate', 'C', 3),
'sprinkles':('Sprinkles', 'S', 2),
'creamcheese':('Cream Cheese', 'Ch', 2),
'whitechocolate':('White Chocolate', 'W', 2),
'berries':('Berries', 'Be', 2),
'nuts':('Nuts', 'N', 2),
'dye':('Red Dye', 'R', 1),
'carrots':('Carrots', 'Ca', 1)}

# cake cards (name, power, ingredients, frequency)
# ingredients, by initial: [B F C S Ch W Be N R Ca ?]
cakedata = {
'wedding':('Wedding Cake', 10, [2,1,0,0,1,1,0,0,0,0,0], 2),
'bundt':('Bundt Cake', 2, [2,0,0,0,0,0,0,0,0,0,1], 2),
'pound':('Pound Cake', 3, [3,0,0,0,0,0,0,0,0,0,0], 2),
'cupcakes':('Cupcakes', 2, [1,1,0,0,0,0,0,0,0,0,1], 2),
'devilsfood':("Devil's Food Cake", 3, [1,1,1,0,0,0,0,0,0,0,0], 2),
'redvelvet':('Red Velvet Cake', 8, [1,0,0,0,0,1,0,0,1,0,0], 2),
'angelfood':("Angel Food Cake", 4, [1,1,0,0,0,1,0,0,0,0,0], 2),
'cheesecake':('Cheesecake', 6, [0,0,0,0,1,0,1,0,0,0,0], 2),
'birthday':('Birthday Cake', 5, [1,1,0,1,0,0,0,0,0,0,0], 2),
'donuts':('Donuts', 2, [1,0,0,1,0,0,0,0,0,0,0], 2),
'chess':('Chess Cake', 5, [1,0,1,0,0,1,0,0,0,0,0], 2),
'carrot':('Carrot Cake', 8, [1,0,0,0,1,0,0,0,0,1,0], 2),
'surprise':('Surprise Cake', 4, [1,0,0,1,0,0,0,0,0,0,2], 2),
'jellyroll':('Jelly Roll', 5, [1,1,0,0,0,0,1,0,0,0,0], 2),
'fruitcake':('Fruitcake', 6, [0,0,0,0,0,0,1,1,0,0,2], 2),
'brownies':('Fudge Brownies', 6, [0,1,2,0,0,0,0,1,0,0,0], 2)}

# zombie cards (name, hunger, gender, cakecrave, ingredientcrave) 
zombiedata = {
'cop':('Officer Brainsley', 6, 'He', 'donuts', None),
'brokenheart':('Breakup Betty', 8, 'She', None, 'chocolate'),
'stoner':('Stoney', 9, 'He', None, 'frosting'),
'z10':('Lobey Cephalonut', 10, 'He', None, None),
'z9':('Hoffer', 9, 'He', None, None),
'z8':('Chimpo', 8, 'He', None, None),
'z7':('Raudabaugh', 7, 'He', None, None),
'z6':('Aekta', 6, 'She', None, None),
'z5':('Brooking', 5, 'She', None, None),
'z4':('Doug', 4, 'He', None, None),
'z3':('Ethan', 3, 'He', None, None),
'z2':('Albus', 2, 'He', None, None),
'wedding':('Crank and Stepho', 15, 'They', 'wedding', None),
'grandma':('Grandma', 5, 'She', 'bundt', None),
'aunt':('Aunt Bertha', 8, 'She', 'fruitcake', None),
'hippie':('Brainful Zed', 11, 'He', 'carrot', None),
'sorority':('Zeta Mu Beta', 4, 'She', 'cupcakes', None),
'clown':('Chucklebellum', 7, 'He', 'surprise', None),
'birthday':("Billy's 5th Birthday Party", 7, 'They', 'birthday', None),
'chessmaster':('Cere Zasparov', 8, 'He', 'chess', None),
'reverend':('Reverend Cortex', 6, 'He', 'angelfood', None)}