#This script randomizes the chests and items in the game.
#The data that keeps track of which rooms have treasures in them on the in-game map are intertwined with the mirror locations list.
#If we're randomizing the chests, we need to essentially make our own list in order for everything to work squeaky clean.
#It's ugly but it works.
import random
import os
import json
from amrShared import *
from amrConfig import *

print("Randomizing chests and items...")

#==================================================
# Loading Weights for Random Generation
#==================================================

# Creates an array with the weights specified
def GetWeightItem(name, pointer):
	return [GetItem(name)] * itemWeights[pointer]

#Referencing amrConfig
weightReference = [("Cherry", 0), ("Drink", 1), ("Meat", 2), ("Battery", 3),
	 	("Tomato", 4), ("1Up", 5), ("Candy", 6), ("MirrorShards", 7)]
weightedItemsToRandomize = []

for item in weightReference: #Fuses created arrays
	weightedItemsToRandomize.extend(GetWeightItem(item[0], item[1]))

#==================================================
# Loading Weights for Random Generation
#==================================================

def randomizeItems(romFile,randomMode):
	items = GetItemsJSON()
	itemlist = []
	itemadd = []
	itemxy = []
	itemroom = []
	
	#If it's not a chest, then shuffle it if the user decides so
	def ManageAddressData(name, value):
		if(name == "BigChest" or name == "SmallChest" or name == "Unrandomized"):
			itemadd.append(value)
		else:
			if randomMode == "Shuffle Items":
				itemlist.extend(GetItem(name)[0])
			else:
				itemlist.extend(random.choice(weightedItemsToRandomize))

	#Load object's data based on its name
	def LoadObjectData(object):
		for key in GetObject(items, object):
			for value in GetParameter(items, object, key):
				match key:
					case "item": itemlist.append(value)
					case "address": ManageAddressData(object, value)
					case "xy": itemxy.append(value) 
					case "room":itemroom.append(value)

	#Loading all the pertinent data to shuffle
	LoadObjectData("BigChest")
	LoadObjectData("SmallChest")

	for item in weightReference: #All other items;
		LoadObjectData(item[0])
	random.shuffle(itemlist)

	#Writing to rom
	for i in range(len(itemadd)):
		break
		#print[itemlist[i]]
		#writeValueToRom(romFile, itemadd[i], itemlist[i][0], 6)
		
	#==================================================
	# Chests & Non-Randomizable items;
	#==================================================
	LoadObjectData("Unrandomized")
	
	#Move the item list over one room, as it generates discrepancies
	for room in range(len(itemroom)):
		if itemroom[room] >= 4:
			itemroom[room] += 1
	
	def chestlistAppend(list, room, value):
		if list[room][0] == 0:
			list[room][0] = value
		else:
			list[room].append(value)

	chestlist = [0] * 287
	itemindex = 0

	#Add the new XYs of the chests to the chestlist
	for x in items["SmallChest"]["item"]:
		itemindex = itemlist.index(x)
		chestlistAppend(chestlist,itemroom[itemindex],itemxy[itemindex])
		
	for x in items["BigChest"]["item"]:
		itemindex = itemlist.index(x)
		chestlistAppend(chestlist,itemroom[itemindex],itemxy[itemindex])
	
	for x in items["Unrandomized"]["item"]:
		itemindex = itemlist.index(x)
		chestlistAppend(chestlist,itemroom[itemindex],itemxy[itemindex])

	#Create a new 9ROM list of our own. Oh dear.
	eof = False
	olposition = 9441164 # "Original List" position.
	nlposition = 14745600 # "New List" position.
	nlroomstart = nlposition # We need to keep track of where the room begins so we can write our pointers.
	copydata = 0
	endofroom = False
	roomnumber = 0
	readvalue = 0
	chestcount = 0
	
	print("Creating new treasure table...")
	while eof == False:
		#First, check if we're done here.
		if olposition <= 9449747:
			#Reset these things.
			endofroom = False 
			chestcount = 0
			nlroomstart = nlposition

			#First, let's write our chests to the new list if the are any in this room we're on.
			if chestlist[roomnumber][0] != 0:
				chestcount = len(chestlist[roomnumber])
				for x in chestlist[roomnumber]:
					romFile.seek(nlposition)
					romFile.write(int(17367039).to_bytes(4,'big'))
					romFile.write(x.to_bytes(4,'big'))
					nlposition += 8
					
			#Now we copy the 02 08s.
			while endofroom == False:
				romFile.seek(olposition)
				readvalue = int.from_bytes(romFile.read(4),'big')
				
				if readvalue == 17367039:
					#If our readvalue is 01 08 FF FF, it's a chest. Skip it.
					olposition += 8
				elif readvalue == 34144255:
					#If our readvalue is 02 08 FF FF, it's a mirror. Copy it to the new list.
					romFile.seek(olposition)
					copydata = int.from_bytes(romFile.read(8),'big')
					romFile.seek(nlposition)
					romFile.write(copydata.to_bytes(8,'big'))
					nlposition += 8
					olposition += 8

				elif readvalue == 65535:
					#If our readvalue is 00 00 FF FF, it's the end of the room.
					olposition += 12
					romFile.seek(nlposition)
					romFile.write(int(65535).to_bytes(4,'big'))
					
					#We have to tell the game to look at this new list, so let's tinker with a pointer or two.
					nlposition += 4
					romFile.write(int(nlroomstart+134217728).to_bytes(4,'little'))
					
					#The list of pointers starts at 0xD2F4C0
					romFile.seek((13825216) + (4 * roomnumber))
					romFile.write(int(nlposition+134217728).to_bytes(4,'little'))
					nlposition += 4
					
					#Finally we have to write a byte counting how many chests are in this room.
					romFile.seek(nlposition)
					romFile.write(chestcount.to_bytes(1,'big'))
					nlposition += 4
					
					#Tick up the room counter and get us out of this loop!
					roomnumber += 1
					endofroom = True
		else:
			#Rangers lead the way.
			eof = True
#==================================================