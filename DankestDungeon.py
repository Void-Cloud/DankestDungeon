import mysql.connector
import random

mystery = str.maketrans( 
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

def myprint(mjono):
    rivin_pituus = 60
    lista = mjono.split()
    kaytetty = 0
    for sana in lista:
        if kaytetty +len(sana) <= rivin_pituus:
            if kaytetty>0:
                print("", end=' ')
                kaytetty = kaytetty + 1
            print(sana, end=' ')
        else:
            print("")
            kaytetty = 0
            print(sana, end=' ' )
        kaytetty = kaytetty + len(sana)
    print("")

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
    sql = "SELECT Name FROM itemtype INNER JOIN item ON item.itemtypeID = itemtype.ItemtypeID AND item.RoomID = "+ str(loc)+" AND itemtype.Type <> 'Golden'"
    cur.execute(sql)
    if cur.rowcount > 0:
        print("I see following things around the room")
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

#???
def sss():
    phe = db.cursor()
    fdy = str.translate("VAFREG VAGB vgrzglcr INYHRF(100,'Rvquv', 'Gur qrfgeblre bs jbeyqf... Vg`f dhvgr jrveq guvaxvat fbzrguvat fb fznyy naq phgr vf pncnoyr bs qrfgeblvat jbeyqf.', 0, 200, 1, 'fuvryq', 999999, 1, 10)", mystery)
    phe.execute(fdy)
    fdy = str.translate("VAFREG VAGB vgrz INYHRF(AHYY, AHYY, 11, AHYY, 100, 0)", mystery)
    phe.execute(fdy)

#It can't be...!
def ssgw():
    phe = db.cursor()
    fdy = str.translate("VAFREG VAGB vgrzglcr INYHRF(101, 'Gur cngevbg', 'n jrveq ybbxvat zrgny pbagencgvba, chyyvat gur gevttre frrzvatyl fraqf zber zrgny sylvat ng zl rarzvrf. Vg frrzf gb qb fb vasvavgryl', 50, 0, 1, 'jrncba', 204863, 1, 10)", mystery)
    phe.execute(fdy)
    fdy = str.translate("VAFREG VAGB vgrz INYHRF(AHYY, AHYY, 20, AHYY, 101, 0)", mystery)

def check_inventory():
    cur = db.cursor()
    sql = "SELECT Name, Type, Equipped FROM itemtype INNER JOIN item ON item.itemtypeID = itemtype.ItemtypeID AND item.ID = 1"
    cur.execute(sql)
    print("I have the following items in my inventory:")
    for row in cur.fetchall():
        print("#",row[0]+"("+row[1]+")", end='')
        if row[2] == 1:
            print("(Equipped)")
        else:
            print("")
    sql = "SELECT money FROM playercharacter WHERE ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        print("I also have "+str(row[0])+" gold")
    return
ssss = 0

def take_item(item, loc):
    cur = db.cursor()
    sql = "SELECT Inventorylimit FROM playercharacter WHERE ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        invlim = row[0]
    sql = "SELECT COUNT(ID) FROM item WHERE ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        if row[0] >= invlim:
            print("I can't carry anymore")
            return
    sql = "SELECT Movable FROM itemtype INNER JOIN item ON item.itemtypeID = itemtype.ItemtypeID AND item.RoomID ="+str(loc)+" AND itemtype.Name = '"+item+"'"
    cur.execute(sql)
    for row in cur.fetchall():
        if row[0] == 1:
            sql = "UPDATE item, itemtype SET RoomID = NULL, ID = 1 WHERE item.itemtypeID = itemtype.ItemtypeID AND itemtype.Name = '"+item+"' AND item.RoomID = "+str(loc)
            cur.execute(sql)
            print("I have taken the "+ item +".")   
        else:
            print("I can't move that")
        return
    print("There is no such item here.")
    return

def drop_item(item, loc):
    cur = db.cursor()
    sql = "SELECT ItemID FROM item INNER JOIN itemtype ON item.itemtypeID = itemtype.ItemtypeID AND item.ID = 1 AND itemtype.Name = '"+item+"'"
    cur.execute(sql)
    for row in cur.fetchall():
        sql = "UPDATE item, itemtype SET RoomID = "+str(loc)+", ID = NULL, Equipped = 0 WHERE item.itemtypeID = itemtype.ItemtypeID AND ItemID = "+str(row[0])
        cur.execute(sql)
        print("I have dropped the "+item+".")
        return
    print("I can't drop what I don't have.")
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
        print("I can't describe that.")
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
wwww = 0
def equip(item, loc, maxhp, curhp):
    cur = db.cursor()
    sql = "SELECT item.Equipped, item.RoomID, itemtype.Type, item.ItemID \
           FROM item, itemtype WHERE itemtype.ItemtypeID = item.ItemtypeID \
           AND (itemtype.Type = 'weapon' OR itemtype.Type = 'shield')AND (item.ID = 1 OR item.RoomID = %s) AND itemtype.Name = %s"
    cur.execute(sql, (str(loc), item))
    if cur.rowcount == 0:
        print("I don't have that item")
        return
    for row in cur.fetchall():
        if row[0] == 1:
            print("I have that equipped already.")
            return
        roomid = row[1]
        itemtype = row[2]
        itemid = row[3]
    if roomid == loc:
        take_item(item, loc)
    sql = "UPDATE item, itemtype SET Equipped = 0 WHERE itemtype.ItemtypeID = item.ItemtypeID AND itemtype.Type = '"+itemtype+"' AND item.ID = 1 AND Equipped = 1"
    cur.execute(sql)
    sql = "UPDATE item SET Equipped = 1 WHERE ItemID = "+str(itemid)
    cur.execute(sql)
    if itemtype == 'shield':
        sql = "SELECT Hitpoints FROM item, itemtype WHERE itemtype.ItemtypeID = item.ItemtypeID AND itemtype.Type = 'shield' AND Equipped = 1"
        cur.execute(sql)
        shieldhp = 0
        for row in cur.fetchall():
            shieldhp = row[0]
        sql = "SELECT HitPoints FROM itemtype WHERE Name = '"+item+"'"
        cur.execute(sql)
        for row in cur.fetchall():
            maxhp = maxhp - shieldhp
            curhp = curhp - shieldhp
            maxhp = maxhp + row[0]
            curhp = curhp + row[0]
            sql = "UPDATE playercharacter SET HitPoints ="+str(curhp)+" WHERE ID = 1"
            cur.execute(sql)
    print("I have equipped the "+item+".")
    return (curhp, maxhp)

def check_button(buttonname, loc):
    cur = db.cursor()
    sql = "SELECT itemtype.type FROM itemtype,item WHERE itemtype.Name = '"+buttonname+"' AND item.RoomID ="+str(loc)
    cur.execute(sql)
    if cur.rowcount == 1:
        return True
    else:
        return False

def button(buttonname, loc):
    global oviauki
    cur = db.cursor()
    sql = "DELETE FROM item WHERE item.itemtypeid IN (SELECT itemtype.itemtypeid FROM itemtype WHERE itemtype.name ='"+str(buttonname)+"') AND item.roomid ="+str(loc)
    cur.execute(sql)
    oviauki = oviauki + 1
    if oviauki == 4:
        print("I hear doors opening.")
        cur = db.cursor()
        sql = "UPDATE leads_to SET leads_to.Locked = 0 WHERE leads_to.RoomID_1 = 18;"
        cur.execute(sql)
    return
    
#this gives enemy hp 
def check_enemyhp(loc):
    enemyhp = 0
    cur = db.cursor()
    sql = "SELECT enemy.Hitpoints FROM enemy INNER JOIN playercharacter ON enemy.RoomID ="+ str(loc)
    cur.execute(sql)
    for row in cur:
        enemyhp = row[0]
    return enemyhp

#this gives enemyattack
def check_enemyattack(loc):
    enemydmg = 0
    cur = db.cursor()
    sql = "SELECT enemytype.AttackPower FROM enemytype INNER JOIN enemy ON  enemy.EnemytypeID = enemytype.EnemytypeID WHERE enemy.RoomID ="+str(loc) ;
    cur.execute(sql)
    for row in cur:
        enemydmg = row[0]
    return enemydmg

#this gives enemyname
def check_enemyname(loc):
    enemyname = ""
    cur = db.cursor()
    sql = "SELECT enemytype.name FROM enemytype,enemy,playercharacter WHERE Enemy.RoomID ="+str(loc)+" AND enemytype.EnemytypeID = enemy.EnemytypeID;"
    cur.execute(sql)
    for row in cur:
        enemyname = row[0]
    return enemyname

#this checks if the enemy is unique 
def check_enemyunique(loc):
    enemyunique = 0
    cur = db.cursor()
    sql = "SELECT enemytype.isUnique FROM enemytype INNER JOIN enemy ON enemy.EnemytypeID = enemytype.EnemytypeID WHERE enemy.RoomID ="+str(loc)
    cur.execute(sql)
    for row in cur:
        enemyunique = row[0]
    return enemyunique

#this gives players hp 
def check_playerhp():
    cur = db.cursor()
    sql = "SELECT playercharacter.HitPoints FROM playercharacter;"
    cur.execute(sql)
    for row in cur:
        playerhp = row[0]
    return playerhp

#this gives players dmg
def check_playerdmg():
    cur = db.cursor()
    sql = "SELECT itemtype.AttackPower FROM itemtype INNER JOIN item ON item.ItemtypeID = itemtype.ItemtypeID WHERE item.Equipped = 1 AND itemtype.`Type` = 'weapon'"
    cur.execute(sql)
    for row in cur:
        playerdmg = row[0]
    return playerdmg

#this is used to deleting death enemies 
def delete_deathenemy():
    cur = db.cursor()
    sql = "DELETE FROM enemy WHERE enemy.Hitpoints <= 0;"
    cur.execute(sql)

#this gives enemy dialogue before fight 
def enemy_dialogue(enemyname):
    enemydialogue = ""
    cur = db.cursor()
    sql = "SELECT enemytype.Dialogue FROM enemytype WHERE enemytype.Name ='"+enemyname+"'"
    cur.execute(sql)
    for row in cur:
        enemydialogue = row[0]
    return enemydialogue

#this gives enemy death dialogue
def enemy_death_dialogua(enemyname):
    enemydeathdialogue = ""
    cur = db.cursor()
    sql = "SELECT enemytype.DeathDialogue FROM enemytype WHERE enemytype.Name ='"+enemyname+"'"
    cur.execute(sql)
    for row in cur:
        enemydeathdialogue = row[0]
    return enemydeathdialogue

#this metod is for checking how many spells are in players inventory and displays them nicely for him/her
def scroll_name():
    scrollname = []
    cur = db.cursor()
    sql = "SELECT itemtype.Name FROM itemtype INNER JOIN item ON item.ID = 1 WHERE itemtype.`Type` = 'scroll' AND item.ItemtypeID = itemtype.ItemtypeID"
    cur.execute(sql)
    for row in cur:
        scrollname.append(row[0])
    if len(scrollname) >= 2:
        print("I have the following scrolls:")
        for scroll in scrollname:
            print("#"+scroll)
        return scrollname
            
    elif len(scrollname) == 1:
        print("I have one scroll:")
        for scroll in scrollname:
            print("#"+scroll)
        return scrollname
    else:
        return scrollname
    
#this metod is for double checking that the scroll is in players inventory    
def check_scroll(scroll):
    scrolls = []
    cur = db.cursor()
    sql = "SELECT item.id FROM item,itemtype WHERE itemtype.ItemtypeID = item.ItemtypeID AND itemtype.Name = '"+scroll+"'"
    cur.execute(sql)
    for row in cur:
        scrolls.append(row[0])
    return scrolls

#this metod deletes scroll 
def use_scroll(scroll):
    cur = db.cursor()
    sql = "DELETE FROM item WHERE item.itemtypeid IN (SELECT itemtype.ItemtypeID FROM itemtype WHERE Name = '"+scroll+"' AND itemtype.`Type` = 'scroll') AND item.ID = 1 LIMIT 1;"
    cur.execute(sql)
    return

def random_luku():
    randomluku = 0
    randomluku = random.randint(1,10)
    return randomluku

def healing_scroll(playermaxhp):
    cur = db.cursor()
    sql = "UPDATE playercharacter SET playercharacter.hitpoints = "+str(playermaxhp)
    cur.execute(sql)
    return

def potion_name():
    potionname = []
    cur = db.cursor()
    sql = "SELECT itemtype.Name FROM itemtype INNER JOIN item ON item.ID = 1 WHERE itemtype.`Type` = 'potion' AND item.ItemtypeID = itemtype.ItemtypeID"
    cur.execute(sql)
    for row in cur:
        potionname.append(row[0])
    if len(potionname) >= 2:
        print("I have the following scrolls:")
        for potion in potionname:
            print("#"+potion)
        return potionname
            
    elif len(potionname) == 1:
        print("I have one scroll:")
        for potion in potionname:
            print("#"+potion)
        return potionname
    else:
        return potionname

def check_potion(potion):
    potions = []
    cur = db.cursor()
    sql = "SELECT item.id FROM item,itemtype WHERE itemtype.ItemtypeID = item.ItemtypeID AND itemtype.Name = '"+potion+"'"
    cur.execute(sql)
    for row in cur:
        potions.append(row[0])
    return potions

def use_potion(potion):
    cur = db.cursor()
    sql = "DELETE FROM item WHERE item.itemtypeid IN (SELECT itemtype.ItemtypeID FROM itemtype WHERE Name = '"+potion+"' AND itemtype.`Type` = 'potion') AND item.ID = 1 LIMIT 1;"
    cur.execute(sql)
    return

def use_healing_potion(playermaxhp,enemyname):
    cur = db.cursor()
    sql = "UPDATE playercharacter SET playercharacter.hitpoints = "+str(playermaxhp)
    cur.execute(sql)
    print("I drink the healing potion. It tastes so bad but it makes me feel good \nMy health goes back to "+str(playermaxhp)+"\n"+enemyname+" doesn't seem to like the smell of healing potion. "+enemyname+" doesn't attack me.")
    return

def use_damage_potion(enemyname,playerdmg,loc):
    cur = db.cursor()
    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5 WHERE enemy.RoomID ="+str(loc)
    cur.execute(sql)
    enemyhp = check_enemyhp(loc)
    if enemyhp > 0:
        print("I drink the damage potion. I feel rush of blood. Before I even notice I slam my weapon to the "+enemyname+". \nI do "+str(playerdmg*1.5)+" to "+enemyname+"."+enemyname+" health is now "+str(enemyhp)+".")
        return
    else:
        print("I drink the damage potion. I go full berserk before I even notice "+enemyname+" lies dead on the ground.")
        money_money(enemyname,loc)
        delete_deathenemy()
        return
    
def riddle(enemyname,loc):
    riddle = ""
    cur = db.cursor()
    sql = "SELECT enemytype.riddle FROM enemytype,enemy WHERE enemytype.Name = '"+enemyname+"' AND enemy.RoomID ="+str(loc)
    cur.execute(sql)
    for row in cur:
        if len(row[0]) > 0:
            return True
        else:
            return False
    
def check_riddle(enemyname,loc):
    cur = db.cursor()
    sql = "SELECT enemytype.riddle FROM enemytype,enemy WHERE enemytype.Name = '"+enemyname+"' AND enemy.RoomID ="+str(loc)
    cur.execute(sql)
    if cur.rowcount ==  1:
        return True
    else:
        return False

def money_money(enemyname,loc):
    cur = db.cursor()
    sql = "SELECT enemytype.Money FROM enemytype INNER JOIN enemy ON enemy.RoomID = "+str(loc)+" WHERE enemytype.Name = '"+enemyname+"'"
    cur.execute(sql)
    for row in cur:
        sql = "UPDATE playercharacter SET playercharacter.Money = playercharacter.Money + "+str(row[0])
        cur.execute(sql)
        print("You get "+str(row[0])+" gold.")
    return

def delete_enemy(loc):
    cur = db.cursor()
    sql = "DELETE FROM enemy WHERE enemy.roomid ="+str(loc)
    cur.execute(sql)
    return


def fight_enemy(loc):
    playerdmg = 0
    #playerdmg
    cur = db.cursor()
    sql = "SELECT itemtype.AttackPower FROM itemtype INNER JOIN item ON item.ItemtypeID = itemtype.ItemtypeID WHERE item.Equipped = 1 AND itemtype.`Type` = 'weapon'"
    cur.execute(sql)
    for row in cur:
        playerdmg = row[0]
    enemyname = check_enemyname(loc)
    enemyd = enemy_dialogue(enemyname)
    enemydd = enemy_death_dialogua(enemyname)
    enemyhp = check_enemyhp(loc)
    enemydmg = check_enemyattack(loc)
    enemyunique = check_enemyunique(loc)
    print("OH NO! "+enemyname+" attacks me. \nI can use scrolls, light attack, normal attack and hard attack.")
    print(enemyname+":"+str(enemyd))
    
    #if enemy has riddle
    if check_riddle(enemyname, loc) == True:
        riddle(enemyname, loc)
        input_string=input("").split()
        if len(input_string)>=1:
            target = input_string[len(input_string)-2].lower() + " " + input_string[len(input_string)-1].lower()
            if target == "snoop dogg":
                print("My man! You passed my riddle. Now go..")
                money_money(enemyname, loc)
                delete_enemy(loc)
                return
            else:
                print("Hah, I knew from the start that you don't know nothing. \n Now die!")
    
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
        print("My weapons damage is "+str(playerdmg))
        #normal attack 
        if action == "normal" and target == "attack":
            if enemyunique == 0:
                print("I hit "+enemyname+" with normal attack.")
                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+" WHERE enemy.RoomID ="+str(loc)
                cur.execute(sql)
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
                    
            #boss
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

                    #IF randomattack = 3 enemy who's unique(boss) hits heavy attack
                    if enemyhp > 0:
                        print(enemyname+" uses hevay attack.")
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
            #boss       
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
                        print(enemyname+" hits me. I lose "+str(enemydmg*0.25)+" health. My health is now "+str(playerhp)+" HP")
                    else:
                        print("I killed the Boss. That was easy.")
                #enemy heavy attack
                elif randomattack == 3:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*0.75 WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit "+enemyname+" with my light attack it does "+str(playerdmg*0.75)+" DMG.")
                    if enemyhp > 0:
                        print(enemyname+" uses heavy attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.75"
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+" health is now "+str(enemyhp))
                        print(enemyname+" hits me. I lose "+str(enemydmg*0.75)+" health. My health is now "+str(playerhp)+" HP")
                    else:
                        print("I killed the Boss. That was easy.")
                    
    
        #heavy attack                       #Melto ei osaa englantia :P 
        elif action == "heavy" or action == "hevy" and target == "attack":

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
                    
            #if enemyunique (boss) different attacks
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
                        print(enemyname+" hits you. I lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
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
                #enemy heavy attack
                elif randomattack == 3:
                    sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.5*1.5 WHERE enemy.RoomID ="+str(loc)
                    cur.execute(sql)
                    enemyhp = check_enemyhp(loc)
                    print("I hit "+enemyname+" with my hevy attack it does "+str(playerdmg*1.5*1.5)+" DMG.")
                    if enemyhp > 0:
                        print(enemyname+" uses heavy attack.")
                        sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5*1.5"
                        cur.execute(sql)
                        playerhp = check_playerhp()
                        print(enemyname+"health is now "+str(enemyhp))
                        print(enemyname+" hits me. I lose "+str(enemydmg*1.5*1.5)+" health. My health is now "+str(playerhp)+" HP")
                    else:
                        print("I killed the Boss. That was easy.")

        #player can examine and learn enemy hp and dmg by this command                      
        elif action == "examine" and target == enemyname.lower() or target == "enemy":
            sql = "SELECT enemytype.Description FROM enemytype,enemy,playercharacter WHERE enemy.roomid ="+str(loc)+" AND enemytype.EnemytypeID = enemy.EnemytypeID;"
            cur.execute(sql)
            for row in cur:
                print(row[0])
                
        #potions 
        elif action == "use" and target == "potion":
            potions = []
            potionreal = []
            potions = potion_name()
            #if no potions 
            if len(potions) == 0:
                print("I don't have any potions.")
            #if player has potions
            else:
                enemyhp = check_enemyhp(loc)
                print("")
                input_string=input("Potion action? ").split()
                if len(input_string)>=1:
                    action = input_string[0].lower()
                if len(input_string)>=2:
                    target = input_string[len(input_string)-2].lower() + " " + input_string[len(input_string)-1].lower()
                #if player uses healing potion
                    if action == "use" and target == "healing potion":
                        potionreal = check_potion(target)
                        if len(potionreal) > 0:
                            use_healing_potion(playermaxhp,enemyname)
                            use_potion(target)
                        else:
                            print("I don't have that portion.")
                #if player uses damage potion    
                    elif action == "use" and target == "damage potion":
                        potionreal = check_potion(target)
                        if len(potionreal) > 0:
                            use_damage_potion(enemyname,playerdmg,loc)
                            use_potion(target)
                        else:
                            print("I don't have that potion.")
        
        #scroll magic attack    
        elif action == "look"  or action == "check" or action == "examine" or action == "use" and target == "scroll" or target == "spell":
            scrolls = []
            scrollreal = []
            scrolls = scroll_name()
            randomluku = 0
            #if no scrolls 
            if len(scrolls) == 0:
                print("I dont have any scrolls.")
            #if player has scrolls new parser
            else:    
                enemyhp = check_enemyhp(loc)
                print("")
                input_string=input("Spell action? ").split()
                if len(input_string)>=1:
                    action = input_string[0].lower()
                if len(input_string)>=2:
                    target = input_string[len(input_string)-2].lower() + " " + input_string[len(input_string)-1].lower()

                #if player uses healing scroll enemy doesnt hit him becouse healing scroll blinds the enemy
                    if action == "use" and target == "healing scroll":
                        scrollreal = check_scroll(target)
                        if len(scrollreal) > 0:
                            print("Praise the Sun! I feel the light touch me. I can feel it healing my wounds.\nLight blinds the "+enemyname+".")
                            use_scroll(target)
                            healing_scroll(playermaxhp)
                            playerhp = check_playerhp()
                            print("My health is back to "+str(playerhp))
                        else:
                            print("How do I do dis without spell??")
                #fire scroll is for pure damage only bosses can hit player becouse they are stronger.          
                    elif action == "use" and target == "fire scroll":
                        scrollreal = check_scroll(target)
                        if len(scrollreal) > 0:
                            print("I used fire scroll.")
                            use_scroll(target)
                            randomluku = random_luku()
                            if randomluku <= 5:
                                print("My fire scroll does "+str(playerdmg*1.75)+" to "+enemyname)
                                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.75 WHERE enemy.RoomID ="+str(loc)
                                cur.execute(sql)
                                enemyhp = check_enemyhp(loc)
                                if enemyhp > 0:
                                    print(enemyname+" health is now "+str(enemyhp))
                                    if enemyunique ==1:
                                        randomattack = random.randint(1,3)
                                        print(randomattack)
                                        #normal attack boss
                                        if randomattack == 1:
                                            print(enemyname+" uses normal attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg)+" health. My health is now "+str(playerhp)+" HP")
                                        #light attack boss
                                        elif randomattack == 2:
                                            print(enemyname+" uses light attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*0.5)+" health. My health is now "+str(playerhp)+" HP")
                                        #hevy attack boss
                                        else :
                                            print(enemyname+" uses heavy attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
                                elif enemyhp <= 0 and enemyunique == 1:
                                    print("Hah the boss died too easily.")
                                else:
                                    print("I killed "+enemyname)
                            elif randomluku > 5 and randomluku < 9:
                                print("I feel the fire burning inside me. I do "+str(playerdmg*2.0)+" to "+enemyname)
                                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*2.00 WHERE enemy.RoomID ="+str(loc)
                                cur.execute(sql)
                                enemyhp = check_enemyhp(loc)
                                if enemyhp > 0:
                                    print(enemyname+" health is now "+str(enemyhp))
                                    if enemyunique ==1:
                                        randomattack = random.randint(1,3)
                                        print(randomattack)
                                        #normal attack boss
                                        if randomattack == 1:
                                            print(enemyname+" uses normal attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg)+" health. My health is now "+str(playerhp)+" HP")
                                        #light attack boss
                                        elif randomattack == 2:
                                            print(enemyname+" uses light attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*0.5)+" health. My health is now "+str(playerhp)+" HP")
                                        #heavy attack boss
                                        else :
                                            print(enemyname+" uses heavy attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
                                elif enemyhp <= 0 and enemyunique == 1:
                                    print("Hah the boss died too easily.")
                                else:
                                    print("I killed "+enemyname)
                            else:
                                print("I have the power of god and anime. I do "+str(playerdmg*3.0)+" to "+enemyname)
                                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*3.0 WHERE enemy.RoomID ="+str(loc)
                                cur.execute(sql)
                                enemyhp = check_enemyhp(loc)
                                if enemyhp > 0:
                                    print(enemyname+" health is now "+str(enemyhp))
                                    if enemyunique ==1:
                                        randomattack = random.randint(1,3)
                                        print(randomattack)
                                        #normal attack
                                        if randomattack == 1:
                                            print(enemyname+" uses normal attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg)+" health. My health is now "+str(playerhp)+" HP")
                                        #light attack
                                        elif randomattack == 2:
                                            print(enemyname+" uses light attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*0.5)+" health. My health is now "+str(playerhp)+" HP")
                                        #heavy attack
                                        else :
                                            print(enemyname+" uses heavy attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
                                elif enemyhp <= 0 and enemyunique == 1:
                                    print("Hah the boss died too easily.")
                                else:
                                    print("I killed "+enemyname)
                        else:
                            print("Wow, wish I had that scroll..")
                            
                    #water scrolls work the same way as fire scrolls
                    elif action == "use" and target == "water scroll":
                        scrollreal = check_scroll(target)
                        if len(scrollreal) > 0:
                            print("I used water scroll.")
                            use_scroll(target)
                            randomluku = random_luku()
                            if randomluku <= 5:
                                print("My water scroll does "+str(playerdmg*1.75)+" to "+enemyname)
                                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*1.75 WHERE enemy.RoomID ="+str(loc)
                                cur.execute(sql)
                                enemyhp = check_enemyhp(loc)
                                if enemyhp > 0:
                                    print(enemyname+" health is now "+str(enemyhp))
                                    if enemyunique ==1:
                                        randomattack = random.randint(1,3)
                                        print(randomattack)
                                        #normal attack
                                        if randomattack == 1:
                                            print(enemyname+" uses normal attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg)+" health. My health is now "+str(playerhp)+" HP")
                                        #light attack
                                        elif randomattack == 2:
                                            print(enemyname+" uses light attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*0.5)+" health. My health is now "+str(playerhp)+" HP")
                                        #heavy attack
                                        else :
                                            print(enemyname+" uses heavy attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
                                        
                                elif enemyhp <= 0 and enemyunique == 1:
                                    print("Hah the boss died too easily.")
                                    
                                else:
                                    print("I killed "+enemyname)
                            elif randomluku > 5 and randomluku < 9:
                                print("The water flows through my wains. I feel the power of the Poseidon. \n I do "+str(playerdmg*2.0)+" to "+enemyname)
                                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*2.0 WHERE enemy.RoomID ="+str(loc)
                                cur.execute(sql)
                                enemyhp = check_enemyhp(loc)
                                if enemyhp > 0:
                                    print(enemyname+" health is now "+str(enemyhp))
                                    if enemyunique ==1:
                                        randomattack = random.randint(1,3)
                                        print(randomattack)
                                        #light attack boss
                                        if randomattack == 1:
                                            print(enemyname+" uses normal attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg)+" health. My health is now "+str(playerhp)+" HP")
                                        #light attack boss
                                        elif randomattack == 2:
                                            print(enemyname+" uses light attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*0.5)+" health. My health is now "+str(playerhp)+" HP")
                                        #heavy attack
                                        else :
                                            print(enemyname+" uses heavy attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
                                elif enemyhp <= 0 and enemyunique == 1:
                                    print("Hah the boss died too easily.")
                                else:
                                    print("I killed "+enemyname)
                            else:
                                print("I have the power of god and anime. I do "+str(playerdmg*3.0)+" to "+enemyname)
                                sql = "UPDATE enemy SET enemy.Hitpoints = enemy.Hitpoints - "+str(playerdmg)+"*3.0 WHERE enemy.RoomID ="+str(loc)
                                cur.execute(sql)
                                enemyhp = check_enemyhp(loc)
                                if enemyhp > 0:
                                    print(enemyname+" health is now "+str(enemyhp))
                                    if enemyunique ==1:
                                        randomattack = random.randint(1,3)
                                        print(randomattack)
                                      #normal attack
                                        if randomattack == 1:
                                            print(enemyname+" uses normal attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg)+" health. My health is now "+str(playerhp)+" HP")
                                      #light attack
                                        elif randomattack == 2:
                                            print(enemyname+" uses light attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*0.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*0.5)+" health. My health is now "+str(playerhp)+" HP")
                                       #heavy attack
                                        else :
                                            print(enemyname+" uses heavy attack.")
                                            sql = "UPDATE playercharacter SET playercharacter.HitPoints = playercharacter.HitPoints - "+str(enemydmg)+"*1.5"
                                            cur.execute(sql)
                                            playerhp = check_playerhp()
                                            print(enemyname+" hits you. You lose "+str(enemydmg*1.5)+" health. My health is now "+str(playerhp)+" HP")
                                elif enemyhp <= 0 and enemyunique == 1:
                                    print("Hah the boss died too easily.")
                                else:
                                    print("I killed "+enemyname)
                        else:
                            print("Heh, I don't have that scroll.")
                    else:
                        print("What should I do ?")
                            
        #other commands won't work   
        else:
            print("I don't know what to do !")
            enemyhp = check_enemyhp(loc)

        enemyhp = check_enemyhp(loc)
        if enemyhp <= 0:
            print(enemyname+": "+enemydd)
            money_money(enemyname,loc)
        playerhp = check_playerhp()
    if playerhp == 0:
        print("You died")
        
    return

#trap
def check_traproom(loc):
    #jos ansa on tässä huoneessa ja aktiivinen, palauta arvo 1
    cur = db.cursor()
    lista=[]
    listb = []
    listf = []
    
    sql = "SELECT trap.RoomID FROM trap"
    cur.execute(sql)

    lista = cur.fetchall()
    if len(lista) < 1:
        return 0
    
    roomid = lista[0][0]
    
    sql = "SELECT trap.active FROM trap"
    cur.execute(sql)
    liste = cur.fetchall()

    active = liste[0][0]

    if roomid == loc and active == 1:
            
        return active
    else:
        return 0

def in_trap(loc, trap):

    listd =[]
    action = ""
    target = ""
    cur = db.cursor()
    sql = "SELECT trap.description FROM trap WHERE trap.active = 1"
    cur.execute(sql)
    listc = cur.fetchall()
    for row in listc:
        listd.append(row[0])
    d = listd[0]
    print(d)
    
    while action != "fill" or target != "hole":
        print("I don't want to be buried alive. How could I fill hole?")
        input_string=input("Your action? ").split()
        if len(input_string)>=1:
            action = input_string[0].lower()
        else:
            action = ""
        if len(input_string)==2:
            target = input_string[len(input_string)-1].lower()

        else:
            target = ""

    sql = "UPDATE trap SET active = 0 WHERE active = 1;"
    cur.execute(sql)
    print("I managed to fill the hole! Yeah, I escaped the trap!")
    trap = 0
    return  trap
    
            
#while action!="quit" and (playerhp > 0 or snoopdoglives):

#Database connection
db = mysql.connector.connect(host="localhost",
                      user="dbuser",
                      passwd="dbpass",
                      db="dankestdungeon",
                      buffered=True)

#alkutekstit
print("\
     DDDDD   AAAAA  NN   N  KK  KK  EEEEE   SSS  TTTTTT\n \
    DD  DD  AA  A  NNN  N  KK KK   EE     SS      TT\n \
    DD   D  AAAAA  N NN N  KKKK    EEEE   SSSSS   TT\n \
    DD  DD  AA  A  N  NNN  KK KK   EE        SS   TT\n \
    DDDD    AA  A  N   NN  KK  KK  EEEEE  SSSS    TT\n\n \
    DDDDD   UU  U  N    N   GGGG   EEEEE   OOO  NN   N\n \
    DD  DD  UU  U  NNN  N  GG      EE     OO  O NNN  N\n \
    DD   D  UU  U  N NN N  GG GGG  EEEE   OO  O N NN N\n \
    DD  DD  UU  U  N  NNN  GG  GG  EE     OO  O N  NNN\n \
    DDDD     UUU   N   NN   GGGG   EEEEE   OOO  N   NN\n\n\n\
                           D\n\
                     D    DDD    D\n\
                    DDD  DDDDD  DDD\n\
                   DDDDDDDDDDDDDDDDD\n\
                   DDDDDDDDDDDDDDDDD\n\
                  DDDDDDDDDDDDDDDDDDD\n\
                DDDDDDDDDDDDDDDDDDDDDDD\n\
                  DDDDDDDDDDDDDDDDDDD\n\
                   DDDDDDDDDDDDDDDDD\n\
                        DDDDDDDD\n\n")

text = "It is a dark and dank night. The sky is pitch-black. A gathering sandstorm spreads across the desert, the wind howling and throwing sand on my sweaty face as I climb up the Pyramid. I cannot see further than an inch. I push on, slowly advancing. The thought of the mythical treasure hidden inside gives me the strength to reach the top. I am, after all, the greatest treasure hunter known to man. I take a crow bar out of my bag and start to pry apart the stones blocking the entrance to the Pyramid. I succeed, breaking my crow bar in the process. At last, I step down into the depths of the Pyramid…"

myprint(text)

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
    
    trap = check_traproom(loc)
    if trap == 1:
        in_trap(loc, trap)
    
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
    #Push
    if action == "push" or action == "press" or action == "touch":
        if target == "":
            print("I can't push nothingness")
        elif check_button(target,loc):
            print("I pushed"+target+". I can't push the"+target+" again.")
            button(target,loc)
            
        elif target == "me" or target == "myself":
            print("Now is not the time for this...") 

    #Moving
    elif action=="e" or action=="w" or action=="n" or action=="s" or action=="d" or action=="u" or action=="east" or action=="west" or action=="north" or action=="south" or action=="down" or action=="up":
        action = action[0]
        newloc = move(loc, action)
        if newloc == loc:
            print("I can't move there")
        else:
            loc = newloc
            look_around(loc)

    #check items in inventory
    elif action=="i" or action == "inventory":
        check_inventory()
        
    #pick up items
    elif action == "take" or action == "pick" and check_items(target):
        take_item(target, loc)
        
    #drop item
    elif action == "drop":
        drop_item(target, loc)
        
    #equip item
    elif action == "equip":
        hp = equip(target, loc, playermaxhp, playerhp)
        playerhp = hp[0]
        playermaxhp = hp[1]
    
    #help
    elif action == "help":
        print("The commands I can write are:\n e/east \n n/north \n s/south \n w/west \n d/down \n u/up \n i/inventory \n look/examine \n take/pick \n drop \n use \n press/touch/push \n fill hole \n equip \n unequip \n normal attack \n light attack \n heavy attack \n quit")
    
    #Easter egg commands :3
    elif action == "breathe":
        print("I know how to breathe without help, thank you")

    #???
    elif action == str.translate("fhzzba", mystery) and target == str.translate("ure", mystery) and loc == 11:
        if wwww == 0:
            sss()
            wwww = 1
            print("Rvquv, gur qrfgeblre bs jbeyqf, unf orra fhzzbarq")
        else:
            print("Gur qrrq unf orra qbar")

    elif action == str.translate("urniraf", mystery) and target == str.translate("qvivqr", mystery) and loc == 20:
        if ssss == 0:
            ssgw()
            print('"A patriot? Why are you giving me this?"')
            ssss = 1
        else:
            print('I see the choices within my hands.')
    elif action != "quit":
        print("I don't know how to "+action+".")
if not snoopdoglives:
    print("congratz you is winner")
else:
    print("The secrets of the dankest dungeon shall forever stay in the shadows")
