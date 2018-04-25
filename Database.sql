DROP DATABASE IF EXISTS dankestdungeon;
CREATE DATABASE dankestdungeon;
USE dankestdungeon;

CREATE TABLE Room
(
  RoomID INT NOT NULL,
  Encounter BOOLEAN NOT NULL, #Marks whether the room has a random encounter
  Description VARCHAR(255) NOT NULL,
  Level INT NOT NULL,
  PRIMARY KEY (RoomID)
);

CREATE TABLE EnemyType
(
  EnemytypeID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  Level INT NOT NULL,
  HitPoints INT NOT NULL,
  AttackPower INT NOT NULL,
  Description VARCHAR(255) NOT NULL,
  Dialogue VARCHAR(255) NOT NULL,
  DeathDialogue VARCHAR(255) NOT NULL,
  Riddle VARCHAR(255) NOT NULL,
  isUnique BOOLEAN NOT NULL,
  Money INT NOT NULL,
  PRIMARY KEY (EnemytypeID)
);

CREATE TABLE Magic
(
  MagicID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  Damage INT NOT NULL,
  Target VARCHAR(255) NOT NULL,
  Cooldown INT NOT NULL,
  PRIMARY KEY (MagicID)
);

CREATE TABLE Enemy
(
  EnemyID INT NOT NULL AUTO_INCREMENT,
  Hitpoints INT NOT NULL,
  RoomID INT NOT NULL,
  EnemytypeID INT NOT NULL,
  PRIMARY KEY (EnemyID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
  FOREIGN KEY (EnemytypeID) REFERENCES EnemyType(EnemytypeID)
);

CREATE TABLE Merchant
(
  MerchantID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  Dialogue VARCHAR(255) NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (MerchantID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Trap
(
  TrapID INT NOT NULL AUTO_INCREMENT,
  Description VARCHAR(255) NOT NULL,
  Active BOOLEAN NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (TrapID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Dialogue
(
  ID INT NOT NULL AUTO_INCREMENT,
  Dialogue VARCHAR(255) NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE Itemtype
(
  ItemtypeID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  Description VARCHAR(255) NOT NULL,
  AttackPower INT NOT NULL,
  HitPoints INT NOT NULL,
  Movable BOOLEAN NOT NULL,
  Type VARCHAR(255) NOT NULL,
  Value INT NOT NULL,
  Created BOOLEAN NOT NULL,
  PRIMARY KEY (ItemtypeID)
);

CREATE TABLE Can_cast
(
  EnemytypeID INT NOT NULL,
  MagicID INT NOT NULL,
  PRIMARY KEY (EnemytypeID, MagicID),
  FOREIGN KEY (EnemytypeID) REFERENCES EnemyType(EnemytypeID),
  FOREIGN KEY (MagicID) REFERENCES Magic(MagicID)
);

CREATE TABLE Leads_to
(
  Direction VARCHAR(255) NOT NULL,
  RoomID_1 INT NOT NULL,
  Leads_toRoomID_2 INT NOT NULL,
  PRIMARY KEY (RoomID_1, Leads_toRoomID_2),
  FOREIGN KEY (RoomID_1) REFERENCES Room(RoomID),
  FOREIGN KEY (Leads_toRoomID_2) REFERENCES Room(RoomID)
);

CREATE TABLE PlayerCharater
(
  ID INT NOT NULL AUTO_INCREMENT,
  HitPoints INT NOT NULL,
  Inventorylimit INT NOT NULL,
  Money INT NOT NULL,
  Description VARCHAR(255) NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Item
(
  ItemID INT NOT NULL AUTO_INCREMENT,
  ID INT,
  RoomID INT,
  MagicID INT,
  MerchantID INT,
  ItemtypeID INT NOT NULL,
  PRIMARY KEY (ItemID),
  FOREIGN KEY (ID) REFERENCES PlayerCharater(ID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
  FOREIGN KEY (MagicID) REFERENCES Magic(MagicID),
  FOREIGN KEY (MerchantID) REFERENCES Merchant(MerchantID),
  FOREIGN KEY (ItemtypeID) REFERENCES Itemtype(ItemtypeID)
);

#Ensimmäinen kerros ja huoneet

INSERT INTO Room VALUES(1, 0,"Top Room", 1);
INSERT INTO Room VALUES(2, 1,"Second row left", 1);
INSERT INTO Room VALUES(3, 1,"Second row right - trap", 1);
INSERT INTO Room VALUES(4, 1,"Third row middle", 1);
INSERT INTO Room VALUES(5, 1,"Third row right", 1);
INSERT INTO Room VALUES(6, 1,"Third row left - trap", 1);
INSERT INTO Room VALUES(7, 1,"Fourth row middle left", 1);
INSERT INTO Room VALUES(8, 1,"Fourth row further left - trap", 1);
INSERT INTO Room VALUES(9, 0,"Fourth row middle right - sphinx", 1);
INSERT INTO Room VALUES(10, 0,"Fourth row further right - BOSS ROOM", 1);

INSERT INTO Leads_to VALUES("D",1,2);
INSERT INTO Leads_to VALUES("U",2,1);
INSERT INTO Leads_to VALUES("E",2,3);
INSERT INTO Leads_to VALUES("W",3,2);
INSERT INTO Leads_to VALUES("D",3,4);
INSERT INTO Leads_to VALUES("U",4,3);
INSERT INTO Leads_to VALUES("E",4,5);
INSERT INTO Leads_to VALUES("W",5,4);
INSERT INTO Leads_to VALUES("W",4,6);
INSERT INTO Leads_to VALUES("E",6,4);
INSERT INTO Leads_to VALUES("D",6,7);
INSERT INTO Leads_to VALUES("U",7,6);
INSERT INTO Leads_to VALUES("W",7,8);
INSERT INTO Leads_to VALUES("E",8,7);
INSERT INTO Leads_to VALUES("E",7,9);
INSERT INTO Leads_to VALUES("W",9,7);
INSERT INTO Leads_to VALUES("E",9,10);
INSERT INTO Leads_to VALUES("W",10,9);
