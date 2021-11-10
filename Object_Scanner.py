#This script simply reads Amazing Mirror's object table then produces stats about an object.
data = open("objecttable.bin",'rb+')
eof = False
check = "Y"

#Start at byte 0C, where the first item is.
position = 12 #Begin on the first object's ID instead of the start of the file.
roomnumber = 0
readvalue = -1
totalfound = -1
object = int(input("Please enter an object to look up: "))
objectaddress = [ ]
objectdata = [ ]
objectx = [ ]
objecty = [ ]
objectroom = [ ]

while eof == False:
        #First check if we've reached the end of the room.
        if position <= 136871:
                data.seek(position-4)
                readvalue = int.from_bytes(data.read(4),'big')

                #Have we reached the end of the room?
                if readvalue == 4294967295:
                        roomnumber += 1
                        #We're looking for "01 24 00 00", the start of the first object's code.
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
                                #Ladies and gentlemen... we got 'em.
                                totalfound += 1
                                #Add object data to our arrays.
                                objectaddress.append(position + 8932452) # Address - we add 8932452 since that's were the object table in the ROM starts.
                                data.seek(position)
                                objectdata.append(int.from_bytes(data.read(6),'big')) # Object ID / properties.
                                data.seek(position-6)
                                objectx.append(int.from_bytes(data.read(2),'little')) # X.
                                data.seek(position-4)
                                objecty.append(int.from_bytes(data.read(2),'little')) # Y.
                                objectroom.append(roomnumber) # Room number.
                                        
                                output = open("objectdata.txt","a")
                                print("Object " + str(objectdata[-1]) + " found in room " + str(objectroom[-1]) + "! Address: " + str(objectaddress[-1]) + ", X/Y: " + str(objectx[-1]) + ", " + str(objecty[-1]))
                                output.write("Object " + str(objectdata[-1]) + " found in room " + str(objectroom[-1]) + "! Address: " + str(objectaddress[-1]) + ", X/Y: " + str(objectx[-1]) + ", " + str(objecty[-1]))
                                output.write("\n")
                        position += 36
        else:
                eof = True

#Naming the object;
object_name = input("Please enter a name for the object: ")

output = open("objectdata.txt","w+")
output.write('"')
output.write(object_name)
output.write('": {\n')
output.write('		"id": [')
output.write(str(object))
output.write('],\n		"address": ')
output.write(str(objectaddress))
output.write("\n	},")

print("Thanks.")
#Print our arrays so I can make a JSON with them.
"""output.write("\t\"\": {\n\t\t\"data\": "+ str(objectdata) + ",\n")
output.write("\t\t\"address\": " + str(objectaddress) + ",\n")
output.write("\t\t\"xy\": " + str(objectxy) + ",\n")
output.write("\t\t\"room\": " + str(objectroom) + "\n\t},")
"""
