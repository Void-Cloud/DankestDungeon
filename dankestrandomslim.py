#kirjasto tietokantaa varten
import mysql.connector
import random

#@Essi :)

def randomize_all():

    def set_traproom(roomid):
        sql3 = "INSERT INTO Trap VALUES(NULL, 'The room seems to be bit off... Oh no sand starts to fill the room from a hole. You need to do something but what?', 1, " + str(roomid) +");"
        cur.execute(sql3)
        rooms.remove(roomid)
        return

    def set_enemy():
        enemytypeind = random.randint((0),(len(enemytypes)-1))
        enemytypeid = enemytypes[enemytypeind]

        #haetaan tarvittavat tiedot, hitpointsit, tietokannasta, jotta voidaan luoda vihollinen
        sql4 = "SELECT enemytype.HitPoints FROM enemytype WHERE enemytype.EnemytypeID = " + str(enemytypeid) + ";"
        cur.execute(sql4)
        temphitpoints = cur.fetchall()
        for row in temphitpoints:
            hitpoints = row[0]
                
        #luodaan  vihollinen ja asetetaan se huoneeseen
        sql5 = "INSERT INTO enemy VALUES (NULL, " + str(hitpoints) + ", " + str(rooms[-1]) + ", " + str(enemytypeid) + ");"
        cur.execute(sql5)
        return

    def set_item():
        itemtypeind = random.randint((0),(len(itemtypes)-1))
        itemtypeid = itemtypes[itemtypeind]

        #luodaan esine ja asetetaan se huoneeseen
        #(ItemID, ID(pelaaja), RoomID, MerchantID, ItemtypeID)
        sql5 = "INSERT INTO item VALUES (NULL, NULL, " + str(rooms[-1]) + ", NULL, " + str(itemtypeid) + ");"
        cur.execute(sql5)
        return
    
    #muuttujia ja listoja
    rooms = []
    itemtypes = []
    enemytypes = []
    level = 1
    cur = db.cursor()

    #muodosta tavaratyyppien id-numeroista oma lista, jos tavaratyypit samat kaikissa kentissä
    #hae tavaratyyppien id, joissa created = 0
    sql1 = "SELECT itemtype.ItemtypeID FROM itemtype WHERE created = 0"
    cur.execute(sql1)
    tempitemtypes = cur.fetchall()
    for row in tempitemtypes:
        itemtypes.append(row[0])

    while level <= 3:

        #hae kentän huoneet, joissa encounter = 1
        sql = "SELECT room.RoomId FROM room WHERE room.Level = " + str(level) + " AND room.Encounter = 1;"
        cur.execute(sql)
        temprooms = cur.fetchall()
        
        #muodosta huoneiden id-numeroista oma lista
        for row in temprooms:
            rooms.append(row[0])

        #hae vihollistyyppien id:t, joissa oikea level ja isUnique = 0
        sql = "SELECT enemytype.EnemytypeID FROm enemytype WHERE enemytype.Level = " + str(level) + " AND isUnique = 0;"
        cur.execute(sql)
        tempenemytypes = cur.fetchall()
        
        #muodosta vihollistyyppien id-numeroista oma lista
        for row in tempenemytypes:
            enemytypes.append(row[0])

        #asetetaan ykköskentän trap

        if level == 1:

            #arvotaan rooms-listalta huone, johon asetetaan trap
            whichtraproom = random.randint(1,3)
            
            #tallennetaan indeksiä vastaava huone muuttujaan ja poistetaan indeksiä vastaava huone rooms-listalta
            if whichtraproom == 1:
                set_traproom(3)
                     
            elif whichtraproom == 2:
                set_traproom(6)

            else:
                set_traproom(8)
        
        #sitten arvotaan, mitä muissa huoneissa on
        #ensin otetaan huone järjestyksessä, aloitetaan listan lopusta
        #sitten arvotaan, onko siinä huoneessa esine vai vihollinen vai molemmat

        while len(rooms) != 0:

            #muuttuja, johon tallennetaan kummasta listasta, esinetyypeistä, vihollistyypeistä vai molemmista arvotaan encounter
            which = random.randint(1,3) 

            #jos which == 1, valitaan vihollislistalta; jos 2, valitaan esinelistalta; jos 3, molemmista tulee
            if which == 1:
                set_enemy()
                del rooms[-1]

            elif which == 2:
                set_item()
                del rooms[-1]

            else:
                set_enemy()
                set_item()
                del rooms[-1]
        
        enemytypes.clear()
        level = level + 1

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

#randomize_merchants()

db.rollback()
db.close()
