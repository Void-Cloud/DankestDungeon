import mysql.connector
import random

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

#-- pääohjelma --

#avataan tietokantayhteys
#teht1
db = mysql.connector.connect(host="localhost",
                             user = "dbuser",
                             passwd = "dbpass",
                             db = "dankestdungeon",
                             buffered = True)

print("Tietokantaan saatiin yhteys, jee!")

randomize_all()

db.rollback()
db.close()
