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

def check_enemyhp(loc):
    enemyhp = 0
    cur = db.cursor()
    sql = "SELECT enemy.Hitpoints FROM enemy INNER JOIN playercharacter ON enemy.RoomID ="+ str(loc)
    cur.execute(sql)
    for row in cur:
        enemyhp = row[0]
    return enemyhp

def check_enemyattack(loc):
    enemydmg = 0
    cur = db.cursor()
    sql = "SELECT enemytype.AttackPower FROM enemytype INNER JOIN enemy ON  enemy.EnemytypeID = enemytype.EnemytypeID WHERE enemy.RoomID ="+str(loc) ;
    cur.execute(sql)
    for row in cur:
        enemydmg = row[0]
    return enemydmg

def check_enemyname(loc):
    enemyname = ""
    cur = db.cursor()
    sql = "SELECT enemytype.name FROM enemytype,enemy,playercharacter WHERE Enemy.RoomID ="+str(loc)+" AND enemytype.EnemytypeID = enemy.EnemytypeID;"
    cur.execute(sql)
    for row in cur:
        enemyname = row[0]
    return enemyname

def check_enemyunique(loc):
    enemyunique = 0
    cur = db.cursor()
    sql = "SELECT enemytype.isUnique FROM enemytype INNER JOIN enemy ON enemy.EnemytypeID = enemytype.EnemytypeID WHERE enemy.RoomID ="+str(loc)
    cur.execute(sql)
    for row in cur:
        enemyunique = row[0]
    return enemyunique

def check_playerhp():
    cur = db.cursor()
    sql = "SELECT playercharacter.HitPoints FROM playercharacter;"
    cur.execute(sql)
    for row in cur:
        playerhp = row[0]
    return playerhp

def check_playerdmg():
    cur = db.cursor()
    sql = "SELECT itemtype.AttackPower FROM itemtype INNER JOIN item ON item.ItemtypeID = itemtype.ItemtypeID WHERE item.ID = 1;"
    cur.execute(sql)
    for row in cur:
        playerdmg = row[0]
    return playerdmg

def delete_deathenemy():
    cur = db.cursor()
    sql = "DELETE FROM enemy WHERE enemy.Hitpoints <= 0;"
    cur.execute(sql)

def fight_enemy(loc):
    playerdmg = 0
    #playerdmg
    cur = db.cursor()
    sql = "SELECT itemtype.AttackPower FROM itemtype INNER JOIN item ON item.ItemtypeID = itemtype.ItemtypeID WHERE item.ID = 1;"
    cur.execute(sql)
    for row in cur:
        playerdmg = row[0]
    enemyname = check_enemyname(loc)
    enemyhp = check_enemyhp(loc)
    enemydmg = check_enemyattack(loc)
    enemyunique = check_enemyunique(loc)
    print("I can use scrolls, light attack, normal attack and hard attack.")
    
    #täytyy lisätä inventory commandit myös tänne koska muuten ei voi taistellussa katsoa inventorya!
    #osioon voi myös lisätä erinlaisia komentoja vielä jos tahtoo laajentaa. esim (examine ei toimi tässä) 
    #tappeluparseri
    while enemyhp > 0:
        print("")
        input_string=input("Attack action? ").split()
        if len(input_string)>=1:
            action = input_string[0].lower()
        else:
            action = ""
        if len(input_string)>=2:
            target = input_string[len(input_string)-1].lower()
        else:
            target = ""
        print("")

        #fighting actions

        #normal attack 
        if action == "normal" and target == "attack":
            if enemyunique == 0:
                print("I hit "+enemyname+" with normal attack.")
                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+" WHERE enemy.RoomID ="+str(loc)
                cur.execute(sql)
                print(enemyhp)
                print(playerdmg)
                enemyhp = check_enemyhp(loc)
                print("I hit enemy with my normal attack it does "+str(playerdmg)+"DMG")
                if enemyhp > 0:
                    sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)
                    cur.execute(sql)
                    playerhp = check_playerhp()
                    print(enemyname+" health is now "+str(enemyhp))
                    print(enemyname+" hits you. You lose "+str(enemydmg)+" health. My health is now "+str(playerhp)+" HP")
                else :
                    print("I killed the enemy")
            elif enemyunique ==1:
                randomattack = random.randint(1,3)
                print(randomattack)
                print("I hit "+enemyname+" with normal attack.")
                if randomattack == 1:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+" WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit "+enemyname+" with my normal attack it does "+str(playerdmg)+"DMG")
                    
                    #IF randomattack = 1 enemy whos unique(boss) hits normal attack
                    if enemyhp > 0:
                        print(enemyname+" uses normal attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+" health is now "+str(enemyhp))
                        print(enemyname+" hits you. You lose "+str(enemydmg)+" health. My health is now "+str(playerhp)+" HP")
                    else:
                        print("I killed the Boss. That was easy.")   
                elif randomattack == 2:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.5 WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit enemy with my normal attack it does "+str(playerdmg*0.5)+"DMG")

                    #If randomattack = 2 enemy who's unique(boss) hits light attack
                    if enemyhp > 0:
                        print(enemyname+" uses light attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.5;"
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+" health is now "+str(enemyhp))
                        print(enemyname+" hits you. You lose "+str(enemydmg*0.5)+" health. My health is now "+str(float(playerhp))+" HP")
                    else :
                        print("I killed the enemy.I killed the Boss. That was easy.")
                elif randomattack == 3:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5 WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit enemy with my normal attack it does "+str(playerdmg*1.5)+"DMG")

                    #IF randomattack = 3 enemy who's unique(boss) hits hevy attack
                    if enemyhp > 0:
                        print(enemyname+" uses hevy attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5"
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+"health is now "+str(enemyhp))
                        print(enemyname+" hits me. I lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
                    else :
                        print("I killed the enemy. I killed the Boss. That was easy.")
                                
                    

        #light attack
        elif action == "light" and target == "attack":

            if enemyunique == 0:
                
                print("I hit "+enemyname+" with light attack.")
                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.5 WHERE enemy.RoomID ="+str(loc)
                cur.execute(sql)
                enemyhp = check_enemyhp(loc)
                print("I hit enemy with my light attack it does "+str(playerdmg*0.5)+"DMG.")

                #vihu lyö
                if enemyhp > 0:
                    sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.5;"
                    cur.execute(sql)
                    playerhp = check_playerhp()
                    print(enemyname+" health is now "+str(enemyhp))
                    print(enemyname+" hits you. You lose "+str(enemydmg*0.5)+" health. My health is now "+str(float(playerhp))+" HP")
                
                else :
                    print("I killed the enemy!")
                    
            elif enemyunique == 1:
                randomattack = random.randint(1,3)
                print(randomattack)
                print("I hit "+enemyname+" with light attack.")
                #enemy normal attack 
                if randomattack == 1:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.5 WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit "+enemyname+" with my light attack it does "+str(playerdmg)+" DMG.")
                    if enemyhp > 0:
                        print(enemyname+" uses normal attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.5"
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+" health is now "+str(enemyhp))
                        print(enemyname+" hits you. You lose "+str(enemydmg*0.5)+" health. My health is now "+str(playerhp)+" HP")
                    else:
                        print("I killed the Boss. That was easy.")
                #enemy light attack
                elif randomattack == 2:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.25 WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit "+enemyname+" with my light attack it does "+str(playerdmg*0.25)+" DMG.")
                    if enemyhp > 0:
                        print(enemyname+" uses light attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.25"
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+" health is now "+str(enemyhp))
                        print(enemyname+" hits you. You lose "+str(enemydmg*0.25)+" health. My health is now "+str(playerhp)+" HP")
                    else:
                        print("I killed the Boss. That was easy.")
                #enemy hevy attack
                elif randomattack == 3:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.75 WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit "+enemyname+" with my light attack it does "+str(playerdmg)+" DMG.")
                    if enemyhp > 0:
                        print(enemyname+" uses hevy attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.75"
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+" health is now "+str(enemyhp))
                        print(enemyname+" hits you. You lose "+str(enemydmg*0.75)+" health. My health is now "+str(playerhp)+" HP")
                    else:
                        print("I killed the Boss. That was easy.")
                    
    
        #hevy attack        
        elif action == "hevy" and target == "attack":

            if enemyunique == 0:
                print("I hit "+enemyname+" with hevy attack.")
                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5 WHERE enemy.RoomID ="+str(loc)
                cur.execute(sql)
                enemyhp = check_enemyhp(loc)
                print("I hit enemy with my hevy attack it does "+str(playerdmg*1.5)+"DMG.")

                #vihu lyö
                if enemyhp > 0:
                    sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5"
                    cur.execute(sql)
                    playerhp = check_playerhp()
                    print(enemyname+"health is now "+str(enemyhp))
                    print(enemyname+" hits me. I lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
                
                else :
                    print("I killed the enemy!")
            elif enemyunique == 1:
                randomattack = random.randint(1,3)
                print(randomattack)
                print("I hit "+enemyname+" with hevy attack.")
                #enemy normal attack 
                if randomattack == 1:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5 WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit "+enemyname+" with my hevy attack it does "+str(playerdmg*1.5)+" DMG.")
                    if enemyhp > 0:
                        print(enemyname+" uses normal attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5"
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+" health is now "+str(enemyhp))
                        print(enemyname+" hits you. You lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
                    else:
                        print("I killed the Boss. That was easy.")
                #enemy light attack
                elif randomattack == 2:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5*0.5 WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit "+enemyname+" with my hevy attack it does "+str(playerdmg*1.5*0.5)+" DMG.")
                    if enemyhp > 0:
                        print(enemyname+" uses light attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5*0.5"
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+"health is now "+str(enemyhp))
                        print(enemyname+" hits me. I lose "+str(enemydmg*1.5*0.5)+" health. My health is now "+str(playerhp)+" HP")
                    else:
                        print("I killed the Boss. That was easy.")
                #enemy hevy attack
                elif randomattack == 3:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5*1.5 WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit "+enemyname+" with my hevy attack it does "+str(playerdmg*1.5*1.5)+" DMG.")
                    if enemyhp > 0:
                        print(enemyname+" uses hevy attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5*1.5"
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+"health is now "+str(enemyhp))
                        print(enemyname+" hits me. I lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
                    else:
                        print("I killed the Boss. That was easy.")

                              
        elif action == "examine" and target == enemyname.lower() or target == "enemy":
            sql = "SELECT enemytype.Description FROM enemytype,enemy,playercharacter WHERE enemy.roomid ="+str(loc)+" AND enemytype.EnemytypeID = enemy.EnemytypeID;"
            cur.execute(sql)
            for row in cur:
                print(row[0])
        
        #scroll magic attack    
        elif action == "use" and target == "scroll" or target == "spell":
            print("I used magic scroll to "+enemyname)
            enemyhp = check_enemyhp()

        #muut commandit eivät käy    
        else:
            print("I don't know what to do !")
            enemyhp = check_enemyhp(loc)

        enemyhp = check_enemyhp(loc)
        
        playerhp = check_playerhp()
    if playerhp == 0:
        print("You died")
        
    return

    
            
#while action!="quit" and (playerhp > 0 or snoopdoglives):

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

    vihuhp = check_enemyhp(loc)
    while  vihuhp > 0:
        fight_enemy(loc)
        vihuhp = check_enemyhp(loc)
        delete_deathenemy()
    
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
