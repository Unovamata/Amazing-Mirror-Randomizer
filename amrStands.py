#This script randomizes the ability statues found in the switch and pre-boss rooms.
import json
import os
import random
from amrShared import *
#==================================================
def randomizeStands(romFile,randomMode):
	print("Randomizing ability stands...")
	items = json.load(open('JSON\items.json'))
	itemlist = []
	itemadd = []

	for x in items["AbilityStand"]["item"]:
		if randomMode == "Shuffle":
			itemlist.append(x)
		#Bomb, Hammer, Smash, Cutter, Sword, Rock
		elif randomMode == "Unlock Path Abilites Only":
			itemlist = [161624014979072, 162723526607104, 162723493052672, 164922465976320, 164922449199104, 161623981424896]
			continue
		elif x not in itemlist:
			itemlist.append(x)
			
	for x in items["AbilityStand"]["address"]:
		itemadd.append(x)

	if randomMode == "Shuffle Stands":
		random.shuffle(itemlist)
		for x in range(len(itemadd)):
			writeValueToRom(romFile,itemadd[x],itemlist[x],6)
	elif randomMode == "Unlock Path Abilites Only":
		for x in range(len(itemadd)):
			writeValueToRom(romFile, itemadd[x], random.choice(itemlist), 6)
	else:
		for x in range(len(itemadd)):
			writeValueToRom(romFile,itemadd[x],random.choice(itemlist),6)
#==================================================