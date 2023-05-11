from amrShared import *

''' * For starters, you'll need to access the following page:
    * https://www.tapatalk.com/groups/lighthouse_of_yoshi/kirby-and-the-amazing-mirror-hacking-t741.html
    * From there, you'll need to convert the id shown in the 
    * page above from hexadecimal to decimal. The decimal value
    * you converted is the number you'll use in this object scanner
    * script.
'''

#==================================================
# Open and process the object table;
#==================================================

#Data table including all the hex values starting with 01 24;
data = open("objecttable.bin",'rb+')
object = int(input("Please enter an object to look up: "))

#Start at byte 0C, where the first item is.
position = 12 #Find first object ID instead of the start of the file;
roomnumber = 0

objectaddress = [ ]
objectdata = [ ]
objectx = [ ]
objecty = [ ]
objectxy = [ ]
objectroom = [ ]

def SaveDataInformation():
        #Add object data to our arrays.
        objectaddress.append(position + 8932452) # Address - we add 8932452 since that's were the object table in the ROM starts.
        data.seek(position)
        objectdata.append(int.from_bytes(data.read(6),'big')) # Object ID / properties.
        data.seek(position-6)
        objectx.append(int.from_bytes(data.read(2),'little')) # X.
        data.seek(position-4)
        objecty.append(int.from_bytes(data.read(2),'little')) # Y.
        objectroom.append(roomnumber) # Room number.
        print(f"Object {objectdata[-1]} found in room {objectroom[-1]} Address: {objectaddress[-1]}, X/Y: {objectx[-1]}, {objecty[-1]}")

readvalue = -1

while True:
        if position >= 136871: break

        data.seek(position-4)
        readvalue = int.from_bytes(data.read(4),'big')

        #Have we reached the end of the room?
        if readvalue == 4294967295: #FF FF FF FF FF FF FF FF
                roomnumber += 1
                #Looking for 01 24 00 00 at the start of the object
                while readvalue != 19136512:
                        position += 4
                        data.seek(position)
                        readvalue = int.from_bytes(data.read(4),'big')
                #Move ahead to the object's ID.
                position += 12
        else:
                data.seek(position)
                readvalue = int.from_bytes(data.read(1),'big')
                if readvalue == object:
                        SaveDataInformation()
                position += 36

#==================================================
# Write information in the 'objectdata.txt' file
#==================================================

#Write parameters in the extracted data file.
def WriteParameter(description, data, isLast):
        output.write(f'    "{description}"'': ')

        if isinstance(data, list): output.write(f'{data}')
        else: output.write(f'[{data}]')
        
        if not isLast: output.write(',\n')

#Naming the object;
object_name = input("Please enter a name for the object: ")

#Formatting the coordinates into hex understandable by the ROM.
for x, y in zip(objectx, objecty):
        decimalHex = int(ConcatHex(x, y))
        objectxy.append(decimalHex)

#Print the extracted data into the object data file;
output = open("objectdata.txt","w+")
output.write(f'"{object_name}": ''{\n')
WriteParameter("id", object, False)
WriteParameter("address", objectaddress, False)
WriteParameter("properties", objectdata, False)
WriteParameter("xy", objectxy, False)
WriteParameter("room", objectroom, True)
output.write("\n	},")

print("Done. Check the 'objectdata.txt' file in folder.")