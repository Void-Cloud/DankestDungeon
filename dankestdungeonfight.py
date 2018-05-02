import mysql.connector
import random

def look_around(loc):
    cur = db.cursor()
    sql = "SELECT room.description FROM Room WHERE Roomid =" + str(loc)
    cur.execute(sql)
    for row in cur:
        print(row[0])
    print("-"*80)
    return

def check_enemy(loc):
    enemyhp = 0
    enemyname = ""
    cur = db.cursor()
    sql = "SELECT enemytype.name FROM enemytype,enemy,playercharacter WHERE Enemy.RoomID ="+str(loc)+" AND enemytype.EnemytypeID = enemy.EnemytypeID;"
    cur.execute(sql)
    for row in cur:
        enemyname = row[0]
        print(enemyname +" apears in front of you!")
    sql = "SELECT enemytype.Description FROM enemytype,enemy,playercharacter WHERE enemy.roomid ="+str(loc)+" AND enemytype.EnemytypeID = enemy.EnemytypeID;"
    cur.execute(sql)
    for row in cur:
        print(row[0])
    sql = "SELECT enemy.Hitpoints FROM enemy WHERE enemy.RoomID ="+str(loc)
    cur.execute(sql)
    for row in cur:
        enemyhp = row[0]
    print("-"*80)
    return enemyhp,enemyname

def check_enemyhp():
    cur = db.cursor()
    sql = "SELECT enemy.Hitpoints FROM enemy INNER JOIN playercharacter ON playercharacter.RoomID = enemy.RoomID;"
    cur.execute(sql)
    for row in cur:
        enemyhp = row[0]
    return enemyhp

def check_enemyattack():
    cur = db.cursor()
    sql = "SELECT enemytype.AttackPower FROM enemytype, enemy INNER JOIN playercharacter ON playercharacter.RoomID = enemy.RoomID WHERE enemy.EnemytypeID = enemytype.EnemytypeID;"
    cur.execute(sql)
    for row in cur:
        enemydmg = row[0]
    return enemydmg

def check_enemyunique():
    cur = db.cursor()
    sql = "SELECT enemytype.isUnique FROM enemytype, playercharacter, enemy WHERE playercharacter.RoomID = enemy.RoomID AND enemy.EnemytypeID = enemytype.EnemytypeID;"
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

def fight_enemy():
    playerdmg = 0
    #playerdmg
    cur = db.cursor()
    sql = "SELECT itemtype.AttackPower FROM itemtype INNER JOIN item ON item.ItemtypeID = itemtype.ItemtypeID WHERE item.ID = 1;"
    cur.execute(sql)
    for row in cur:
        playerdmg = row[0]
    enemyhp = check_enemyhp()
    enemydmg = check_enemyattack()
    enemyunique = check_enemyunique()
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
                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+" WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                cur.execute(sql)
                enemyhp = check_enemyhp()
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
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+" WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                    cur.execute(sql)
                    enemyhp = check_enemyhp()
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
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.5 WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                    cur.execute(sql)
                    enemyhp = check_enemyhp()
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
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5 WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                    cur.execute(sql)
                    enemyhp = check_enemyhp()
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
                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.5 WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                cur.execute(sql)
                enemyhp = check_enemyhp()
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
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.5 WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                    cur.execute(sql)
                    enemyhp = check_enemyhp()
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
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.25 WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                    cur.execute(sql)
                    enemyhp = check_enemyhp()
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
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.75 WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                    cur.execute(sql)
                    enemyhp = check_enemyhp()
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
                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5 WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                cur.execute(sql)
                enemyhp = check_enemyhp()
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
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5 WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                    cur.execute(sql)
                    enemyhp = check_enemyhp()
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
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5*0.5 WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                    cur.execute(sql)
                    enemyhp = check_enemyhp()
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
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5*1.5 WHERE enemy.RoomID IN (SELECT playercharacter.RoomID FROM playercharacter);"
                    cur.execute(sql)
                    enemyhp = check_enemyhp()
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
            enemyhp = check_enemyhp()

        enemyhp = check_enemyhp()
        
        playerhp = check_playerhp()
    if playerhp == 0:
        print("You died")
        
    return
            
# Open DB connection
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
cur = db.cursor()
sql = "SELECT HitPoints FROM playercharacter"
cur.execute(sql)
for row in cur.fetchall():
    playermaxhp = row[0]
playerhp = playermaxhp

snoopdgolives = True
action = ""

print(playerhp, snoopdgolives, loc)

#Main
enemytiedot = []
enemyhp = 0
enemyname = ""

while action!="quit" and loc!="EXIT":
    
    enemytiedot.append(check_enemy(loc));
    for tiedot in enemytiedot:
        enemyhp = tiedot[0]
        enemyname = tiedot[1]
    
    while  enemyhp > 0:
        fight_enemy()
        enemyhp = check_enemyhp()
        delete_deathenemy()
        
    print("")
    input_string=input("My action? ").split()
    if len(input_string)>=1:
        action = input_string[0].lower()
    else:
        action = ""
    if len(input_string)>=2:
        target = input_string[len(input_string)-1].lower()
    else:
        target = ""
    #print("Parsed action: " + action)
    #print("Parsed target: " + target)
    print("")

    
    if (action=="look" or action=="examine" or action=="view"):
        if target=="":
            look_around(loc);
    
            
#while action!="quit" and (playerhp > 0 or snoopdoglives):
