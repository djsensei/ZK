from ZKClasses import *

print("===== Someone's in the Kitchen With Zombies! =====")
nump = int(input("How many players (2-6)? "))
diff = int(input("How difficult (1 = easy, 2 = med, 3 = hard)? "))
game = Game(123123, nump, diff)
game.play()