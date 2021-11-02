#This script randomizes the ability statues found in the switch and pre-boss rooms.
import json
import os
import random
from amrShared import *
#==================================================
def randomizeEnemies(romFile,randomMode):
	print("Randomizing enemies...")
	enemies = json.load(open('JSON\enemies.json'))
	enemyadd = []

	#Setting the read parameters
	enemies_names = ["WaddleDee","BrontoBurt","Squishy","Scarfy","Gordo","Snooter","Chip","Soarar","Haley","RolyPoly","Cupie","Blockin","Leap","BigWaddleDee","WaddleDoo","Flamer","HotHead","LaserBall","Pengy","Rocky","SirKibble","Sparky","SwordKnight","UFO","Twister","Wheelie","Noddy","Golem","Alt1Golem","Alt2Golem","Shooty","Foley","Boxin","Cookin","Bomber","HeavyKnight","GiantRocky","MetalGuardian","Batty","BangBang","Droppy","Prank","Shotzo"]

	#Enemies ids;
	"""It is not advised to include the following enemies into the randomization:
	Blipper - [2] (It would lead to empty levels)
	Glunk - [3] (It would lead to empty levels)
	SnooterEmpty - [14] (It's empty, there's no entities associated to it)
	Jack - [16] (It can maybe crash the game)
	ScarfyEmpty - [36] (It's empty, there's no entities associated to it)
	Minny - [39] (Specifically for puzzles)
	Nothing - [44] (It's empty, there's no entities associated to it)
	FoleyAutomaticTrigger [46] - (It's empty, there's no entities associated to it)
	Explosion [48] - (It's empty, there's no entities associated to it)
	Nothing2 - [49] (It's empty, there's no entities associated to it)
	Mirra - [52] (Can lead to unbeatable seeds)
	Nothing3 - [54] (It has some entities, though it's better to leave it out of the mix)
	WaddleDee2 - [55] (Only one entity in the entire game, so it's best to skip)"""

	randomMode = "Randomize Enemies"

	#Randomizable enemies;
	ids = [0,1,4,5,6,7,8,9,10,11,12,13,15,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,37,38,40,41,42,43,45,47,50,51,53]
	ids_size = range(0, len(ids))
	random.shuffle(ids)

	#Shuffling the addresses
	for x in ids_size:
		for y in enemies[enemies_names[x]]["address"]:
			enemyadd.append(y)

	enemy_list_add_size = range(0, len(enemyadd))

	if randomMode == "Randomize Enemies":
		for z in enemy_list_add_size:
			#print("&",z)
			writeValueToRom(romFile, enemyadd[z], random.choice(ids), 1)