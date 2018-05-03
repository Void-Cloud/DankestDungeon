import mysql.connector
import random

def Dirtransform(dire):
    if dire == "E":
        return "East"
    elif dire == "W":
        return "West"
    elif dire == "N":
        return "North"
    elif dire == "S":
        return "South"
    elif dire == "D":
        return "Down"
    elif dire == "U":
        return "Up"
    else:
        return "Someone dun goofed."

def look_around(loc):
    cur = db.cursor()
    sql = "SELECT Description FROM room WHERE RoomID = "+ str(loc)
    cur.execute(sql)
    for row in cur.fetchall():
        print(row[0]+'\n')
    sql = "SELECT Name FROM itemtype INNER JOIN item ON item.itemtypeID = itemtype.ItemtypeID AND item.RoomID = "+ str(loc)
    cur.execute(sql)
    if cur.rowcount > 0:
        print("I see following items around the room")
    for row in cur.fetchall():
        print("<>", row[0])
    print("")
    sql = "SELECT Direction FROM leads_to WHERE RoomID_1 = "+ str(loc)
    cur.execute(sql)
    print("Exits are to:")
    i = 0;
    for row in cur.fetchall():
        i = i+1
        print(Dirtransform(row[0]), end='')
        if i < cur.rowcount - 1:
            print(",", end=' ')
        elif i == cur.rowcount -1 and cur.rowcount > 1:
            print(" and ", end='')
    print("")
    return

def move(loc, dire):
    destination=loc
    cur = db.cursor()
    sql = "SELECT Leads_toRoomID_2, Locked FROM leads_to WHERE Direction='" + dire + "' AND RoomID_1 = " + str(loc)
    cur.execute(sql)
    if cur.rowcount>=1:
        for row in cur.fetchall():
            if row[1] == 1:
                print("It's locked!")
            else:
                destination = row[0]
        sql = "UPDATE playercharacter SET RoomID = "+str(destination)
    else:
        destination = loc; # movement not possible
    return destination

def check_inventory():
    cur = db.cursor()
    sql = "SELECT Name, Type, Equipped FROM itemtype INNER JOIN item ON item.itemtypeID = itemtype.ItemtypeID AND item.ID = 1"
    cur.execute(sql)
    print("I have the following items in my inventory:")
    for row in cur.fetchall():
        print("#",row[0]+"("+row[1]+")", end='')
        if row[2] == 1:
            print("(Equipped)")
    return

def take_item(item, loc):
    cur = db.cursor()
    sql = "SELECT Name, Movable FROM itemtype INNER JOIN item ON item.itemtypeID = itemtype.ItemtypeID AND item.RoomID ="+str(loc)+" AND itemtype.Name = '"+item+"'"
    cur.execute(sql)
    for row in cur.fetchall():
        if row[1] == 1:
            sql = "UPDATE item, itemtype SET RoomID = NULL, ID = 1 WHERE item.itemtypeID = itemtype.ItemtypeID AND itemtype.Name = '"+item+"'"
            cur.execute(sql)
        else:
            print("I can't move that")
        return
    print("There is no such item here.")
    return

def check_items(name):
    cur = db.cursor()
    sql = "SELECT Name FROM itemtype WHERE Name = '"+name+"'"
    cur.execute(sql)
    if cur.rowcount == 1:
        return True
    else:
        return False

def item_desc(item, loc):
    cur = db.cursor()
    sql = "SELECT Name, Description FROM itemtype INNER JOIN item ON item.itemtypeID = itemtype.ItemtypeID AND (item.RoomID ="+str(loc)+" OR item.ID = 1) AND itemtype.Name = '"+item+"'"
    cur.execute(sql)
    if cur.rowcount == 0:
        print("There is no such item here.")
    else:
        for row in cur.fetchall():
            print(row[0] + '\n' + row[1])
    return

def me_desc():
    cur = db.cursor()
    sql = "SELECT Description FROM playercharacter WHERE ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        print(row[0])
    return

#Database connection
db = mysql.connector.connect(host="localhost",
                      user="dbuser",
                      passwd="dbpass",
                      db="dankestdungeon",
                      buffered=True)

#Find player start position
cur = db.cursor()
sql = "SELECT RoomID FROM playercharacter"
cur.execute(sql)
for row in cur.fetchall():
    loc = row[0]

#Fetch player max health
sql = "SELECT HitPoints FROM playercharacter"
cur.execute(sql)
for row in cur.fetchall():
    playermaxhp = row[0]
playerhp = playermaxhp

snoopdoglives = True
action = ""

look_around(loc)

#Main Loop
while action!="quit" and (playerhp > 0 or snoopdoglives):
    print("")
    input_string=input("Your action? ").split()
    if len(input_string)>=1:
        action = input_string[0].lower()
    else:
        action = ""
    if len(input_string)==2:
        target = input_string[len(input_string)-1].lower()
    elif len(input_string) >= 3:
        check = input_string[len(input_string)-2].lower() + " " + input_string[len(input_string)-1].lower()
        if check_items(check):
            target = check
        else:
            target = input_string[len(input_string)-1].lower()
    else:
        target = ""
        
    #print("Parsed action: " + action)
    #print("Parsed target: " + target)

    #Look
    if action == "look" or action == "examine":
        if target == "":
            look_around(loc)
        elif check_items(target):
            item_desc(target, loc)
        elif target == "me" or target == "myself":
            me_desc()

    #Moving
    elif action=="e" or action=="w" or action=="n" or action=="s" or action=="d" or action=="u" or action=="east" or action=="west" or action=="north" or action=="south" or action=="down" or action=="up":
        action = action[0]
        newloc = move(loc, action)
        if newloc == loc:
            print("I can't move there")
        else:
            loc = newloc
            look_around(loc)

    elif action=="i" or action == "inventory":
        check_inventory()

    elif action == "take" or action == "pick" and check_items(target):
        take_item(target, loc)
        
    #Easter egg commands :3
    elif action == "breath":
        print("I know how to breath without help, thank you")

    else:
        print("I don't know how to "+action+".")
if not snoopdoglives:
    print("congratz you is winner")
else:
    print("The secrets of the dankest dungeon shall forever stay in the shadows")
