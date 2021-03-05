#This script ranadomizes the mirrors, cannons, and warp starts.
import random
import os
import json
from amrShared import *
#==================================================
def findLinkedMirror(string):
	underscore = string.find("_")
	return string[underscore+1:len(string)] + "_" + string[0:underscore]

def removeBrackets(value):
	value = str(value)
	value = value.strip("[")
	value = value.strip("]")
	return int(value)

def randomizeMirrors(romFile,spoilerLogEnable,totalRandom,spoilerLogFileName):
	mirrors = json.load(open('JSON\mirrors.json'))
	mirrorlist = list(mirrors.keys())
	
	mirrorlist.remove("Rbr1_AbilityRoom")
	mirrorlist.remove("AbilityRoom_Rbr1")
	mirrorlist.remove("Int1_Int2")
	mirrorlist.remove("Int2_Int3")
	mirrorlist.remove("Int3_Int2")
	mirrorlist.remove("Car19_Reset") #Cause it's fucking aggrivating
	mirrorlist.remove("Car19_N")
	mirrorlist.remove("Car19_NE")
	mirrorlist.remove("Car19_E")
	mirrorlist.remove("Car19_SE")
	mirrorlist.remove("Car19_S")
	mirrorlist.remove("Car19_SW")
	mirrorlist.remove("Car19_W")
	mirrorlist.remove("Car19_NW")

	#I've removed the option to randomize hub mirrors. It's not fun, and it just caused problems I'm too lazy to fix.
	mirrorlist.remove("Rbr1_Rbr27")
	mirrorlist.remove("Rbr27_Rbr1")
	mirrorlist.remove("Rbr1_Can10")
	mirrorlist.remove("Can10_Rbr1")
	mirrorlist.remove("Rbr1_Cab8")
	mirrorlist.remove("Cab8_Rbr1")
	mirrorlist.remove("Rbr1_Pep5")
	mirrorlist.remove("Pep5_Rbr1")
	mirrorlist.remove("Rbr1_Mnl4")
	mirrorlist.remove("Mnl4_Rbr1")
	mirrorlist.remove("Rbr1_Rbr21")
	mirrorlist.remove("Rbr21_Rbr1")
	mirrorlist.remove("Rbr1_Rbr8")
	mirrorlist.remove("Rbr8_Rbr1")
	mirrorlist.remove("Rbr1_Cab19")
	mirrorlist.remove("Cab19_Rbr1")
	mirrorlist.remove("Rbr1_Rbr15")
	mirrorlist.remove("Rbr15_Rbr1")
	mirrorlist.remove("Rbr27_Mus12")
	mirrorlist.remove("Mus12_Rbr27")
	mirrorlist.remove("Rbr15_Cab17")
	mirrorlist.remove("Cab17_Rbr15")
	mirrorlist.remove("Rbr21_Car5")
	mirrorlist.remove("Car5_Rbr21")
	mirrorlist.remove("Cab19_Oli11")
	mirrorlist.remove("Oli11_Cab19")
	mirrorlist.remove("Cab8_Rad12")
	mirrorlist.remove("Rad12_Cab8")
	mirrorlist.remove("Pep5_Pep24")
	mirrorlist.remove("Pep24_Pep5")

	#If we're generating a spoiler log, edit the random seed so that people can't cheat during races or something.
	if spoilerLogEnable == 1:
		random.seed(random.randint(0,999999))
	
	#Change the appearance of trans-world mirrors.
	worldadds = [ 8936124, 8936160, 8938120, 8943824, 8943860, 8944700, 8945536, 8948624, 8952188, 8955204, 8956436, 8959468, 8960196, 8970592, 8977420, 8978776, 8986156, 8988736, 8989284, 8991428, 8992080, 8994916, 9015868, 9018236, 9024384, 9024820, 9032592, 9040044, 9044108, 9049652, 9054584, 9055424, 9056184 ]
	for x in range(len(worldadds)):
		romFile.seek(worldadds[x] - 4) 						# Seek to the Y position of the door
		yPos = int.from_bytes(romFile.read(2),'little') - 8	# Move the door up 8 pixels so it overlaps the warp tile.
		romFile.seek(worldadds[x]-4)
		romFile.write(yPos.to_bytes(2,'little'))			# Write the changed Y coordinate.
		writeValueToRom(romFile,worldadds[x],111,1)			# Change the object number of the mirror to 6F (a regular mirror).
		writeValueToRom(romFile,worldadds[x]+2,1,1)			# This byte changes whether or not the mirror has a "boarded up sprite" if not on a revealed warp tile. This makes them look proper if they're hidden by a mirra.
	
	#Change the appearance of mirrors exiting switch rooms.
	hubadds = [ 9040044, 9040188, 9014668, 9014632, 9056436, 9056472, 8970048, 8970012, 9000960, 9000924, 9036740, 9036704, 8982812, 8982776, 8988520, 8988556, 9049760, 9049832, 8945356, 8945392, 8947464, 8947500, 8959284, 8959320, 8940048, 8940084, 9024020, 9024056, 9024276, 9024384 ]
	for x in range(len(hubadds)):
		romFile.seek(hubadds[x] - 4) 						# Seek to the Y position of the door
		yPos = int.from_bytes(romFile.read(2),'little') + 8	# Move the door down 8 pixels so it overlaps the warp tile.
		romFile.seek(hubadds[x]-4)
		romFile.write(yPos.to_bytes(2,'little'))			# Write the changed Y coordinate.
		writeValueToRom(romFile,hubadds[x],153,1)			# Change the object number of the mirror to 99 (a world mirror).
		writeValueToRom(romFile,hubadds[x]+2,1,1)			# This byte changes whether or not the mirror has a "boarded up sprite" if not on a revealed warp tile. This makes them look proper if they're hidden by a mirra.
	
	#Randomize warp stars.
	print("Randomizing warp stars...")
	warpstaradds = [ [ 8944554, 8944566 ], [ 8964698, 8964710 ], [ 8981034, 8981046 ], [ 8998010, 8998022 ], [ 9006434, 9006446 ], [ 9065234, 9065246 ] ]
	warpstarvalues = [ [ 0, 277076896629504, [ "Mnl1_Mnl2" ] ], [ 4, 69269484247297, [ "Can1_Can9", "Can1_Can2" ] ], [ 1, 12094879601665, [ "Can4_Can6", "Can4_Can2", "Can4_Can5Carbon" ] ], [ 2, 281471017324801, [ "Can7_Can9", "Can7_Can6", "Can7_Can8" ] ], [ 3, 5497809837825, [ "Can21_Can22" ] ], [ 5, 281470681800192, [ "Pep23_Pep24", "Pep23_Car4" ] ] ]

	random.shuffle(warpstarvalues)
	for x in range(len(warpstaradds)):
		writeValueToRom(romFile,warpstaradds[x][0],warpstarvalues[x][0],1)
		writeValueToRom(romFile,warpstaradds[x][1],warpstarvalues[x][1],6)
	
	#Randomize fused cannons.
	print("Randomizing CANNONs stars...")
	cannonadds = [ 8951430, 8999618, 9033722, 9050022 ]
	cannonvalues = [ [ 4179903404153243910, [ "Rbr26_Rbr27", "Rbr26_Rbr25" ] ], [ 3170817811668802562, [ "Mus24L_Kracko" ] ], [ 9583663305579299867, [ "Oli5Bottom_Oli6" ] ], [ 937313871469740802, [ "Rad28_Rad29" ] ] ]

	random.shuffle(cannonvalues)
	for x in range(len(cannonadds)):
		writeValueToRom(romFile,cannonadds[x],cannonvalues[x][0],8)

	#We need to filter our mirror list into two other lists: a dead end list and a...not...dead end list.
	#We're gonna check if the one-way mirror entry (Type 1) is labeled as 'DEADEND'.
	#Then we're gonna check (if total random mode is off) if there's only one possible exit out of a two-way mirror.
	mirrorListRandomized = []
		
	for x in range(len(mirrorlist)):
		mirrorListRandomized.append('NULL')
		
	#Please note that these are the "Pre" random lists.
	if totalRandom == "Normal Mode":
		twoWayPreRandomList = []
		oneWayPreRandomList = []
		deadEndTwoWayPreRandomList = []
		deadEndOneWayPreRandomList = []
	else:
		mirrorPreRandomList = []
		deadEndPreRandomList = []

	print("Determining dead ends...")
	for x in mirrorlist:
		if mirrors[x]['type'][0] == 1:
			if totalRandom == "Normal Mode":
				if len(mirrors[x]['exits']) == 1:
					deadEndTwoWayPreRandomList.append(x)
				else:
					twoWayPreRandomList.append(x)
			else:
				mirrorPreRandomList.append(x)
		else:
			if 'DEADEND' in mirrors[x]['exits']:
				if totalRandom == "Normal Mode":
					deadEndOneWayPreRandomList.append(x)
				else:
					deadEndPreRandomList.append(x)
			else:
				if totalRandom == "Normal Mode":
					oneWayPreRandomList.append(x)
				else:
					mirrorPreRandomList.append(x)

	print("Randomizing mirrors...")
	if totalRandom == "Normal Mode":
		random.shuffle(twoWayPreRandomList)
		random.shuffle(oneWayPreRandomList)
		random.shuffle(deadEndTwoWayPreRandomList)
		random.shuffle(deadEndOneWayPreRandomList)
	else:
		random.shuffle(mirrorPreRandomList)
		random.shuffle(deadEndPreRandomList)
		
	#The queue list. Once this runs out, the rest of the mirrors that aren't randomized get filled with dead ends.
	#Once an entrance is randomized, its exits are added to the queue.
	queueList = [ "Rbr1_Rbr2" ] #Start with the first mirror.
	spoilerLogLists = [["Rbr1_Rbr2"]]
	alreadyRandomized = []
	mirrorlistRandomized = []
	for x in range(len(mirrorlist)):
		mirrorlistRandomized.append('NULL')

	if totalRandom == "Total Random":
		while len(queueList) > 0:
			currentPick = queueList[0]
			
			#Spoiler log stuff.
			spoilerLogFirstExit = True #We only want to make a new list int he spoiler log if the path branches.
			for x in spoilerLogLists:
				if x[-1] == currentPick:
					spoilerLogCurrentIndex = spoilerLogLists.index(x)
					spoilerLogCurrentString = x.copy()
			
			#If the exit is a CANNON or a WARPSTAR, add the exits for that warpstar or CANNON to the list and move on.
			if currentPick.startswith("WARPSTAR") and not ( currentPick in alreadyRandomized ):
				alreadyRandomized.append(currentPick)
				for x in warpstarvalues[int(currentPick[8])-1][2]:
					if not x in alreadyRandomized:
						queueList.append(x)
						#Spoiler Log Stuff
						if spoilerLogFirstExit == True:
							spoilerLogFirstExit = False
							spoilerLogLists[spoilerLogCurrentIndex].append(x)
						else:
							spoilerLogLists.append(spoilerLogCurrentString.copy())
							spoilerLogLists[-1].append(x)
			elif currentPick.startswith("CANNON") and not ( currentPick in alreadyRandomized ):
				alreadyRandomized.append(currentPick)
				for x in cannonvalues[int(currentPick[5])-1][1]:
					if not x in alreadyRandomized:
						queueList.append(x)
						#Spoiler log stuff
						if spoilerLogFirstExit == True:
							spoilerLogFirstExit = False
							spoilerLogLists[spoilerLogCurrentIndex].append(x)
						else:
							spoilerLogLists.append(spoilerLogCurrentString.copy())
							spoilerLogLists[-1].append(x)

			#If it's not a CANNON or a WARPSTAR, then it's probably something we can work with?
			elif currentPick in mirrorlist:
				currentPickId = mirrorlist.index(currentPick)
				#Dead-end test. If a mirror's exits are all already randomized, add it to the dead-end list and re-random.
				isGoodCheck = False
				while isGoodCheck == False:
					alreadyCheck = 0
					if len(mirrorPreRandomList) == 0:
						isGoodCheck = True
					else:
						for x in mirrors[mirrorPreRandomList[0]]['exits']:
							if x in alreadyRandomized:
								alreadyCheck += 1
							elif x in queueList:
								alreadyCheck += 1
						if alreadyCheck == len(mirrors[mirrorPreRandomList[0]]['exits']):
							deadEndPreRandomList.append(mirrorPreRandomList[0])
							random.shuffle(deadEndPreRandomList)
							del mirrorPreRandomList[0]
						else:
							isGoodCheck = True
				
				if not currentPick in alreadyRandomized:
					#Spoiler log stuff here.
					alreadyRandomized.append(currentPick)
					if len(mirrorPreRandomList) > 0:
						for x in mirrors[mirrorPreRandomList[0]]['exits']:
							if not x in alreadyRandomized:
								queueList.append(x)
								#Spoiler log stuff
								if spoilerLogFirstExit == True:
									spoilerLogFirstExit = False
									spoilerLogLists[spoilerLogCurrentIndex].append(x)
								else:
									spoilerLogLists.append(spoilerLogCurrentString.copy())
									spoilerLogLists[-1].append(x)
						mirrorlistRandomized[currentPickId] = mirrorPreRandomList[0]
						del mirrorPreRandomList[0]
					else:
						mirrorlistRandomized[currentPickId] = deadEndPreRandomList[0]
						#Remove this string from the spoiler log list.
						spoilerLogCurrentIndex = spoilerLogLists.index(spoilerLogCurrentString)
						spoilerLogLists[spoilerLogCurrentIndex].append("END " + deadEndPreRandomList[0])
						del deadEndPreRandomList[0]

			#This means the exit isn't scheduled to be randomized. Mark it as already randomized, but don't do anything with mirrorlistRandomized.
			else:
				if not currentPick in alreadyRandomized:
					alreadyRandomized.append(currentPick)
					for x in mirrors[currentPick]['exits']:
						if not x in alreadyRandomized:
							queueList.append(x)
							#Spoiler log stuff
							if spoilerLogFirstExit == True:
								spoilerLogFirstExit = False
								spoilerLogLists[spoilerLogCurrentIndex].append(x)
							else:
								spoilerLogLists.append(spoilerLogCurrentString.copy())
								spoilerLogLists[-1].append(x)
			
			queueList.remove(currentPick)
			
			if len(queueList) == 0:
				for x in range(len(mirrorlistRandomized)):
					if mirrorlistRandomized[x] == "NULL":
						if mirrorlist[x] in alreadyRandomized:
							alreadyRandomized.remove(mirrorlist[x])
							print("ERROR: FOUND NULL")
						queueList.append(mirrorlist[x])

	#Non-total random.
	else:
		while len(queueList) > 0:
			currentPick = queueList[0]
		
			#Spoiler log stuff.
			spoilerLogFirstExit = True #We only want to make a new list int he spoiler log if the path branches.
			for x in spoilerLogLists:
				if x[-1] == currentPick:
					spoilerLogCurrentIndex = spoilerLogLists.index(x)
					spoilerLogCurrentString = x.copy()
		
			#If the exit is a CANNON or a WARPSTAR, add the exits for that warpstar or CANNON to the list and move on.
			if currentPick.startswith("WARPSTAR") and not ( currentPick in alreadyRandomized ):
				alreadyRandomized.append(currentPick)
				for x in warpstarvalues[int(currentPick[8])-1][2]:
					if not x in alreadyRandomized:
						queueList.append(x)
						#Spoiler Log Stuff
						if spoilerLogFirstExit == True:
							spoilerLogFirstExit = False
							spoilerLogLists[spoilerLogCurrentIndex].append(x)
						else:
							spoilerLogLists.append(spoilerLogCurrentString.copy())
							spoilerLogLists[-1].append(x)
			elif currentPick.startswith("CANNON") and not ( currentPick in alreadyRandomized ):
				alreadyRandomized.append(currentPick)
				for x in cannonvalues[int(currentPick[6])-1][1]:
					if not x in alreadyRandomized:
						queueList.append(x)
						#Spoiler Log Stuff
						if spoilerLogFirstExit == True:
							spoilerLogFirstExit = False
							spoilerLogLists[spoilerLogCurrentIndex].append(x)
						else:
							spoilerLogLists.append(spoilerLogCurrentString.copy())
							spoilerLogLists[-1].append(x)

			#If it's not a CANNON or a WARPSTAR, then it's probably something we can work with?
			elif currentPick in mirrorlist:
				currentPickId = mirrorlist.index(currentPick)
				#Dead-end test. If a mirror's exits are all already randomized, add it to the dead-end list and re-random.
				isGoodCheck = False
				while isGoodCheck == False:
					alreadyCheck = 0
					if mirrors[currentPick]['type'][0] == 1:
						if len(twoWayPreRandomList) == 0:
							isGoodCheck = True
						else:
							#If all a mirror's exits are already randomized, move it to the dead end list.
							for x in mirrors[twoWayPreRandomList[0]]['exits']:
								if x in alreadyRandomized:
									alreadyCheck += 1
								elif x in queueList:
									alreadyCheck += 1
							if alreadyCheck == len(mirrors[twoWayPreRandomList[0]]['exits']):
								deadEndTwoWayPreRandomList.append(twoWayPreRandomList[0])
								random.shuffle(deadEndTwoWayPreRandomList)
								del twoWayPreRandomList[0]
							else:
								isGoodCheck = True
					else:
						if len(oneWayPreRandomList) == 0:
							isGoodCheck = True
						else:
							#If all a mirror's exits are already randomized, move it to the dead end list.
							for x in mirrors[oneWayPreRandomList[0]]['exits']:
								if x in alreadyRandomized:
									alreadyCheck += 1
								elif x in queueList:
									alreadyCheck += 1
							if alreadyCheck == len(mirrors[oneWayPreRandomList[0]]['exits']):
								deadEndOneWayPreRandomList.append(oneWayPreRandomList[0])
								random.shuffle(deadEndOneWayPreRandomList)
								del oneWayPreRandomList[0]
							else:
								isGoodCheck = True
				
				if not currentPick in alreadyRandomized:
					alreadyRandomized.append(currentPick)
					if mirrors[currentPick]['type'][0] == 1:
						#Do some more tests as to whether or not the possible pair is a dead end or not.
						deadendTest = False
						while deadendTest == False:
							if len(twoWayPreRandomList) == 0:
								deadendTest = True
							else:
								deadEndCount = 0
								for x in mirrors[twoWayPreRandomList[0]]['exits']:
									if x in alreadyRandomized:
										deadEndCount += 1
								if deadEndCount == len(mirrors[twoWayPreRandomList[0]]['exits']):
									deadEndTwoWayPreRandomList.append(twoWayPreRandomList[0])
									del twoWayPreRandomList[0]
								else:
									deadendTest = True
							
						if len(twoWayPreRandomList) > 0:
							while twoWayPreRandomList[0] == findLinkedMirror(currentPick):
								random.shuffle(twoWayPreRandomList)
							for x in mirrors[twoWayPreRandomList[0]]['exits']:
								if not x in alreadyRandomized:
									queueList.append(x)
									#Spoiler Log Stuff
									if spoilerLogFirstExit == True:
										spoilerLogFirstExit = False
										spoilerLogLists[spoilerLogCurrentIndex].append(x)
									else:
										spoilerLogLists.append(spoilerLogCurrentString.copy())
										spoilerLogLists[-1].append(x)
							mirrorlistRandomized[currentPickId] = twoWayPreRandomList[0]
							mirrorlistRandomized[mirrorlist.index(findLinkedMirror(twoWayPreRandomList[0]))] = findLinkedMirror(currentPick)
							alreadyRandomized.append(mirrorlist[mirrorlist.index(findLinkedMirror(twoWayPreRandomList[0]))])
							if findLinkedMirror(currentPick) in twoWayPreRandomList:
								twoWayPreRandomList.remove(findLinkedMirror(currentPick))
							else:
								deadEndTwoWayPreRandomList.remove(findLinkedMirror(currentPick))
							del twoWayPreRandomList[0]
						else:
							while deadEndTwoWayPreRandomList[0] == findLinkedMirror(currentPick):
								random.shuffle(deadEndTwoWayPreRandomList)
							mirrorlistRandomized[currentPickId] = deadEndTwoWayPreRandomList[0]
							mirrorlistRandomized[mirrorlist.index(findLinkedMirror(deadEndTwoWayPreRandomList[0]))] = findLinkedMirror(currentPick)
							alreadyRandomized.append(mirrorlist[mirrorlist.index(findLinkedMirror(deadEndTwoWayPreRandomList[0]))])
							
							deadEndTwoWayPreRandomList.remove(findLinkedMirror(currentPick))
							#Don't bother adding this to the spoiler log cause we only care about one-way dead ends.
							del deadEndTwoWayPreRandomList[0]
					else:
						if len(oneWayPreRandomList) > 0:
							for x in mirrors[oneWayPreRandomList[0]]['exits']:
								if not x in alreadyRandomized:
									queueList.append(x)
									#Spoiler Log Stuff
									if spoilerLogFirstExit == True:
										spoilerLogFirstExit = False
										spoilerLogLists[spoilerLogCurrentIndex].append(x)
									else:
										spoilerLogLists.append(spoilerLogCurrentString.copy())
										spoilerLogLists[-1].append(x)
							mirrorlistRandomized[currentPickId] = oneWayPreRandomList[0]
							del oneWayPreRandomList[0]
						else:
							mirrorlistRandomized[currentPickId] = deadEndOneWayPreRandomList[0]
							#Remove this string from the spoiler log list.
							spoilerLogCurrentIndex = spoilerLogLists.index(spoilerLogCurrentString)
							spoilerLogLists[spoilerLogCurrentIndex].append("END " + deadEndOneWayPreRandomList[0])
							del deadEndOneWayPreRandomList[0]
						
			#This means the exit isn't scheduled to be randomized. Mark it as already randomized, but don't do anything with mirrorlistRandomized.
			else:
				if not currentPick in alreadyRandomized:
					alreadyRandomized.append(currentPick)
					for x in mirrors[currentPick]['exits']:
						if not x in alreadyRandomized:
							queueList.append(x)
							#Spoiler Log Stuff
							if spoilerLogFirstExit == True:
								spoilerLogFirstExit = False
								spoilerLogLists[spoilerLogCurrentIndex].append(x)
							else:
								spoilerLogLists.append(spoilerLogCurrentString.copy())
								spoilerLogLists[-1].append(x)

			queueList.remove(currentPick)
			
			if len(queueList) == 0:
				for x in range(len(mirrorlistRandomized)):
					if mirrorlistRandomized[x] == "NULL":
						if mirrorlist[x] in alreadyRandomized:
							alreadyRandomized.remove(mirrorlist[x])
							print("ERROR: FOUND NULL")
						queueList.append(mirrorlist[x])
	
	#Generate the spoiler log.
	spoilerLogCompleted = []
	spoilerBosList = []
	for x in spoilerLogLists:
		if not x[-1].startswith("WARPSTAR") and not x[-1].startswith("CANNON") and x[-1].startswith("END "):
			#The reason we're adding "END" to the end of the dead ends is so it doesn't add any goal mirrors that happen to be randomized where the vanilla entrances to bosses are.
			if mirrors[x[-1][4:]]['type'][0] == 2:
				spoilerLogCompleted.append(x.copy())

	spoilerLogLists.clear()

	#Create the text spoiler now.
	if spoilerLogEnable == 1:
		spoilerTextFile = open(spoilerLogFileName,'w')
		for x in range(len(spoilerLogCompleted)):
			#Header
			if spoilerLogCompleted[x][-1] == "END Mnl10_BigGolem":
				spoilerTextFile.write("KING GOLEM")
			elif spoilerLogCompleted[x][-1] == "END Cab11_Moley":
				spoilerTextFile.write("MOLEY")
			elif spoilerLogCompleted[x][-1] == "END Mus24L_Kracko":
				spoilerTextFile.write("LEFT KRACKO ENTRANCE")
			elif spoilerLogCompleted[x][-1] == "END Mus24R_Kracko":
				spoilerTextFile.write("RIGHT KRACKO ENTRANCE")
			elif spoilerLogCompleted[x][-1] == "END Car22_MegaTitan":
				spoilerTextFile.write("MEGA TITAN")
			elif spoilerLogCompleted[x][-1] == "END Oli25_Gobbler":
				spoilerTextFile.write("GOBBLER")
			elif spoilerLogCompleted[x][-1] == "END Pep21_Wiz":
				spoilerTextFile.write("WIZ")
			elif spoilerLogCompleted[x][-1] == "END Rad22_DarkMetaKnight":
				spoilerTextFile.write("???")
			elif spoilerLogCompleted[x][-1] == "END Can27_CrazyHand":
				spoilerTextFile.write("CRAZY+MASTER HAND")

			for y in range(len(spoilerLogCompleted[x])-1):
				#The mirrors.json doesn't have entries for cannons or warpstars.
				if spoilerLogCompleted[x][y] == 'CANNON1':
					spoilerTextFile.write("\nRbr42 > Fused CANNON")
				elif spoilerLogCompleted[x][y] == 'CANNON2':
					spoilerTextFile.write("\nMus23L > Fused CANNON")
				elif spoilerLogCompleted[x][y] == 'CANNON3':
					spoilerTextFile.write("\nOli8 > Fused CANNON")
				elif spoilerLogCompleted[x][y] == 'CANNON4':
					spoilerTextFile.write("\nRad26 > Fused CANNON")
				elif spoilerLogCompleted[x][y] == 'WARPSTAR1':
					spoilerTextFile.write("\nRbr7 > Warpstar")
				elif spoilerLogCompleted[x][y] == 'WARPSTAR2':
					spoilerTextFile.write("\nMnl20 > Warpstar")
				elif spoilerLogCompleted[x][y] == 'WARPSTAR3':
					spoilerTextFile.write("\nPep29 > Warpstar")
				elif spoilerLogCompleted[x][y] == 'WARPSTAR4':
					spoilerTextFile.write("\nMus7 > Warpstar")
				elif spoilerLogCompleted[x][y] == 'WARPSTAR5':
					spoilerTextFile.write("\nCan20 > Warpstar")
				elif spoilerLogCompleted[x][y] == 'WARPSTAR6':
					spoilerTextFile.write("\nCar14 > Warpstar")
				else:
					spoilerTextFile.write("\n" + spoilerLogCompleted[x][y][0:spoilerLogCompleted[x][y].find('_')] + " > " + mirrors[spoilerLogCompleted[x][y]]['desc'][0])
					
			spoilerTextFile.write("\n\n")
	
	print("Writing mirrors to ROM...")
	for x in range(len(mirrorlist)):
		#Location warps in Amazing Mirror have two places in the ROM to change, else it softlocks.
		#We need to change both of them, and there could be any number of addresses to write to
		#to change just one warp.
		location = removeBrackets(mirrors[mirrorlistRandomized[x]]['location'])
		for y in mirrors[mirrorlist[x]]['eightrom']:
			writeValueToRom(romFile,y,location,5)
		for z in mirrors[mirrorlist[x]]['ninerom']:
			writeValueToRom(romFile,z,(location >> 8),4)
		
		if mirrors[mirrorlistRandomized[x]]['special'][0] == 1 and mirrors[mirrorlist[x]]['special'][0] != -1:
			romFile.seek(mirrors[mirrorlist[x]]['object'][0] - 4) 				# Seek to the Y position of the door
			yPos = int.from_bytes(romFile.read(2),'little') + 8					# Move the door down 8 pixels so it overlaps the warp tile.
			romFile.seek(mirrors[mirrorlist[x]]['object'][0] - 4)
			romFile.write(yPos.to_bytes(2,'little'))							# Write the changed Y coordinate.
			writeValueToRom(romFile,mirrors[mirrorlist[x]]['object'][0],153,1)	# Change the object number of the mirror to 99 (a world mirror).
			writeValueToRom(romFile,mirrors[mirrorlist[x]]['object'][0]+2,1,1)	# This byte changes whether or not the mirror has a "boarded up sprite" if not on a revealed warp tile. This makes them look proper if they're hidden by a mirra.
	
		elif mirrors[mirrorlistRandomized[x]]['special'][0] == 2 and mirrors[mirrorlist[x]]['special'][0] != -1:
			writeValueToRom(romFile,mirrors[mirrorlist[x]]['object'][0]+22,1,1)
		
#==================================================