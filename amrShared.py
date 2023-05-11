#==================================================
# Contains a bunch of functions that are used across all the scripts.
#==================================================
def writeValueToRom(romname,address,value,bytes):
	romname.seek(address)
	romname.write(value.to_bytes(bytes,'big'))

#==================================================
# Reverses the placement of an INT value.
#==================================================
def ShiftHex(hex): 
	#Shift by 8 bytes, and then, move the right most byte to the left;
	return ((hex >> 8) & 0xff) | ((hex << 8) & 0xff00)

def ConcatHex(a, b):
	aHex = ShiftHex(a)
	bHex = ShiftHex(b)
	return aHex << 16 | bHex #Make space for the bHex value;


#==================================================
# JSON Manager
#==================================================
import json

enemies = json.load(open('JSON\enemies.json'))
items = json.load(open('JSON\items.json'))
minibosses = json.load(open('JSON\minibosses.json'))
mirrors = json.load(open('JSON\mirrors.json'))

def GetEnemiesJSON():
	return enemies

def GetItemsJSON():
	return items

def GetMinibossesJSON():
	return minibosses

def GetMirrorsJSON():
	return mirrors

def GetObject(json, name):
	return json[name]

def GetParameter(json, name, parameter):
	return json[name][parameter]

#==================================================
# Dictionaries
#==================================================
def LoadJSONInDictionary(json, parameter):
	dictionary = {}

	for object in json:
		objectName = str(object)
		objectItems = json[objectName][parameter]
		dictionary[objectName] = objectItems
	
	return dictionary

#Get Dictionary Values
def GetEnemy(key):
	return enemyDictionary[key]

def GetItem(key):
	return itemDictionary[key]

enemyDictionary = LoadJSONInDictionary(GetEnemiesJSON(), "id")
itemDictionary = LoadJSONInDictionary(GetItemsJSON(), "item")

print(GetParameter(GetItemsJSON(), "Cherry", "item"))