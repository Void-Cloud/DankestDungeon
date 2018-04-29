#kirjasto tietokantaa varten
import mysql.connector
import random

#@Essi :)
def randomize_all():

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
    #print("itemtypeids =", itemtypes)

    while level <= 3:

        #print("------LEVEL ", level, " --------")

        #hae kentän huoneet, joissa encounter = 1
        sql = "SELECT room.RoomId FROM room WHERE room.Level = " + str(level) + " AND room.Encounter = 1;"
        cur.execute(sql)
        temprooms = cur.fetchall()
        
        #muodosta huoneiden id-numeroista oma lista
        for row in temprooms:
            rooms.append(row[0])
        #print("roomids =", rooms)

        #hae vihollistyyppien id:t, joissa oikea level ja isUnique = 0
        sql2 = "SELECT enemytype.EnemytypeID FROm enemytype WHERE enemytype.Level = " + str(level) + " AND isUnique = 0;"
        cur.execute(sql2)
        tempenemytypes = cur.fetchall()
        
        #muodosta vihollistyyppien id-numeroista oma lista
        for row in tempenemytypes:
            #print("enemytype is ", row[0])
            enemytypes.append(row[0])
        #print("enemytypeids={}".format(enemytypes))

        if level == 1:
            
            #print("----trapin asettaminen-----")

            #arvotaan rooms-listalta huone, johon asetetaan trap
            whichtraproom = random.randint(1,3)
            #print("whichtraproom =", whichtraproom)
            
            #tallennetaan indeksiä vastaava huone muuttujaan ja poistetaan indeksiä vastaava huone rooms-listalta
            if whichtraproom == 1:
                traproomid = 3
                sql3 = "INSERT INTO Trap VALUES(NULL, 'The room seems to be bit off... Oh no sand starts to fill the room from a hole. You need to do something but what?', 1, " + str(traproomid) +");"
                cur.execute(sql3)
                rooms.remove(traproomid)
                #print("traproomid =", traproomid)
                
            elif whichtraproom == 2:
                traproomid = 6
                sql3 = "INSERT INTO Trap VALUES(NULL, 'The room seems to be bit off... Oh no sand starts to fill the room from hole. You need to do something but what?', 1, 6);"
                cur.execute(sql3)
                rooms.remove(traproomid)
                #print("traproomid =", traproomid)

            else:
                traproomid = 8
                sql3 = "INSERT INTO Trap VALUES(NULL, 'The room seems to be bit off... Oh no sand starts to fill the room from hole. You need to do something but what?', 1, 8);"
                cur.execute(sql3)
                rooms.remove(traproomid)
                #print("traproomid is ", traproomid)
                
            #print("rooms =", rooms)
        
        #sitten arvotaan, mitä muissa huoneissa on
        #ensin otetaan huone järjestyksessä, aloitetaan listan lopusta
        #sitten arvotaan, onko siinä huoneessa esine vai vihollinen vai molemmat

        #print("---- muiden juttujen arvonta alkaa levelillä ", level, "---------")
        while len(rooms) != 0:

            #muuttuja, johon tallennetaan kummasta listasta, esinetyypeistä, vihollistyypeistä vai molemmista arvotaan encounter
            which = random.randint(1,3) #huomhuomhuom
            #print(which, "is going to be in the last room on the list")

            #jos which == 1, valitaan vihollislistalta; jos 2, valitaan esinelistalta; jos 3, molemmista tulee
            if which == 1:
                #print("It's an enemy!")
                enemytypeind = random.randint((0),(len(enemytypes)-1))
                #print("enemyind= ", enemytypeind)
                enemytypeid = enemytypes[enemytypeind]
                #print("enemyid is ", enemytypeid)

                #haetaan tarvittavat tiedot, hitpointsit, tietokannasta, jotta voidaan luoda vihollinen
                sql4 = "SELECT enemytype.HitPoints FROM enemytype WHERE enemytype.EnemytypeID = " + str(enemytypeid) + ";"
                cur.execute(sql4)
                temphitpoints = cur.fetchall()
                for row in temphitpoints:
                    #print("hitpoints are ", row[0])
                    hitpoints = row[0]
                    #print("hitpoints are ", hitpoints)
                
                #luodaan  vihollinen ja asetetaan se huoneeseen
                sql5 = "INSERT INTO enemy VALUES (NULL, " + str(hitpoints) + ", " + str(rooms[-1]) + ", " + str(enemytypeid) + ");"
                cur.execute(sql5)
                del rooms[-1]
                #print("rooms = ", rooms)

            elif which == 2:
                #print("It's an item!")
                itemtypeind = random.randint((0),(len(itemtypes)-1))
                #print("itemtypeind= ", itemtypeind)
                itemtypeid = itemtypes[itemtypeind]
                #print("itemtypeid is ", itemtypeid)

                #luodaan esine ja asetetaan se huoneeseen
                #(ItemID, ID(pelaaja), RoomID, MerchantID, ItemtypeID)
                sql5 = "INSERT INTO item VALUES (NULL, NULL, " + str(rooms[-1]) + ", NULL, " + str(itemtypeid) + ");"
                cur.execute(sql5)
                del rooms[-1]
                #print("rooms = ", rooms)
   
            else:
                #print("It's both!")
            
                enemytypeind = random.randint((0),(len(enemytypes)-1))
                #print("enemyind= ", enemytypeind)
                enemytypeid = enemytypes[enemytypeind]
                #print("enemyid is ", enemytypeid)

                #haetaan tarvittavat tiedot, hitpointsit, tietokannasta, jotta voidaan luoda vihollinen
                sql4 = "SELECT enemytype.HitPoints FROM enemytype WHERE enemytype.EnemytypeID = " + str(enemytypeid) + ";"
                cur.execute(sql4)
                temphitpoints = cur.fetchall()
                for row in temphitpoints:
                    #print("hitpoints are ", row[0])
                    hitpoints = row[0]
                    #print("hitpoints are ", hitpoints)
                
                #luodaan  vihollinen ja asetetaan se huoneeseen
                sql5 = "INSERT INTO enemy VALUES (NULL, " + str(hitpoints) + ", " + str(rooms[-1]) + ", " + str(enemytypeid) + ");"
                cur.execute(sql5)

                itemtypeind = random.randint((0),(len(itemtypes)-1))
                #print("itemtypeind= ", itemtypeind)
                itemtypeid = itemtypes[itemtypeind]
                #print("itemtypeid is ", itemtypeid)

                #luodaan esine ja asetetaan se huoneeseen
                #(ItemID, ID(pelaaja), RoomID, MerchantID, ItemtypeID)
                sql5 = "INSERT INTO item VALUES (NULL, NULL, " + str(rooms[-1]) + ", NULL, " + str(itemtypeid) + ");"
                cur.execute(sql5)
                del rooms[-1]
                #print("rooms = ", rooms)
        
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
