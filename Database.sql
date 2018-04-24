CREATE TABLE Room
(
  RoomID INT NOT NULL,
  Encounter BOOLEAN NOT NULL, --Marks wether the room has a random encounter
  Description VARACHAR(255) NOT NULL,
  Level INT NOT NULL,
  PRIMARY KEY (RoomID)
);

CREATE TABLE EnemyType
(
  EnemytypeID INT NOT NULL,
  Name VARCHAR(255) NOT NULL,
  Level INT NOT NULL,
  HitPoints INT NOT NULL,
  AttackPower INT NOT NULL,
  Description VARCHAR(255) NOT NULL,
  Dialogue VARCHAR(255) NOT NULL,
  DeathDialogue VARCHAR(255) NOT NULL,
  Riddle VARCHAR(255) NOT NULL,
  Unique BOOLEAN NOT NULL,
  Money INT NOT NULL,
  PRIMARY KEY (EnemytypeID)
);

CREATE TABLE Magic
(
  MagicID INT NOT NULL,
  Name VARCHAR(255) NOT NULL,
  Damage INT NOT NULL,
  Target VARCHAR(255) NOT NULL,
  Cooldown INT NOT NULL,
  PRIMARY KEY (MagicID)
);

CREATE TABLE Enemy
(
  EnemyID INT NOT NULL,
  Hitpoints INT NOT NULL,
  RoomID INT NOT NULL,
  EnemytypeID INT NOT NULL,
  PRIMARY KEY (EnemyID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
  FOREIGN KEY (EnemytypeID) REFERENCES EnemyType(EnemytypeID)
);

CREATE TABLE Merchant
(
  MerchantID INT NOT NULL,
  Name VARCHAR(255) NOT NULL,
  Dialogue VARCHAR(255) NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (MerchantID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Trap
(
  TrapID INT NOT NULL,
  Description VARCHAR(255) NOT NULL,
  Active BOOLEAN NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (TrapID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Dialogue
(
  ID INT NOT NULL,
  Dialogue VARCHAR(255) NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE Itemtype
(
  ItemtypeID INT NOT NULL,
  Name VARCHAR(255) NOT NULL,
  Description VARCHAR(255) NOT NULL,
  AttackPower INT NOT NULL,
  HitPoints INT NOT NULL,
  Movable BOOLEAN NOT NULL,
  Type VARCHAR(255) NOT NULL,
  Value INT NOT NULL,
  Exists BOOLEAN NOT NULL,
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
  ID INT NOT NULL,
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
  ItemID INT NOT NULL,
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
