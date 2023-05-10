#==================================================
#Contains a bunch of functions that are used across all the scripts.
#==================================================
def writeValueToRom(romname,address,value,bytes):
	romname.seek(address)
	romname.write(value.to_bytes(bytes,'big'))

#==================================================
#Reverses the placement of an INT value.
#==================================================
def ShiftHex(hex): 
	#Shift by 8 bytes, and then, move the right most byte to the left;
	return ((hex >> 8) & 0xff) | ((hex << 8) & 0xff00)

def ConcatHex(a, b):
	aHex = ShiftHex(a)
	bHex = ShiftHex(b)
	return aHex << 16 | bHex #Make space for the bHex value;