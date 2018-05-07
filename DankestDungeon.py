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

def issnoopdead():
    cur = db.cursor()
    sql = "SELECT enemy.HitPoints FROM enemy, enemytype WHERE enemytype.EnemytypeID = enemy.EnemytypeID AND enemytype.Name = 'Snoop Dogg'"
    cur.execute(sql)
    for row in cur.fetchall():
        return True
    return False
ssss = 0
def isequipped(item):
    cur = db.cursor()
    sql = "SELECT Equipped FROM item INNER JOIN itemtype ON itemtype.ItemtypeID = item.ItemtypeID AND itemtype.Name = '"+item+"'"
    cur.execute(sql)
    isit = cur.fetchone()
    if isit[0] == 0:
        return False
    elif isit[0] == 1:
        return True
    
def unequip(item, maxhp, curhp):
    cur = db.cursor()
    sql = "SELECT Type FROM itemtype INNER JOIN item ON itemtype.ItemtypeID = item.ItemtypeID AND itemtype.Name = '"+item+"' AND item.Equipped = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        if row[0] == 'shield':
            sql = "SELECT HitPoints FROM itemtype WHERE Name = '"+item+"'"
            cur.execute(sql)
            shieldhp = cur.fetchone()
            maxhp = maxhp - shieldhp[0]
            curhp = curhp - shieldhp[0]
            sql = "UPDATE Item, itemtype SET item.Equipped = 0 WHERE itemtype.ItemtypeID = item.ItemtypeID AND itemtype.Name = '"+item+"' AND Equipped = 1"
            cur.execute(sql)
            sql = "UPDATE playercharacter SET HitPoints = "+str(curhp)+" WHERE ID = 1"
            cur.execute(sql)
            return (maxhp, curhp, 1)
        elif row[0] == 'weapon':
            sql = "SELECT COUNT(*) FROM item INNER JOIN itemtype ON itemtype.ItemtypeID = item.ItemtypeID AND itemtype.Type = 'weapon' AND item.ID = 1"
            cur.execute(sql)
            weapons = cur.fetchone()
            if weapons[0] == 1:
                print("I probably should hold on to my only weapon")
                return(maxhp, curhp, 0)
            else:
                sql = "SELECT ItemID FROM item INNER JOIN itemtype ON itemtype.ItemtypeID = item.ItemtypeID AND itemtype.Type = 'weapon' AND item.ID = 1 AND itemtype.Name <> '"+item+"'"
                cur.execute(sql)
                for row2 in cur.fetchall():
                    bestweaponid = row2[0]
                sql = "UPDATE item, itemtype SET equipped = 0 WHERE itemtype.ItemtypeID = item.ItemtypeID AND item.ID = 1 AND itemtype.Name = '"+item+"'"
                cur.execute(sql)
                sql = "UPDATE item SET equipped = 1 WHERE ItemID = "+str(bestweaponid)
                cur.execute(sql)
                return(maxhp, curhp, 1)
    print("I can't unequip that.")
    return(maxhp, curhp, 0)
                
def look_around(loc):
    cur = db.cursor()
    sql = "SELECT Description FROM room WHERE RoomID = "+ str(loc)
    cur.execute(sql)
    for row in cur.fetchall():
        print(row[0]+'\n')
    sql = "SELECT Name FROM itemtype INNER JOIN item ON item.itemtypeID = itemtype.ItemtypeID AND item.RoomID = "+ str(loc)+" AND itemtype.Type <> 'Golden'"
    cur.execute(sql)
    if cur.rowcount > 0:
        print("")
        print("I see following things around the room")
    for row in cur.fetchall():
        print("<>", row[0])
    sql = "SELECT RoomID FROM merchant WHERE RoomID = "+ str(loc)
    cur.execute(sql)
    for row in cur.fetchall():
        print("I see a merchant in the room")
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
    phe.execute(fdy)

def check_inventory():
    cur = db.cursor()
    sql = "SELECT Name, Type, Equipped, Value FROM itemtype INNER JOIN item ON item.itemtypeID = itemtype.ItemtypeID AND item.ID = 1"
    cur.execute(sql)
    print("I have the following items in my inventory:")
    for row in cur.fetchall():
        print("#",row[0]+" | ("+row[1]+") | ("+str(row[3])+" gold)", end='')
        if row[2] == 1:
            print(" | (Equipped)")
        else:
            print("")
    sql = "SELECT money FROM playercharacter WHERE ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        print("I also have "+str(row[0])+" gold")
    return

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

def drop_item(item, loc, maxhp, curhp):
    cur = db.cursor()
    sql = "SELECT ItemID, Equipped FROM item INNER JOIN itemtype ON item.itemtypeID = itemtype.ItemtypeID AND item.ID = 1 AND itemtype.Name = '"+item+"'"
    cur.execute(sql)
    for row in cur.fetchall():
        if isequipped(item):
            unequipping = unequip(item, maxhp, curhp)
            if unequipping[2] == 0:
                return (maxhp, curhp)
        sql = "UPDATE item, itemtype SET RoomID = "+str(loc)+", ID = NULL WHERE item.itemtypeID = itemtype.ItemtypeID AND ItemID = "+str(row[0])
        cur.execute(sql)
        print("I have dropped the "+item+".")
        return(maxhp, curhp)
    print("I can't drop what I don't have.")
    return(maxhp, curhp)

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
    sql = "SELECT Description, HitPoints FROM playercharacter WHERE ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        print(row[0]+"\nI have "+str(row[1])+" HP")
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
        return(curhp, maxhp)
    for row in cur.fetchall():
        if row[0] == 1:
            print("I have that equipped already.")
            return(curhp, maxhp)
        roomid = row[1]
        itemtype = row[2]
        itemid = row[3]
    if roomid == loc:
        take_item(item, loc)
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
    sql = "UPDATE item, itemtype SET Equipped = 0 WHERE itemtype.ItemtypeID = item.ItemtypeID AND itemtype.Type = '"+itemtype+"' AND item.ID = 1 AND Equipped = 1"
    cur.execute(sql)
    sql = "UPDATE item SET Equipped = 1 WHERE ItemID = "+str(itemid)
    cur.execute(sql)
    print("I have equipped the "+item+".")
    return (curhp, maxhp)

def look_merchant(loc):
    cur = db.cursor()
    sql = "SELECT Description FROM merchant WHERE RoomID = "+ str(loc)
    cur.execute(sql)
    print("")
    for row in cur.fetchall():
        print(row[0])
        return
    print("There is no merchant here.")
    return

def talk_merchant(loc):
    cur = db.cursor()
    sql = "SELECT Name, Dialogue, MerchantID FROM merchant WHERE RoomID = "+ str(loc)
    cur.execute(sql)
    for row in cur.fetchall():
        print('I am "'+row[0]+'".\n'+row[1])
        merchantid = row[2]
    sql = "SELECT Name, Value FROM itemtype INNER JOIN item ON itemtype.ItemtypeID = item.ItemtypeID AND item.MerchantID = "+str(merchantid)
    cur.execute(sql)
    if cur.rowcount > 1:
        print('I have the following items on sale:')
        for row in cur.fetchall():
            print("- "+row[0]+"("+str(row[1])+" gold)")
    elif cur.rowcount > 1:
        print('I have the following item on sale:')
        for row in cur.fetchall():
            print("- "+row[0]+"("+str(row[1])+" gold)")
    else:
        print("It seems i have run out of stock.")
    return

def buy_item(loc, item):
    cur = db.cursor()
    sql = "SELECT MerchantID FROM merchant WHERE RoomID = "+ str(loc)
    cur.execute(sql)
    if cur.rowcount < 1:
        print("There is no merchant here.")
        return
    for row in cur.fetchall():
        merchantid = row[0]
    sql = "SELECT Money FROM playercharacter WHERE ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        money = row[0]
    sql = "SELECT Name, Value, item.ItemID FROM itemtype INNER JOIN item ON itemtype.ItemtypeID = item.ItemtypeID AND item.MerchantID = "+str(merchantid)+" AND itemtype.Name = '"+item+"'"
    cur.execute(sql)
    if cur.rowcount < 1:
        print("The merchant does not have that item.")
        return
    for row in cur.fetchall():
        if row[1] > money:
            print("Not enough gold, stranger")
            return
        money = money - row[1]
        sql = "UPDATE playercharacter SET Money = "+str(money)+" WHERE ID = 1"
        cur.execute(sql)
        sql = "UPDATE item SET MerchantID = NULL, ID = 1 WHERE ItemID ="+str(row[2])
        cur.execute(sql)
        print("I have bought the "+item+".")
        return
    print("There should be no way you are seeing this message :P")
    return

def sell_item(loc, item, maxhp, curhp):
    cur = db.cursor()
    sql = "SELECT MerchantID FROM merchant WHERE RoomID = "+ str(loc)
    cur.execute(sql)
    if cur.rowcount < 1:
        print("There is no merchant here.")
        return(maxhp, curhp)
    for row in cur.fetchall():
        merchantid = row[0]
    sql = "SELECT Money FROM playercharacter WHERE ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        money = row[0]
    sql = "SELECT Name, Value, item.ItemID FROM itemtype INNER JOIN item ON itemtype.ItemtypeID = item.ItemtypeID AND item.ID= 1 AND itemtype.Name = '"+item+"'"
    cur.execute(sql)
    if cur.rowcount < 1:
        print("I don't have that item.")
        return(maxhp, curhp)
    for row in cur.fetchall():
        if isequipped(item):
            unequipping = unequip(item, maxhp, curhp)
            if unequipping[2] == 0:
                return (maxhp, curhp)
        money = money + int(row[1] * 0.5)
        sql = "UPDATE playercharacter SET Money = "+str(money)+" WHERE ID = 1"
        cur.execute(sql)
        sql = "UPDATE item SET MerchantID = "+str(merchantid)+", ID = NULL WHERE ItemID ="+str(row[2])
        cur.execute(sql)
        print("I have sold the "+item+".")
        return(maxhp, curhp)
    print("There should be no way you are seeing this message :P")
    return(maxhp, curhp)

def buttonpush(loc):
    cur = db.cursor()
    sql = "SELECT itemtype.Value, itemtype.itemtypeID FROM item, itemtype WHERE item.ItemtypeID = itemtype.ItemtypeID AND itemtype.Type = 'button' AND RoomID = "+ str(loc)
    cur.execute(sql)
    if cur.rowcount == 0:
        print("There are no buttons here")
        return
    for row in cur.fetchall():
        if row[0] == 0:
            sql = "UPDATE itemtype SET Value = 1 WHERE ItemtypeID = "+str(row[1])
            cur.execute(sql)
            print("I push the button")
        elif row[0] == 1:
            print("I already pushed that")
            return
    sql = "SELECT Locked FROM leads_to WHERE RoomID_1 = 14 AND Leads_toRoomID_2 = 21"
    cur.execute(sql)
    locked = cur.fetchone()
    if locked[0] == 1:
        sql = "SELECT COUNT(*) FROM itemtype WHERE Type = 'button' AND Value = 1"
        cur.execute(sql)
        for row in cur.fetchall():
            if row[0] == 4:
                print("A door has opened elsewhere.")
                sql = "UPDATE leads_to SET locked = 0 WHERE (RoomID_1 = 14 AND Leads_toRoomID_2 = 21) OR (RoomID_1 = 18 AND Leads_toRoomID_2 = 20)"
                cur.execute(sql)
    else:
        return

def usehppotion(playermaxhp):
    cur = db.cursor()
    sql = "SELECT item.itemID FROM item, itemtype WHERE item.ItemtypeID = itemtype.ItemtypeID AND itemtype.Name = 'healing potion' AND item.ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        sql = "UPDATE item SET ID = NULL WHERE ItemID = "+str(row[0])
        cur.execute(sql)
        sql = "UPDATE playercharacter SET HitPoints = "+str(playermaxhp)
        cur.execute(sql)
        return True
    print("I don't have a healing potion")
    return False

def anvilcheck():
    cur = db.cursor()
    sql = "SELECT COUNT(*) FROM item, itemtype WHERE item.ItemtypeID = itemtype.ItemtypeID AND itemtype.Type = 'key' AND item.ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        if row[0] == 2:
            print("The keys have been joined into a master key")
            sql = "UPDATE item, itemtype SET item.ID = NULL WHERE item.ItemtypeID = itemtype.ItemtypeID AND (itemtype.Name = 'key piece' OR itemtype.Name = 'key fragment')"
            cur.execute(sql)
            sql = 'INSERT INTO itemtype VALUES(75, "Master key", "From two pieces a key was created", 0, 0, 1, "key", 0, 1, 3)'
            cur.execute(sql)
            sql = 'INSERT INTO item VALUES(NULL, 1, NULL, NULL, 75, 0)'
            cur.execute(sql)
            return
    print("It's like something is still missing...")
    return

def keycheck():
    cur = db.cursor()
    sql = "SELECT COUNT(*) FROM item, itemtype WHERE item.ItemtypeID = itemtype.ItemtypeID AND itemtype.Name = 'master key' AND item.ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        if row[0] == 1:
            sql = "UPDATE leads_to SET locked = 0 WHERE RoomID_1 = 29 AND Leads_toRoomID_2 = 36"
            cur.execute(sql)
            print("The door has opened")

def goldencheck():
    cur = db.cursor()
    sql = "SELECT COUNT(*) FROM item, itemtype WHERE item.ItemtypeID = itemtype.ItemtypeID AND itemtype.Type = 'golden' AND item.ID = 1"
    cur.execute(sql)
    for row in cur.fetchall():
        if row[0] == 3:
            return True
    return False

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
    cur = db.cursor()
    sql = "SELECT enemytype.riddle FROM enemytype,enemy WHERE enemytype.Name = '"+enemyname+"' AND enemy.RoomID ="+str(loc)
    cur.execute(sql)
    for row in cur:
        if len(row[0]) > 0:
            return True
        else:
            return False
    
def check_riddle(enemyname):
    cur = db.cursor()
    sql = "SELECT enemytype.riddle FROM enemytype WHERE enemytype.Name = '"+enemyname+"'"
    cur.execute(sql)
    for row in cur:
        return row[0]
    return

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


def fight_enemy(loc, playerhp):
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
    if riddle(enemyname, loc) == True:
        print(check_riddle(enemyname))
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
    while enemyhp > 0 and playerhp > 0:
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
    if playerhp <= 0:
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
    action = ""
    target = ""
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
    return trap

#by Essi :)

def make_enemytype_list(level):
    cur = db.cursor()
    enemytypes = []
    #hae vihollistyyppien id:t, joissa oikea level ja isUnique = 0
    sql = "SELECT enemytype.EnemytypeID FROM enemytype WHERE enemytype.Level = " + str(level) + " AND isUnique = 0;"
    cur.execute(sql)
    tempenemytypes = cur.fetchall()
        
    #muodosta vihollistyyppien id-numeroista oma lista
    for row in tempenemytypes:
        enemytypes.append(row[0])

    return enemytypes

def make_room_list(level):
    #hae kentän huoneet, joissa encounter = 1
    rooms = []
    cur = db.cursor()
    sql = "SELECT room.RoomId FROM room WHERE room.Level = " + str(level) + " AND room.Encounter = 1;"
    cur.execute(sql)
    temprooms = cur.fetchall()
        
    #muodosta huoneiden id-numeroista oma lista
    for row in temprooms:
        rooms.append(row[0])

    return rooms

def make_itemtype_list(level):
    cur = db.cursor()
    itemtypes = []
    #valitse kentän esineet tähän
    sql = "SELECT itemtype.ItemtypeID FROM itemtype WHERE created = 0 AND ((level <= " + str(level) + " AND level != 0) OR level = 5);"
    cur.execute(sql)
            
    tempitemtypes = cur.fetchall()
    for row in tempitemtypes:
        itemtypes.append(row[0])
    return itemtypes

def set_traproom(rooms, roomid):
    cur = db.cursor()
    sql = "INSERT INTO Trap VALUES(NULL, 'The room seems to be bit off... Oh no sand starts to fill the room from a hole. You need to do something but what?', 1, " + str(roomid) +");"
    cur.execute(sql)
    rooms.remove(roomid)
    return

def set_room(rooms):
    itemroomind = random.randint(0, len(rooms)-1)
    itemroomid = rooms[itemroomind]
    return itemroomid

def set_item(itemroomid, itemtypes):
    cur = db.cursor()
    itemtypeind = random.randint((0),(len(itemtypes)-1))
    itemtypeid = itemtypes[itemtypeind]
    sql = "INSERT INTO item VALUES (NULL, NULL, " + str(itemroomid) + ", NULL, " + str(itemtypeid) + ", 0);"
    cur.execute(sql)
    return itemtypeid

def remove_if_weapon(itemtypeid, itemtypes):
    cur = db.cursor()
    if itemtypeid <= 9:
        sql = "UPDATE ITEMTYPE SET Created=1 WHERE ItemtypeID = " + str(itemtypeid) + ";"
        cur.execute(sql)
        itemtypes.remove(itemtypeid)
    return 

def set_merchant_items(level, itemtypes):
    cur =db.cursor()
    for i in range(0,2):
        itemtypeind = random.randint((0),(len(itemtypes)-1))
        itemtypeid = itemtypes[itemtypeind]
        sql = "INSERT INTO item VALUES (NULL, NULL, NULL, " + str(level) + ", " + str(itemtypeid) +", 0);"
        cur.execute(sql)

        remove_if_weapon(itemtypeid, itemtypes)
    return 

def set_health_items(level):
    cur = db.cursor()
    #tehdään eka lista health itemtypeista
    healthtypes = []
    #hae vihollistyyppien id:t, joissa oikea level ja isUnique = 0
    sql = "SELECT itemtype.itemtypeID FROM itemtype WHERE itemtypeID = 10 OR itemtypeID = 12;"
    cur.execute(sql)
    temphealthtypes = cur.fetchall()
        
    #muodosta vihollistyyppien id-numeroista oma lista
    for row in temphealthtypes:
        healthtypes.append(row[0])

    ind = random.randint((0),(len(healthtypes)-1))
    idid = healthtypes[ind]
    sql = "INSERT INTO item VALUES (NULL, NULL, NULL, " + str(level) + ", " + str(idid) + ", 0);"
    cur.execute(sql)
    
    return

def set_enemy(rooms, enemytypes):
    cur = db.cursor()
    enemytypeind = random.randint((0),(len(enemytypes)-1))
    enemytypeid = enemytypes[enemytypeind]

    #haetaan tarvittavat tiedot, hitpointsit, tietokannasta, jotta voidaan luoda vihollinen
    sql = "SELECT enemytype.HitPoints FROM enemytype WHERE enemytype.EnemytypeID = " + str(enemytypeid) + ";"
    cur.execute(sql)
    temphitpoints = cur.fetchall()
    for row in temphitpoints:
            hitpoints = row[0]
                
    #luodaan  vihollinen ja asetetaan se huoneeseen
    sql = "INSERT INTO enemy VALUES (NULL, " + str(hitpoints) + ", " + str(rooms[-1]) + ", " + str(enemytypeid) + ");"
    cur.execute(sql)
    return

def randomize_all():

    for level in range(1,4):

        rooms = make_room_list(level)

        enemytypes = make_enemytype_list(level)
       
        #asetetaan ykköskentän trap
        if level == 1:

            #arvotaan rooms-listalta huone, johon asetetaan trap
            whichtraproom = random.randint(1,3)
            
            #tallennetaan indeksiä vastaava huone muuttujaan ja poistetaan indeksiä vastaava huone rooms-listalta
            if whichtraproom == 1:
                set_traproom(rooms, 3)
                     
            elif whichtraproom == 2:
                set_traproom(rooms, 6)

            else:
                set_traproom(rooms, 8)

        #muodosta tavaratyyppien id-numeroista lista, joka ensin ekassa kentässä tietynlainen
        #jos randomissa tulee ase tai kilpi, se poistetaan listalta ja päivitetään tietokantaan, että sellainen item on luotu
        #hae tavaratyyppien id, joissa created = 0 ja kentän mukaan
        
        itemtypes = make_itemtype_list(level)

        #arvotaan eri 2 huonetta, joihin tulee tavaraa
        itemroomid = set_room(rooms)
        itemroomid2 = set_room(rooms)
            
        while itemroomid == itemroomid2:
            itemroomid2 = set_room(rooms)
            
        #arvotaan tavara huoneeseen ja luodaan esine huoneeseen
        itemtypeid = set_item(itemroomid, itemtypes)

        #jos arvotaan ase tai kilpi, updatetaan created tietokantaan ja poistetaan se huoneiden arvontalistalta
        remove_if_weapon(itemtypeid, itemtypes)

        itemtypeid = set_item(itemroomid2, itemtypes)

        remove_if_weapon(itemtypeid, itemtypes)

        #merchantin tavaroiden arpominen
        set_merchant_items(level, itemtypes)

        set_health_items(level)
           
        #sitten kaikkiin encounter = 1 huoneisiin arvotaan viholliset
        #ensin otetaan huone järjestyksessä, aloitetaan listan lopusta
        #sitten arvotaan, mikä vihollistyyppi huoneessa on
        #luodaan huoneeseen vihollinen

        while len(rooms) != 0:

            set_enemy(rooms, enemytypes)

            del rooms[-1]

        enemytypes.clear()

    return    
         
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

#Randomize everything into the floors
randomize_all()

snoopdoglives = True
action = ""

look_around(loc)
#Main Loop
while action!="quit" and playerhp > 0 and snoopdoglives:

    vihuhp = check_enemyhp(loc)
    while  vihuhp > 0 and playerhp > 0:
        fight_enemy(loc, playerhp)
        vihuhp = check_enemyhp(loc)
        delete_deathenemy()
        playerhp = check_playerhp()
    playerhp = check_playerhp()
    snoopdoglives = issnoopdead()
    if loc == 36:
        if goldencheck():
            loc = 37
            sql = "UPDATE playercharacter SET RoomID = "+str(loc)
            cur.execute(sql)
            print("There are intendations on the wall for 3 items, the golden ankh, the golden skull and the golden monkey. Luckily I have those items. Once I placed the items, a strange force pulled me into a dank, dark place... This must be the dankest dungeon I've ever been in.")
        else:
            print("There are intendations on the wall, they are for an ankh, a skull and a monkey. It seems I have missed something. The treasures in the deepest depths of the dungeon shall remain in the shadows...")
            exit()
    if playerhp > 0 and snoopdoglives:
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
        elif action == "push" or action == "press" or action == "touch":
            if target == "":
                print("I can't push what ain't there.")
            elif target == "button" or target == "snake button" or target == "jaquar button" or target == "quetzal button" or target == "butterfly button":
                buttonpush(loc)
            elif target == "me" or target == "myself":
                print("this is not the time for that")

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
            if target == "eidhi" and wwww == 1:
                print("I'd rather not.")
            else:
                hp = drop_item(target, loc, playermaxhp, playerhp)
                playerhp = hp[0]
                playermaxhp = hp[1]
            
        #equip item
        elif action == "equip":
            hp = equip(target, loc, playermaxhp, playerhp)
            playerhp = hp[0]
            playermaxhp = hp[1]
            
        #talk to merchant
        elif action == "talk" and target == "merchant":
            talk_merchant(loc)

        #buy item
        elif action == "buy":
            buy_item(loc, target)
            
        #sell item
        elif action == "sell":
            if target == "eidhi" and wwww == 1:
                print("Some things are too valuable to sell.")
            else:
                hp = sell_item(loc, target, playermaxhp, playerhp)
                playerhp = hp[0]
                playermaxhp = hp[1]
                
        #Unequip item
        elif action == "unequip":
            success = unequip(target, playermaxhp, playerhp)
            if success[2] == 1:
                playermaxhp = success[0]
                playerhp = success[1]
                print("I have unequipped "+target+".")
        #use
        elif action == "use":
            if target == "healing potion":
                if usehppotion(playermaxhp):
                    playerhp = playermaxhp
            elif target == "anvil" and loc == 28:
                anvilcheck()
            elif target == "master key" and loc == 29:
                keycheck()
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
        #dev action, remember to delete
        elif action == "destroy" and target == "everything":
            cur = db.cursor()
            sql = "DELETE FROM enemy"
            cur.execute(sql)
            sql = "INSERT INTO enemy VALUES(NULL,140,38,15)"
            cur.execute(sql)
        elif action != "quit":
            print("I don't know how to "+action+".")
if not snoopdoglives:
    print("congratz you is winner")
else:
    print("The secrets of the dankest dungeon shall forever stay in the shadows")
