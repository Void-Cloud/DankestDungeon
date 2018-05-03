import mysql.connector
import random

#@Essi :)



def randomize_all():

    #pitäisikö nämä aliohjelmat laittaa ulkopuolelle ja antaa parametreina tiedot cur ja rooms ja muut ja palauttaa muuttuneet jutut

    def set_traproom(roomid):
        sql = "INSERT INTO Trap VALUES(NULL, 'The room seems to be bit off... Oh no sand starts to fill the room from a hole. You need to do something but what?', 1, " + str(roomid) +");"
        cur.execute(sql)
        rooms.remove(roomid)
        return

    def set_enemy():
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

    #jos merchantia ei tule, tämä käyttöön?
    #def set_item():
        #itemtypeind = random.randint((0),(len(itemtypes)-1))
        #itemtypeid = itemtypes[itemtypeind]

        #luodaan esine ja asetetaan se huoneeseen
        #(ItemID, ID(pelaaja), RoomID, MerchantID, ItemtypeID)
        #sql = "INSERT INTO item VALUES (NULL, NULL, " + str(rooms[-1]) + ", NULL, " + str(itemtypeid) + ", 0);"
        #cur.execute(sql)
        #return
    
    #muuttujia ja listoja
    rooms = []
    itemtypes = []
    enemytypes = []
    #tämä vielä toimimaan!!!!!!!!
    healthitemtypes = []
    cur = db.cursor()

    #tarvitseeko neljännelle kentälle???
    for level in range(1,5):

        #hae kentän huoneet, joissa encounter = 1
        sql = "SELECT room.RoomId FROM room WHERE room.Level = " + str(level) + " AND room.Encounter = 1;"
        cur.execute(sql)
        temprooms = cur.fetchall()
        
        #muodosta huoneiden id-numeroista oma lista
        for row in temprooms:
            rooms.append(row[0])

        #hae vihollistyyppien id:t, joissa oikea level ja isUnique = 0
        sql = "SELECT enemytype.EnemytypeID FROM enemytype WHERE enemytype.Level = " + str(level) + " AND isUnique = 0;"
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

        #muodosta tavaratyyppien id-numeroista lista, joka ensin ekassa kentässä tietynlainen
        #jos randomissa tulee ase tai kilpi, se poistetaan listalta ja päivitetään tietokantaan, että sellainen on olemassa
        #hae tavaratyyppien id, joissa created = 0 ja kentän mukaan
        if level == 1:
            #valitse kentän esineet tähän
            sql = "SELECT itemtype.ItemtypeID FROM itemtype WHERE created = 0 AND (level = " + str(level) + " OR level = 5);"
            cur.execute(sql)
            tempitemtypes = cur.fetchall()
            for row in tempitemtypes:
                itemtypes.append(row[0])

            
            #arvotaan 2 huonetta, joihin tavaraa tulee
            itemroomind = random.randint(0, len(rooms)-1)
            itemroomid = rooms[itemroomind]
            print("tämä on tärkeä: " + str(itemroomid))

            itemroomind2 = itemroomind
            while itemroomind == itemroomind2:
                itemroomind2 = random.randint(0, len(rooms)-1)

            itemroomid2 = rooms[itemroomind2]
            
            #arvotaan tavara huoneeseen
            itemtypeind = random.randint((0),(len(itemtypes)-1))
            itemtypeid = itemtypes[itemtypeind]

            #luodaan esine ja asetetaan se huoneeseen
            #jos arvotaan ase tai kilpi, updatetaan created tietokantaan ja poistetaan se huoneiden arvontalistalta
            #(ItemID, ID(pelaaja), RoomID, MerchantID, ItemtypeID)
            sql = "INSERT INTO item VALUES (NULL, NULL, " + str(itemroomid) + ", NULL, " + str(itemtypeid) + ", 0);"
            cur.execute(sql)

            if itemtypeid <= 9:
                sql = "UPDATE ITEMTYPE SET Created=1 WHERE ItemtypeID = " + str(itemtypeid) + ";"
                cur.execute(sql)
                itemtypes.remove(itemtypeid)

            itemtypeind = random.randint((0),(len(itemtypes)-1))
            itemtypeid = itemtypes[itemtypeind]
            sql = "INSERT INTO item VALUES (NULL, NULL, " + str(itemroomid2) + ", NULL, " + str(itemtypeid) + ", 0);"
            cur.execute(sql)

            if itemtypeid <= 9:
                sql = "UPDATE ITEMTYPE SET Created=1 WHERE ItemtypeID = " + str(itemtypeid) + ";"
                cur.execute(sql)
                itemtypes.remove(itemtypeid)

            #merchantin tavaroiden arpominen
            
            for i in range(0,2):
                itemtypeind = random.randint((0),(len(itemtypes)-1))
                itemtypeid = itemtypes[itemtypeind]
                sql = "INSERT INTO item VALUES (NULL, NULL, NULL, " + str(level) + ", " + str(itemtypeid) +", 0);"
                cur.execute(sql)
                
                if itemtypeid <= 9:
                    sql = "UPDATE ITEMTYPE SET Created=1 WHERE ItemtypeID = " + str(itemtypeid) + ";"
                    cur.execute(sql)
                    itemtypes.remove(itemtypeid)
          
        elif level == 2:
            #lisää vain ne jutut listalle, joita siellä ei vielä ole
            sql = "SELECT itemtype.ItemtypeID FROM itemtype WHERE created = 0 AND ((level > 0 AND level <= " + str(level) + ") OR level = 5);"
            cur.execute(sql)
            tempitemtypes = cur.fetchall()
            #käydään lista läpi
            for row in tempitemtypes:
                #jos listassa ei esiinny kyseistä esinetyyppiid:tä, niin se lisätään listaan
                if itemtypes.count(row[0]) == 0:
                    itemtypes.append(row[0])
            #print(itemtypes)
            
            #arvotaan 2 huonetta, joihin tavaraa tulee
            itemroomind = random.randint(0, len(rooms)-1)
            itemroomid = rooms[itemroomind]
            print("tämä on tärkeä: " + str(itemroomid))

            itemroomind2 = itemroomind
            while itemroomind == itemroomind2:
                itemroomind2 = random.randint(0, len(rooms)-1)
            itemroomid2 = rooms[itemroomind2]
            
            itemtypeind = random.randint((0),(len(itemtypes)-1))
            itemtypeid = itemtypes[itemtypeind]

            #luodaan esine ja asetetaan se huoneeseen (aseita on aina vain yksi: jos arvotaan ase, poistetaan se listalta)
            #(ItemID, ID(pelaaja), RoomID, MerchantID, ItemtypeID)
            sql = "INSERT INTO item VALUES (NULL, NULL, " + str(itemroomid) + ", NULL, " + str(itemtypeid) + ", 0);"
            cur.execute(sql)

            if itemtypeid <= 9:
                sql = "UPDATE ITEMTYPE SET Created=1 WHERE ItemtypeID = " + str(itemtypeid) + ";"
                cur.execute(sql)
                itemtypes.remove(itemtypeid)

            itemtypeind = random.randint((0),(len(itemtypes)-1))
            itemtypeid = itemtypes[itemtypeind]
            sql = "INSERT INTO item VALUES (NULL, NULL, " + str(itemroomid2) + ", NULL, " + str(itemtypeid) + ", 0);"
            cur.execute(sql)

            if itemtypeid <= 9:
                sql = "UPDATE ITEMTYPE SET Created=1 WHERE ItemtypeID = " + str(itemtypeid) + ";"
                cur.execute(sql)
                itemtypes.remove(itemtypeid)

            #merchantin tavaroiden arpominen
            
            for i in range(0,2):
                itemtypeind = random.randint((0),(len(itemtypes)-1))
                itemtypeid = itemtypes[itemtypeind]
                sql = "INSERT INTO item VALUES (NULL, NULL, NULL, " + str(level) + ", " + str(itemtypeid) +", 0);"
                cur.execute(sql)
                
                if itemtypeid <= 9:
                    sql = "UPDATE ITEMTYPE SET Created=1 WHERE ItemtypeID = " + str(itemtypeid) + ";"
                    cur.execute(sql)
                    itemtypes.remove(itemtypeid)
            
            
        elif level == 3:
            sql = "SELECT itemtype.ItemtypeID FROM itemtype WHERE created = 0 AND ((level > 0 AND level <= " + str(level) + ") OR level = 5);"
            cur.execute(sql)
            tempitemtypes = cur.fetchall()
            for row in tempitemtypes:
                #jos listassa ei esiinny kyseistä esinetyyppiid:tä, niin se lisätään listaan
                if itemtypes.count(row[0]) == 0:
                    itemtypes.append(row[0])
            print(itemtypes)

            #arvotaan 2 huonetta, joihin tavaraa tulee
            itemroomind = random.randint(0, len(rooms)-1)
            itemroomid = rooms[itemroomind]
            #
            print("tämä on tärkeä: " + str(itemroomid))

            itemroomind2 = itemroomind
            while itemroomind == itemroomind2:
                itemroomind2 = random.randint(0, len(rooms)-1)
            itemroomid2 = rooms[itemroomind2]
            
            itemtypeind = random.randint((0),(len(itemtypes)-1))
            itemtypeid = itemtypes[itemtypeind]

            #luodaan esine ja asetetaan se huoneeseen (aseita on aina vain yksi: jos arvotaan ase, poistetaan se listalta)
            #(ItemID, ID(pelaaja), RoomID, MerchantID, ItemtypeID)
            sql = "INSERT INTO item VALUES (NULL, NULL, " + str(itemroomid) + ", NULL, " + str(itemtypeid) + ", 0);"
            cur.execute(sql)

            if itemtypeid <= 9:
                sql = "UPDATE ITEMTYPE SET Created=1 WHERE ItemtypeID = " + str(itemtypeid) + ";"
                cur.execute(sql)
                itemtypes.remove(itemtypeid)

            itemtypeind = random.randint((0),(len(itemtypes)-1))
            itemtypeid = itemtypes[itemtypeind]
            sql = "INSERT INTO item VALUES (NULL, NULL, " + str(itemroomid2) + ", NULL, " + str(itemtypeid) + ", 0);"
            cur.execute(sql)

            if itemtypeid <= 9:
                sql = "UPDATE ITEMTYPE SET Created=1 WHERE ItemtypeID = " + str(itemtypeid) + ";"
                cur.execute(sql)
                itemtypes.remove(itemtypeid)

            #merchantin tavaroiden arpominen
            
            for i in range(0,2):
                itemtypeind = random.randint((0),(len(itemtypes)-1))
                itemtypeid = itemtypes[itemtypeind]
                sql = "INSERT INTO item VALUES (NULL, NULL, NULL, " + str(level) + ", " + str(itemtypeid) +", 0);"
                cur.execute(sql)
                
                if itemtypeid <= 9:
                    sql = "UPDATE ITEMTYPE SET Created=1 WHERE ItemtypeID = " + str(itemtypeid) + ";"
                    cur.execute(sql)
                    itemtypes.remove(itemtypeid)
        else:
            #tarvitaanko näitä ylärivejä???
            #sql = "SELECT itemtype.ItemtypeID FROM itemtype WHERE itemtypeID = 5 OR itemtypeID = 12;"
            #cur.execute(sql)
            #tempitemtypes = cur.fetchall()
            #for row in tempitemtypes:
                #itemtypes.append(row[0])
            sql = "INSERT INTO item VALUES (NULL, NULL, NULL, " + str(level) + ", 5, 0);"
            cur.execute(sql)
            sql = "INSERT INTO item VALUES (NULL, NULL, NULL, " + str(level) + ", 12, 0);"
            cur.execute(sql)
            print(itemtypes)
        
        #sitten arvotaan viholliset
        #ensin otetaan huone järjestyksessä, aloitetaan listan lopusta
        #sitten arvotaan, mikä vihollistyyppi huoneessa on
        #luodaan huoneeseen vihollinen

        while len(rooms) != 0:

            set_enemy()

            #30 prosenttiin huoneista tulee item!
            #ifitem = random.randint(1,10)
            #if ifitem <= 3:
                #set_item()

            del rooms[-1]

        #itemtypes.clear()
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

db.rollback()
db.close()
