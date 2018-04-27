DROP DATABASE IF EXISTS dankestdungeon;
CREATE DATABASE dankestdungeon;
USE dankestdungeon;

CREATE TABLE Room
(
  RoomID INT NOT NULL,
  Encounter BOOLEAN NOT NULL, #Marks whether the room has a random encounter
  Description VARCHAR(1000) NOT NULL,
  Level INT NOT NULL,
  PRIMARY KEY (RoomID)
);

CREATE TABLE EnemyType
(
  EnemytypeID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(1000) NOT NULL,
  Level INT NOT NULL,
  HitPoints INT NOT NULL,
  AttackPower INT NOT NULL,
  Description VARCHAR(1000) NOT NULL,
  Dialogue VARCHAR(255) NOT NULL,
  DeathDialogue VARCHAR(1000) NOT NULL,
  Riddle VARCHAR(1000) NOT NULL,
  isUnique BOOLEAN NOT NULL,
  Money INT NOT NULL,
  PRIMARY KEY (EnemytypeID)
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
  Name VARCHAR(1000) NOT NULL,
  Dialogue VARCHAR(1000) NOT NULL,
  Description VARCHAR(1000) NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (MerchantID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Trap
(
  TrapID INT NOT NULL AUTO_INCREMENT,
  Description VARCHAR(1000) NOT NULL,
  Active BOOLEAN NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (TrapID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Dialogue
(
  ID INT NOT NULL AUTO_INCREMENT,
  Dialogue VARCHAR(1000) NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE Itemtype
(
  ItemtypeID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(1000) NOT NULL,
  Description VARCHAR(1000) NOT NULL,
  AttackPower INT NOT NULL,
  HitPoints INT NOT NULL,
  Movable BOOLEAN NOT NULL,
  Type VARCHAR(1000) NOT NULL,
  Value INT NOT NULL,
  Created BOOLEAN NOT NULL,
  PRIMARY KEY (ItemtypeID)
);

CREATE TABLE Leads_to
(
  Direction VARCHAR(1000) NOT NULL,
  RoomID_1 INT NOT NULL,
  Leads_toRoomID_2 INT NOT NULL,
  PRIMARY KEY (RoomID_1, Leads_toRoomID_2),
  FOREIGN KEY (RoomID_1) REFERENCES Room(RoomID),
  FOREIGN KEY (Leads_toRoomID_2) REFERENCES Room(RoomID)
);

CREATE TABLE PlayerCharacter
(
  ID INT NOT NULL AUTO_INCREMENT,
  HitPoints INT NOT NULL,
  Inventorylimit INT NOT NULL,
  Money INT NOT NULL,
  Description VARCHAR(1000) NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Item
(
  ItemID INT NOT NULL AUTO_INCREMENT,
  ID INT,
  RoomID INT,
  MerchantID INT,
  ItemtypeID INT NOT NULL,
  PRIMARY KEY (ItemID),
  FOREIGN KEY (ID) REFERENCES PlayerCharacter(ID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
  FOREIGN KEY (MerchantID) REFERENCES Merchant(MerchantID),
  FOREIGN KEY (ItemtypeID) REFERENCES Itemtype(ItemtypeID)
);

#First level rooms and connections

INSERT INTO Room VALUES(1, 0,"This is the top most room in the Pyramid. The walls are covered with hieroglyphs: animals, vases, people, odd shapes, eyes watching...  It's magnificent and creepy. There's a stairway leading down.", 1); #Top Room
INSERT INTO Room VALUES(2, 1,"This room is a kind of an antechamber, an entrance way to the most sacred parts of the Pyramid. Lots of hieroglyphs on the limestone walls again... There's a stairway leading up.", 1); #Second row left
INSERT INTO Room VALUES(3, 1,"In this room there's a mural painting of a weighing scale and of a guy who has the head of a black scruffy dog. What's that drawn on the scales... a feather and a human heart... Eww. The stone stairs lead downwards.", 1); #Second row right - trap
INSERT INTO Room VALUES(4, 1,"This is the grand gallery. What a big room! The stone stairs lead upwards.", 1); #Third row middle
INSERT INTO Room VALUES(5, 1,"This must be the Queen's burial chamber. There's a huge, empty sarcophagus made of stone on the floor. And no, I shouldn't lie in it!", 1); #Third row right
INSERT INTO Room VALUES(6, 1,"Oh vow! Really nice decor here, probably the King's burial chamber. There's a spiral stairway going downwards.", 1); #Third row left - trap
INSERT INTO Room VALUES(7, 1,"Here is the biggest subterranean chamber. Still so many hieroglyphs everywhere... There's a spiral stairway going upwards.", 1); #Fourth row middle left
INSERT INTO Room VALUES(8, 1,"This room would make a great wine cellar, maybe it's been one in the olden day. But sadly no wine here.", 1); #Fourth row further left - trap
INSERT INTO Room VALUES(9, 0,"Yet another burial chamber, not as fancy as the others. Maybe it was for the pharaoh's distant cousin or something. There's a big ornamental door, where might that lead?", 1); #Fourth row middle right - sphinx
INSERT INTO Room VALUES(10, 0,"In this room there are just way too many hieroglyphs. Enough with the hieroglyphs already! There's a stairway going further and further down...", 1); #Fourth row further right - BOSS ROOM

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

INSERT INTO Room VALUES(11, 0,"Oh dear! This is obviously the middle room in a ruined Mayan Temple! The walls are covered with sculpted tablets depicting totemic animals. Maybe the treasure is in this room... Nope.", 2); #Middle room
INSERT INTO Room VALUES(12, 1,"This hall is an ancient indoor Mesoamerican ballcourt. It was easy to get a ball back then, just use a spare head!", 2); #North room
INSERT INTO Room VALUES(13, 1,"This is the obsidian room, the walls are decorated with blades of volcanic glass used by the Mayan people... wait, what? That's a real thing? I thought GRRM made that up!", 2); #North west room - button
INSERT INTO Room VALUES(14, 1,"This must be the Mayan kitchen. I'm not hungry though. There's an old wooden door. ", 2); #West room
INSERT INTO Room VALUES(15, 1,"A room for food storage, I assume. Lots of pictures of corn painted on the walls.", 2); #South west room - button
INSERT INTO Room VALUES(16, 1,"Oh, a balcony! A great view over the Guatemalan rainforests! ", 2); #South room
INSERT INTO Room VALUES(17, 1,"Lintels portraying Mayan Gods and animals are fastened on the walls of this room. I'll call this 'the lintel room'", 2); #South east room - button
INSERT INTO Room VALUES(18, 1,"A room full of pictures of animals on the walls. Again. I'm starting to see a pattern here. Again. There's also a hidden trap door. You cannot see it.", 2); #East room
INSERT INTO Room VALUES(19, 1,"The powder room! I've been looking for this as long as for the treasure!", 2); #North east - button
INSERT INTO Room VALUES(20, 0,"This is the hidden room.", 2); #Golden skull room
INSERT INTO Room VALUES(21, 0,"I'm in the altar room of the Mayan Temple now. The built-in altar is full of pictures of sacrificial animals (and sacrificial humans).", 2); #Boss room

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

INSERT INTO Room VALUES(22, 0,"Hold up! The walls are decorated from the floor up to the ceiling with bones, human bones. This is the foyer of the Catacombs.", 3); #Start room
INSERT INTO Room VALUES(23, 1,"They seem to be going for the same boney look in this dining room. I do like that collar bone, is it Scandinavian? Could I get that at Ikea?", 3); #Start room north
INSERT INTO Room VALUES(24, 1,"This is the skull room. The room's walls are covered with skulls. There's a bit of brain still left in that one.", 3); #Start room west
INSERT INTO Room VALUES(25, 1,"The rib room! I'm so hungry!", 3); #Start Room north west
INSERT INTO Room VALUES(26, 1,"There are lots of different bones in this room. Let's see: head, shoulders, knees, toes, knees, toes...", 3); #Middle room
INSERT INTO Room VALUES(27, 0,"The tooth room. They really should have been using fluoride toothpaste.", 3); #Squre room east
INSERT INTO Room VALUES(28, 1,"The phalange room. Phalange is a really weird word.", 3); #Squre room north east - anvil
INSERT INTO Room VALUES(29, 1,"The intermediate cuneiform bone room. Need I say more? There's also a door made of - surprise, surprise - bones.", 3); #Squre room north
INSERT INTO Room VALUES(30, 1,"The stapes room. The stapes is the smallest and lightest bone in the human body, I just looked it up on Wikipedia.", 3); #Squre room north west - key piece
INSERT INTO Room VALUES(31, 1,"This room's id number is 31. 31, for crying out loud! And there has been no sign of the effing treasure in this whole game! Just those golden items... wonder if they're worth anything?", 3); #Squre room west
INSERT INTO Room VALUES(32, 1,"The Room. Tommy Wiseau's 2003 film The Room has been repeatedly mentioned as one of the worst films ever made. Its main character is a banker called Johnny, played by Wiseau himself, who...", 3); #Squre room south west
INSERT INTO Room VALUES(33, 1,"The operating theatre. Unfortunately all the nice stuff like bone cutters and amputation saws have been taken away.", 3); #Squre room south
INSERT INTO Room VALUES(34, 1,"The bones-for-sale room. There's a sign on the wall saying: 'Come and get the best calf bones on the market! Half price, used only once, hardly any bite marks. Call 02-718 28 18 now!'", 3); #Squre room south east - key piece
INSERT INTO Room VALUES(35, 0,"The living room. Well, how many wannabe jokes is one supposed to be able to make about rooms and bones? Not that many, I agree.", 3); #Squre room middle - Golden Monkey
INSERT INTO Room VALUES(36, 0,"The ticket office. A large sign advertises that the Catacombs are open for public from 10 am to 6 pm and ticket prices range from 10 to 20 euros.", 3); #Boss room

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

INSERT INTO Room VALUES(37, 0, "An eery whisper, almost like a bark, echoes in the ominous dungeon... The smell of something sweet, rotten even, lingers in the stuffy air... There are cobwebs on the broken chains on the floor...  Something is moving in the next room... I have been teleported away from the Catacombs to the Dankest Dungeon... There's an enormous black door towering in front of me.", 4); #Dankest start
INSERT INTO Room VALUES(38, 0, "Wooow! Dang dude, da crib is phat yo!", 4); #Dankest boss

INSERT INTO Leads_to VALUES("E",37,38);

INSERT INTO playercharacter VALUES(NULL, 100, 10, 15, "Me, a humble treasure hunter.", 1);

INSERT INTO itemtype VALUES(NULL, "Dagger", "A basic blade to hit monsters with", 10, 0, 1, "weapon", 0, 1);
INSERT INTO itemtype VALUES(NULL, "Short sword", "A basic sword for hitting monsters", 13, 0, 1, "weapon", 100, 0);
INSERT INTO itemtype VALUES(NULL, "Medium sword", "Slightly better sword for hitting monsters", 18, 0, 1, "weapon", 200, 0);
INSERT INTO itemtype VALUES(NULL, "Long sword", "Clearly better sword for hitting monsters", 25, 0, 1, "weapon", 400, 0);
INSERT INTO itemtype VALUES(NULL, "Einhander", "Little brother of the Zweihander", 30, 0, 1, "weapon", 800, 0);

INSERT INTO itemtype VALUES(NULL, "Buckler", "Smallest little shield", 0, 80, 1, "shield", 100, 0);
INSERT INTO itemtype VALUES(NULL, "Small Shield", "Small little shield", 0, 100, 1, "shield", 150, 0);
INSERT INTO itemtype VALUES(NULL, "Shield", "Moderately sized shield", 0, 120, 1, "shield", 300, 0);
INSERT INTO itemtype VALUES(NULL, "Tower shield", "Using a tower as a shield, bold!", 0, 150, 1, "shield", 600, 0);

INSERT INTO itemtype VALUES(NULL, "Healing potion", "Small bottle filled with dark, red liquid. Heals to full health.", 0, 0, 1, "Potion", 100, 0);
INSERT INTO itemtype VALUES(NULL, "Damage potion", "Small bottle filled with grey liquid, smells awful. Increases combat prowess.", 20, 0, 1, "Potion", 500, 0);

INSERT INTO Itemtype VALUES(NULL, "Healing Scroll", "A Scroll containig esoteric knowledge. There is a picture of a red cross in the middle.", 0, 0, 1, "Scroll", 500, 0);
INSERT INTO Itemtype VALUES(NULL, "Water Scroll", "A Scroll containig esoteric knowledge. There is a picture of a tsunami in the middle.", 0, 0, 1, "Scroll", 500, 0);
INSERT INTO Itemtype VALUES(NULL, "Fire Scroll", "A Scroll containig esoteric knowledge. There is a picture of a fireball in the middle.", 0, 0, 1, "Scroll", 500, 0);

INSERT INTO Itemtype VALUES(NULL, "Golden ankh", "A curious treasure, pure gold. I can't help but feel this item is important", 0, 0, 1, "Golden", 4000, 1);
INSERT INTO Itemtype VALUES(NULL, "Golden skull", "A curious treasure, pure gold. I can't help but feel this item is important", 0, 0, 1, "Golden", 4000, 1);
INSERT INTO Itemtype VALUES(NULL, "Golden monkey", "A curious treasure, pure gold. I can't help but feel this item is important", 0, 0, 1, "Golden", 4000, 1);

INSERT INTO Itemtype VALUES(NULL, "Key piece", "It seems to be a half of a key", 0, 0, 1, "key", 0, 1);
INSERT INTO Itemtype VALUES(NULL, "Piece of a key", "It seems to be a half of a key", 0, 0, 1, "key", 0, 1);

INSERT INTO Itemtype VALUES(NULL, "Snake button", "It's a button with a picture of a snake. I feel compelled to push it", 0, 0, 0, "Button", 0, 1);
INSERT INTO Itemtype VALUES(NULL, "Jaquar button", "It's a button with a picture of a jaquar. I feel compelled to push it", 0, 0, 0, "Button", 0, 1);
INSERT INTO Itemtype VALUES(NULL, "Quetzal button", "It's a button with a picture of a quetzal. I feel compelled to push it", 0, 0, 0, "Button", 0, 1);
INSERT INTO Itemtype VALUES(NULL, "Butterfly button", "It's a button with a picture of a butterfly. I feel compelled to push it", 0, 0, 0, "Button", 0, 1);

INSERT INTO Item VALUES(NULL, 1, NULL, NULL, 1); #Put Dagger into player's inventory

INSERT INTO Item VALUES(NULL, NULL, 8, NULL, 15); #put golden items into their rooms
INSERT INTO Item VALUES(NULL, NULL, 20, NULL, 16);
INSERT INTO Item VALUES(NULL, NULL, 35, NULL, 17);

INSERT INTO Item VALUES(NULL, NULL, 34, NULL, 18); #put key pieces into their rooms
INSERT INTO Item VALUES(NULL, NULL, 30, NULL, 19);

INSERT INTO Item VALUES(NULL, NULL, 13, NULL, 20); #put buttons into their rooms
INSERT INTO Item VALUES(NULL, NULL, 15, NULL, 21);
INSERT INTO Item VALUES(NULL, NULL, 17, NULL, 22);
INSERT INTO Item VALUES(NULL, NULL, 19, NULL, 23);

#Level 1 enemytypes, Pyramid

INSERT INTO EnemyType VALUES(NULL, 'Scorpions', 1, 6, 1, "The black Scorpions are small, but menacing. Their grasping pedipalps open and close, and the venomous stingers at the end of their tails are curved forward, pointing straight at me... (Their hit points are 6, and attack power just 1.)", "Grrr", "Grr...rr..r","", 0, 1); #Scorpion
INSERT INTO EnemyType VALUES(NULL, 'Mummy Cat', 1, 14, 2, "Mummy Cat is licking its mummified, linen-wrapped paw, purring peacefully. Such a lovely cat! (Appearances can be deceiving, though: its hit points are 14 and attack power 2.)", "Meouw", "Meouuwww","",0, 2); #Mummy Cat
INSERT INTO EnemyType VALUES(NULL, 'Mummy', 1, 21, 5, "Mummy stands still in the corner. His hideous disfigured and odd-coloured corps is visible between the linen shreds wrapped around him. It is hard to understand that once he's been a human, too. But hey, looks aren't everything! (Hit points 21, attack power 5)", "Brainss....", "Too much sanddd..","", 0, 3); #Mummy
INSERT INTO EnemyType VALUES(NULL, 'Sphinx', 1, 31, 20, "Sphinx has the body of a lioness and the head of a beautiful woman. She is carved out of a huge monolith. She does seem a little... stoned... (However, don't make her angry: her hit points are 31, and attack power 20.)", "Hmmm what we have here...well answer my riddle correctly or die pathethic death.", "This wasen't supposed to happen...", "Who is the greatest rapper of all time?", 1, 5); #Sphinx
INSERT INTO EnemyType VALUES(NULL, 'Anubis', 1, 50, 10, "Anubis, the Jackal-headed God of the Dead, the Protector of Tombs, the Embalmer, the Guide of Souls, the Mother of Dragons, the Boss of the Pyramid... His strength is his jackal-like fighting, and his weakness is that he's scared of fireworks. (Hit points 50, attack power 10)", "You dare to challenge me...a mere mortal. Die you pathethic fool.", "What? How can you be so strong??? No mortal has ever defeated me.","", 1, 10); #Anubis

#Level 2 enemytypes, Mayan Temple

INSERT INTO EnemyType VALUES(NULL, 'Satanic Monkeys', 2, 14, 5, "The Satanic Monkeys make hideous noise, it annoys me. I want to silence them. (hit points 14 and attack power 5.)", "Oooh oooh ahh ahh", "ahh ahh oohh....", "", 0, 3); #Satanic Monkeys
INSERT INTO EnemyType VALUES(NULL, 'Fire Ant Colony', 2, 18, 7, "Oh no Fire Ant Colony is ahead of me. They look very nasty, don't let them bite or it will hurt like a lot. (hit points 18 and attack power 7.)", "skrttttt it's lit bois", "skrt...skr..t", "", 0, 4); #Fire Ant Colony
INSERT INTO EnemyType VALUES(NULL, 'Tiger', 2, 25, 10, "Tiger looks very angry. It looks like it's going to bite me. Watch out! (hit points 25 and attack power 10.)", "Rawwrr..", "Gr..rr","", 0, 5); #Tiger
INSERT INTO EnemyType VALUES(NULL, 'Cursed Mayan Soldiers', 2, 35, 12, "Cursed Mayan Soldies march ahead of me. They appear to be in serious pain, screaming like hell itself. (hit points 35 and attack power 12.)", "Aaaaah make it stop, the voices they don't stop...", "Thank you...oh thank you good adventurer.", "", 0, 6); #Cursed Mayan Soldiers
INSERT INTO EnemyType VAlUES(NULL, 'Mayan God', 2, 60, 15, "Mayan God Ah Puch looks at me. He smiles and starts to laugh. (I think he's impressed by me.. his hit points are 60 and attack power 15.)", "Haha..haa you litle ant destroyed all my minions. Well am I impressed, this is going to be fun fight. I am going to add you to my collection.", "Ha..ha..haa might I say, I am really impressed.", "", 1, 13); #Mayan God

#Level 3 enemytypes, Catacomb

INSERT INTO EnemyType VALUES(NULL, 'Blood Sucking Bats', 3, 22, 10, "Those bats look like they want blood. Don't let them suck it all or I'm going to be a mummy. (hit points 22 and attack power 10.)", "Brrrt brrtt..give blood.", "Brrrtt..", "", 0, 8); #Blood Sucking Bats
INSERT INTO EnemyType VALUES(NULL, 'Skeleton Warriors', 3, 28, 15, "Skeleton Warriors make nasty sounds when they walk. Bones hitting the catacombs floor gives me chills. Let the bodies now hit the floor! (hit points  28 and attack power 15.)", "Cling clang clung", "Clung cling", "", 0, 10); #Skeleton Warriors 
INSERT INTO EnemyType VALUES(NULL, 'Dead Warriors', 3, 45, 18, "Dead warriors, those who dare the lord were never given the peace in underworld and now they march in unrest ready to give their pain to others. (hit points 45 and attack power 18.)", "Kill kill more killing and maybe...no just kill.", "Nooooo...", "", 0, 14); #Dead Warriors
INSERT INTO EnemyType VALUES(NULL, 'Priest of The Underworld', 3, 100, 20, "Priest of the Underworld Pekka menacing priest who doesn't let the dead rest. Give him his death so he learns what death really means. (hit points 100 and attack power 20.)", "Well well well....I will make you my greatest undead soldier of all time. Now die for me!", "No I don't wanna die not like this....!", "", 1, 20); #Priest of The Underworld

#Level 3 enemytypes, Dankest Dungeon

INSERT INTO EnemyType VALUES(NULL, 'Snoop Dogg', 4, 140, 42, "Oh my god!! It's Snoop Dogg the Greatest rapper of all time. He looks pretty chill, how can that be? (He must be really stoned or drunk...) (His hit points are 140 and attack power 42.)", "When the pimp's in the crib ma. Drop it like it's hot. Drop it like it's hot. Drop it like it's hot.", "Damm you beat me now have this medal.", "", 1, 420); #Snoop Dogg

#Merchants

INSERT INTO Merchant VALUES(NULL,'',"Hey you over there! Do you wanna buy some sweet weapons that I have? For a low price it's all yours.", "Old looking fellow stares at me from the corner of the room. He seems to have something in his backbag. Looks like he is waving at me to come closer.", 5); #Level 1 merchant
INSERT INTO Merchant VALUES(NULL,'Mayan Monk', "Looks like you are lost young man do you wanna buy some sweets that I have in my monk bag?.", "I see an old Mayan monk in the room. He seems to be praying. Suddenly he notices me and takes a bag from his back.", 14); #Level 2 merchant
INSERT INTO Merchant VALUES(NULL,'Merchant', "Got some rare things on sale, stranger! ", "A strange man in a black trench-coat with a huge backbag is standing behind a desk filled with items. There is also a torch that is burning with a blue flame.", 26); #Level 3 merhcant
INSERT INTO Merchant VALUES(NULL,'Loyal Hound Man',"Ah you have reached the final boss. I suggest you buy some upgrades or my master is going to finish you with one hit. Wof wof.", "I see a man... no, it's a dog, no, it's a man. Well it doesn't matter, it seems like the houndman has something he wants me to know.", 37); #Level 4 merchant

#Put bosses into their rooms

INSERT INTO Enemy VALUES(NULL, (SELECT HitPoints FROM Enemytype WHERE Name = "Sphinx"), 9, 4);
INSERT INTO Enemy VALUES(NULL, (SELECT HitPoints FROM Enemytype WHERE Name = "Anubis"), 10, 5);
INSERT INTO Enemy VALUES(NULL, (SELECT HitPoints FROM Enemytype WHERE Name = "Mayan God"), 21, 10);
INSERT INTO Enemy VALUES(NULL, (SELECT HitPoints FROM Enemytype WHERE Name = "Priest of The Underworld"), 36, 14);
INSERT INTO Enemy VALUES(NULL, (SELECT HitPoints FROM Enemytype WHERE Name = "Snoop Dogg"), 38, 15);
