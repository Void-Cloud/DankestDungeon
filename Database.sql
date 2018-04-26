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

#First level rooms and connections

INSERT INTO Room VALUES(1, 0,"Top Room", 1); #Top Room
INSERT INTO Room VALUES(2, 1,"Second row left", 1); #Second row left
INSERT INTO Room VALUES(3, 1,"Second row right - trap", 1); #Second row right - trap
INSERT INTO Room VALUES(4, 1,"Third row middle", 1); #Third row middle
INSERT INTO Room VALUES(5, 1,"Third row right", 1); #Third row right
INSERT INTO Room VALUES(6, 1,"Third row left - trap", 1); #Third row left - trap
INSERT INTO Room VALUES(7, 1,"Fourth row middle left", 1); #Fourth row middle left
INSERT INTO Room VALUES(8, 1,"Fourth row further left - trap", 1); #Fourth row further left - trap
INSERT INTO Room VALUES(9, 0,"Fourth row middle right - sphinx", 1); #Fourth row middle right - sphinx
INSERT INTO Room VALUES(10, 0,"Fourth row further right - BOSS ROOM", 1); #Fourth row further right - BOSS ROOM

INSERT INTO Leads_to VALUES("D",1,2); #Top Room -> Second row left
INSERT INTO Leads_to VALUES("U",2,1); #Second row left -> Top Room
INSERT INTO Leads_to VALUES("E",2,3); #Second row left -> Second row right
INSERT INTO Leads_to VALUES("W",3,2); #Second row right -> Second row left
INSERT INTO Leads_to VALUES("D",3,4); #Second row right -> Third row middle
INSERT INTO Leads_to VALUES("U",4,3);
INSERT INTO Leads_to VALUES("E",4,5);
INSERT INTO Leads_to VALUES("W",4,6);
INSERT INTO Leads_to VALUES("W",5,4);
INSERT INTO Leads_to VALUES("E",6,4);
INSERT INTO Leads_to VALUES("D",6,7);
INSERT INTO Leads_to VALUES("U",7,6);
INSERT INTO Leads_to VALUES("W",7,8);
INSERT INTO Leads_to VALUES("E",7,9);
INSERT INTO Leads_to VALUES("E",8,7);
INSERT INTO Leads_to VALUES("W",9,7);
INSERT INTO Leads_to VALUES("E",9,10);
INSERT INTO Leads_to VALUES("W",10,9);

#Second level rooms and connections

INSERT INTO Room VALUES(11, 0,"Middle room", 2); #Middle room
INSERT INTO Room VALUES(12, 1,"North room", 2); #North room
INSERT INTO Room VALUES(13, 1,"North west room", 2); #North west room - button
INSERT INTO Room VALUES(14, 1,"West room", 2); #West room
INSERT INTO Room VALUES(15, 1,"South west room", 2); #South west room - button
INSERT INTO Room VALUES(16, 1,"South room", 2); #South room
INSERT INTO Room VALUES(17, 1,"South east room", 2); #South east room - button
INSERT INTO Room VALUES(18, 1,"East room", 2); #East room
INSERT INTO Room VALUES(19, 1,"North east room", 2); #North east - button
INSERT INTO Room VALUES(20, 0,"Golden skull room", 2); #Golden skull room
INSERT INTO Room VALUES(21, 0,"Boss room", 2); #Boss room

INSERT INTO Leads_to VALUES("D",10,11);
INSERT INTO Leads_to VALUES("N",11,12);
INSERT INTO Leads_to VALUES("W",11,14);
INSERT INTO Leads_to VALUES("S",11,16);
INSERT INTO Leads_to VALUES("E",11,18);
INSERT INTO Leads_to VALUES("S",12,11);
INSERT INTO Leads_to VALUES("W",12,13);
INSERT INTO Leads_to VALUES("E",12,19);
INSERT INTO Leads_to VALUES("E",13,12);
INSERT INTO Leads_to VALUES("S",13,14);
INSERT INTO Leads_to VALUES("E",14,11);
INSERT INTO Leads_to VALUES("N",14,13);
INSERT INTO Leads_to VALUES("W",14,21); #locked
INSERT INTO Leads_to VALUES("S",14,15);
INSERT INTO Leads_to VALUES("N",15,14);
INSERT INTO Leads_to VALUES("E",15,16);
INSERT INTO Leads_to VALUES("W",16,15);
INSERT INTO Leads_to VALUES("N",16,11);
INSERT INTO Leads_to VALUES("E",16,17);
INSERT INTO Leads_to VALUES("W",17,16);
INSERT INTO Leads_to VALUES("N",17,18);
INSERT INTO Leads_to VALUES("W",18,11);
INSERT INTO Leads_to VALUES("S",18,17);
INSERT INTO Leads_to VALUES("E",18,20); #locked
INSERT INTO Leads_to VALUES("N",18,19);
INSERT INTO Leads_to VALUES("S",19,18);
INSERT INTO Leads_to VALUES("W",19,12);
INSERT INTO Leads_to VALUES("W",20,18);
INSERT INTO Leads_to VALUES("E",21,14);

#third level rooms and connections

INSERT INTO Room VALUES(22, 0,"Start Room", 3); #Start room
INSERT INTO Room VALUES(23, 1,"Start room north", 3); #Start room north
INSERT INTO Room VALUES(24, 1,"Start room west", 3); #Start room west
INSERT INTO Room VALUES(25, 1,"Start room NW", 3); #Start Room north west
INSERT INTO Room VALUES(26, 1,"Middle room", 3); #Middle room
INSERT INTO Room VALUES(27, 0,"Squre room east", 3); #Squre room east
INSERT INTO Room VALUES(28, 1,"Squre room north east", 3); #Squre room north east - anvil
INSERT INTO Room VALUES(29, 1,"Squre room north", 3); #Squre room north
INSERT INTO Room VALUES(30, 1,"Squre room north west", 3); #Squre room north west - key piece
INSERT INTO Room VALUES(31, 1,"Squre room west", 3); #Squre room west
INSERT INTO Room VALUES(32, 1,"Squre room south west", 3); #Squre room south west
INSERT INTO Room VALUES(33, 1,"Squre room south", 3); #Squre room south
INSERT INTO Room VALUES(34, 1,"Squre room south east", 3); #Squre room south east - key piece
INSERT INTO Room VALUES(35, 0,"Squre room middle", 3); #Squre room middle - Golden Monkey
INSERT INTO Room VALUES(36, 0,"Boss room", 3); #Boss room

INSERT INTO Leads_to VALUES("D",21,22);
INSERT INTO Leads_to VALUES("N",22,23);
INSERT INTO Leads_to VALUES("W",22,24);
INSERT INTO Leads_to VALUES("S",23,22);
INSERT INTO Leads_to VALUES("W",23,25);
INSERT INTO Leads_to VALUES("E",24,22);
INSERT INTO Leads_to VALUES("N",24,25);
INSERT INTO Leads_to VALUES("E",25,23);
INSERT INTO Leads_to VALUES("S",25,24);
INSERT INTO Leads_to VALUES("W",25,26);
INSERT INTO Leads_to VALUES("E",26,25);
INSERT INTO Leads_to VALUES("W",26,27);
INSERT INTO Leads_to VALUES("E",27,26);
INSERT INTO Leads_to VALUES("W",27,35);
INSERT INTO Leads_to VALUES("S",27,34);
INSERT INTO Leads_to VALUES("N",27,28);
INSERT INTO Leads_to VALUES("S",28,27);
INSERT INTO Leads_to VALUES("W",28,29);
INSERT INTO Leads_to VALUES("E",29,28);
INSERT INTO Leads_to VALUES("N",29,36); #locked
INSERT INTO Leads_to VALUES("S",29,35);
INSERT INTO Leads_to VALUES("W",29,30);
INSERT INTO Leads_to VALUES("E",30,29);
INSERT INTO Leads_to VALUES("S",30,31);
INSERT INTO Leads_to VALUES("N",31,30);
INSERT INTO Leads_to VALUES("E",31,35);
INSERT INTO Leads_to VALUES("S",31,32);
INSERT INTO Leads_to VALUES("N",32,31);
INSERT INTO Leads_to VALUES("E",32,33);
INSERT INTO Leads_to VALUES("W",33,32);
INSERT INTO Leads_to VALUES("N",33,35);
INSERT INTO Leads_to VALUES("E",33,34);
INSERT INTO Leads_to VALUES("W",34,33);
INSERT INTO Leads_to VALUES("N",34,27);
INSERT INTO Leads_to VALUES("N",35,29);
INSERT INTO Leads_to VALUES("W",35,31);
INSERT INTO Leads_to VALUES("S",35,33);
INSERT INTO Leads_to VALUES("E",35,27);

#Dankest dungeon

INSERT INTO Room VALUES(37, 0, "Dankest start", 4); #Dankest start
INSERT INTO Room VALUES(38, 0, "Dankest boss", 4); #Dankest boss

INSERT INTO Leads_to VALUES("E",37,38);

#Level 1 enemytypes, Pyramid

INSERT INTO EnemyType VALUES(NULL, 'Scorpions', 1, 6, 1, 'The black Scorpions are small, but menacing. Their grasping pedipalps open and close, and the venomous stingers at the end of their tails are curved forward, pointing straight at you... (Their hit points are 6, and attack power just 1.)', 'Grrr', 'Grr...rr..r','', 0, 1); #Scorpion
INSERT INTO EnemyType VALUES(NULL, 'Mummy Cat', 1, 14, 2, 'Mummy Cat is licking its mummified, linen-wrapped paw, purring peacefully. Such a lovely cat! (Appearances can be deceiving, though: its hit points are 14 and attack power 2.)', 'Meouw', 'Meouuwww','',0, 2); #Mummy Cat
INSERT INTO EnemyType VALUES(NULL, 'Mummy', 1, 21, 5, 'The Mummy stands still in the corner. His hideous disfigured and odd-coloured corps is visible between the linen shreds wrapped around him. It is hard to understand that once he's been a human, too. But hey, looks aren't everything! (Hit points 21, attack power 5)', 'Brainss....', 'Too much sanddd..','', 0, 3); #Mummy
INSERT INTO EnemyType VALUES(NULL, 'Sphinx', 1, 31, 20, 'Sphinx has the body of a lioness and the head of a beautiful woman. She is carved out of a huge monolith. She does seem a little... stoned... (However, don't make her angry: her hit points are 31, and attack power 20.)', 'Hmmm what we have here...well answer my riddle correctly or die pathethic death.', 'This wasen't supposed to happen...', 'Who is the greatest rapper of all time?', 1, 5); #Sphinx
INSERT INTO EnemyType VALUES(NULL, 'Anubis', 1, 50, 10, 'Anubis, the Jackal-headed God of the Dead, the Protector of Tombs, the Embalmer, the Mother of Dragons, the Guide of Souls... His strength is his jackal-like fighting, and his weakness is that he's scared of fireworks. (Hit points 50, attack power 10)', 'You dare to challenge me...a mere mortal. Die you pathethic fool.', 'What how can you be so strong??? No mortal has ever defeated me.','', 1, 10); #Anubis

#Level 2 enemytypes, Mayan Temple

INSERT INTO EnemyType VALUES(NULL, 'Satanic Monkeys', 2, 14, 5, 'The Satanic Monkeys make hideorous noise, it annoys you. You wan't to silence them. (hit points 14 and attack power 5.)', 'oooh oooh ahh ahh', 'ahh ahh oohh....', '', 0, 3); #Satanic Monkeys
INSERT INTO EnemyType VALUES(NULL, 'Fire Ant Colony', 2, 18, 7, 'Oh no Fire Ant Colony is in head of you. They look very nasty, don't let them bite you or it will hurt like a lot. (hit points 18 and attack power 7.)', 'skrttttt it's lit bois', 'skrt...skr..t', '', 0, 4); #Fire Ant Colony
INSERT INTO EnemyType VALUES(NULL, 'Tiger', 2, 25, 10, 'Tiger looks very angry. It looks like it's going to bite you. Watch out! (hit points 25 and attack power 10.)', 'Rawwrr..', 'Gr..rr','', 0, 5); #Tiger
INSERT INTO EnemyType VALUES(NULL, 'Cursed Mayan Soldiers', 2, 35, 12, 'Cursed Mayan Soldies march in head of you. They appear to be in serious pain, screaming like hell it self. (hit points 35 and attack power 12.)', 'Aaaaah make it stop, the voices they don't stop...', 'Thank you...oh thank you good adventurer.', '', 0, 6); #Cursed Mayan Soldiers
INSERT INTO EnemyType VAlUES(NULL, 'Mayan God', 2, 60, 15, 'Mayan God Ah Puch looks at you. He smiles and starts to laugh. (I think he's impressed on you.. hes hit points are 60 and attack power 15.)', 'Haha..haa you litle ant destroyed all my minions. Well am I impressed, this is going to be fun fight. I am going to add you to my collection.', 'Ha..ha..haa might I say, I am really impressed.', '', 1, 13); #Mayan God

#Level 3 enemytypes, Catacomb

INSERT INTO EnemyType VALUES(NULL, 'Blood Sucking Bats', 3, 22, 10, 'Those bats look like they wan't blood. Don't let them suck it all or your going to be a mummy. (hit points 22 and attack power 10.)', 'Brrrt brrtt..give blood.', 'Brrrtt..', '', 0, 8); #Blood Sucking Bats
INSERT INTO EnemyType VALUES(NULL, 'Skeleton Warriors', 3, 28, 15, 'Skeleton Warriors make nasty sounds when they walk. Bones hitting the catacombs floor gives you chills. Let the bodies now hit the floor! (hit points  28 and attack power 15.)', 'Cling clang clung', 'Clung cling', '', 0, 10); #Skeleton Warriors 
INSERT INTO EnemyType VALUES(NULL, 'Dead Warriors', 3, 45, 18, 'Dead warriors, those who dare the lord where never given the peace in underworld and now they march in unreast ready to give theyr paint to others. (hit points 45 and attack power 18.)', 'Kill kill more killing and maybe...no just kill.', 'Nooooo...', '', 0, 14); #Dead Warriors
INSERT INTO EnemyType VALUES(NULL, 'Priest of The Underworld', 3, 100, 18, 'Priest of the Underworld Pekka menacing priest who doesn't let the death rest. Give him hes death so he learns what death really means. (hit points 100 and attack power 20.)', 'Well well well....I will make you my greatest undead soldier of all time. Now die for me!', 'No I don't wanna die not like this....!', '', 1, 20); #Priest of The Underworld

#Level 3 enemytypes, Dankest Dungeon

INSERT INTO EnemyType VALUES(NULL, 'Snoop Dogg', 4, 100, 42, 'Oh my god!! It's Snoop Dogg the Greatest rapper of all time. He looks pretty chill, how can that be? (He must be really stoned or drunk...) (Hes hit points are 140 and attack power 42.)', 'When the pimp's in the crib ma. Drop it like it's hot. Drop it like it's hot. Drop it like it's hot.', 'Damm you beat me now have this medal.', '', 1, 420); #Snoop Dogg

