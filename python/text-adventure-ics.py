#############################
## Basic Text Adventure
## zihoffman7
## Oct 29, 2020

# Used to choose random element out of list
import random

# Player class
class player:
  def __init__(self, name):
    self.name = name
    self.weapon = weapon()
    self.armor = armor()
    self.shield = False
    self.healing = 0
    self.hp = 20
  # Takes damage depending on armor stats
  def damage(self, hp):
    prot = random.choice(self.armor.prot)
    damage = int(hp / prot)
    self.hp += damage
    return prot, -1 * damage
  # Executes attack
  def attack(self, attackType):
    if attackType == "jab":
      attack = random.choice(list(self.weapon.jab.items()))
      return attack[0], attack[1]
    attack = random.choice(list(self.weapon.damage.items()))
    return attack[0], attack[1]
  # Heals to full health
  def heal(self):
    if self.healing > 0:
      self.hp = 20
      print("\nYou healed to full HP")
      self.healing -= 1
    else:
      print("\nYou don't have any healing\n")

# Weapon class for player
class weapon:
  # Default
  def __init__(self):
    self.damage = {"missed" : 0, "hit" : 1, "hit" : 1, "critically hit" : 2}
    self.jab = {"missed" : 0, "critically hit" : 2}
    self.name = "Fist"
  # Upgrade
  def upgrade(self, damage, jab, name):
    self.damage = damage
    self.jab = jab
    self.name = name

# Armor class for player
class armor:
  # Default
  def __init__(self):
    self.prot = [1]
    self.name = "None"
  # Upgrade
  def upgrade(self, prot, name):
    self.prot = prot
    self.name = name

# Class for all enemies
class enemy:
  def __init__(self, hp, name, damages, prot=[1]):
    self.name = name.capitalize()
    self.hp = hp
    self.moves = damages
    self.prot = prot
  # Takes damage depending on armor stats
  def damage(self, hp):
    prot = random.choice(self.prot)
    damage = int(hp / prot)
    self.hp += damage
    return prot, -1 * damage
  # Executes attack
  def attack(self):
    attack = random.choice(list(self.moves.items()))
    return attack[0], attack[1]

def check(boolean):
  while True:
    if input("(a) next\n> ") == 'a':
      return boolean

def hasShield(player):
  if player.shield == True:
    return "\n(c) shield\n> "
  else:
    return "\n> "

# Player attack
def playerAttack(player, enemy):
  global shielded
  shielded = False
  text = "(a) swing\n(b) jab" + hasShield(player)
  while True:
    userInput = input(text).lower()
    if userInput == 'h':
      print("\nCan't heal during battle!\n")
    if userInput == 'a' or userInput == 'b':
      print(''.join('\n' * 30))
      # Do jab attack
      if userInput == 'b':
        damage = player.attack("jab")
        # Do swing attack
      else:
        damage = player.attack("swing")
      print("You " + damage[0], "the", enemy.name + "!\n")
      armoredDamage = enemy.damage(-1 * damage[1])
      # If enemy does damage and armor protects, show protection message
      if damage[1] > 0 and armoredDamage[0] > 1:
        print("Their armor tanks the damage so they only take", str(armoredDamage[1]), "damage point(s)!\n")
      else:
        print("You deal " + str(damage[1]) + " damage point(s)\n")
      # If enemy is dead, exit with True
      if enemy.hp <= 0:
        print(enemy.name + " defeated!\n")
        return check(True)
      print(enemy.name + " new hp: " + str(enemy.hp))
      print("----------------")
      break
    elif userInput == 'e':
      print("\nCan't access inventory now\n")
    elif userInput == 'r':
      start()
    elif userInput == 'c' and player.shield == True:
      shielded = True
      break

# Enemy attack
def enemyAttack(player, enemy):
  global shielded
  while True:
    if shielded == True:
      print("\nYou shielded and successfully blocked the " + enemy.name.lower() + "'s attack.\n")
      break
    userInput = input("(a or b) next\n> ").lower()
    if userInput == 'a' or userInput == 'b':
      print(''.join('\n' * 30))
      damage = enemy.attack()
      print("The", enemy.name, damage[0] + " you!\n")
      armoredDamage = player.damage(-1 * damage[1])
      # If player does damage and armor protects, show protection message
      if damage[1] > 0 and armoredDamage[0] > 1:
        print("Your armor tanks the damage so you only take", str(armoredDamage[1]), "damage!\n")
      else:
        print("The", enemy.name, "does", str(damage[1]) + " damage point(s)\n")
        # If player is dead, exit with False
      if player.hp <= 0:
        print(player.name + " defeated!\n")
        return check(False)
      print(player.name + " new hp: " + str(player.hp))
      print("----------------")
      break

# Runs player vs enemy battle
def battle(player, enemy):
  battleText = "\n(a) Begin " + enemy.name.lower() + " battle\n"
  try:
    if user.healing > 0 and battleText.find("(h)") < 0:
      battleText += "(h) heal\n> "
    else:
      battleText += "> "
  except:
    battleText += "> "
  if input(battleText) == 'h':
    user.heal()
  if player.shield:
    print("\nSwing - Accurate attack, chance for critical hit\nJab - 50% chance for critical hit and for no damage at all\nShield - Block the enemies attack, but it counts as your attack\n")
  else:
     print("\nSwing - Accurate attack, chance for critical hit\nJab - 50% chance for critical hit and for no damage at all\n")
  # Runs battle until someone wins
  while True:
    if playerAttack(player, enemy) == True:
      return True
    else:
      if enemyAttack(player, enemy) == False:
        return False

# Gets user input, reroutes to new story function
def master(options, text, functions):
  validInput = False
  # Will rerun until user gives valid input
  while not validInput:
    try:
      if user.healing > 0 and text.find("(h)") < 0:
        text += "(h) heal\n"
    except:
      pass
    selection = input(text + "> ").strip().lower()
    # If valid response, do corresponding reroute function
    if selection in options:
      validInput = True
      functions[options.index(selection)]()
    elif selection == 'h':
      user.heal()
    # Shows inventory if prompted
    elif selection == 'e':
      print(''.join('\n' * 30))
      print("\nInventory\n\nName: " + user.name + "\nWeapon: " + user.weapon.name + "\nAvg Damage: " + str(sum(user.weapon.damage.values())/len(user.weapon.damage.values())) + " hp\nArmor: " + user.armor.name + "\nAvg Protection: " + str(sum(user.armor.prot)/len(user.armor.prot))+ "\nShield: " + str(user.shield) + "\nHP: " + str(user.hp) + "/20\nHealing: " + str(user.healing) + '\n')
    # restarts
    elif selection == 'r':
      start()
    elif selection == 'm':
      menu()
    # If invalid input, will notify user an rerun loop
    else:
      print("Invalid character")

def menu():
  global user
  master(["a", "b"], "\nChoose a game mode\n(a) Adventure mode\n(b) Boss run\n", [start, bossRun])

# Starts the game
def start():
  global user
  user = player(input("\nEnter your name\n> "))
  print("\nWelcome " + user.name + "\n\nClick 'e' at any time to view inventory\nClick 'r' to restart\nClick 'm' for the main menu\n\nYou wake up in a jungle.  What do you do?\n")
  master(["a", "b"], "(a) Search for shelter\n(b) Search for food\n(e) inventory\n", [searchShelter, searchFood])

# All game possibilities below
def searchShelter():
  global user
  print("\nYou encounter a snake!")
  snake = enemy(4, "snake", {"missed" : 0, "bit you" : 1, "bit you" : 1, "poisoned you" : 3})
  results = battle(user, snake)
  if results == True:
    print("\nIt turns out the snake was guarding a sword\n\nYou aquire a basic sword (click e to view inventory)\n")
    user.weapon.upgrade({"missed" : 0, "hit" : 1, "struck" : 2, "struck" : 2, "critically hit" : 3}, {"missed" : 0, "critically hit" : 3}, "Longsword")
    master(["a"], "(a) Progress along path\n(e) inventory\n", [fork])
  else:
    print("\nYou loose!")
    gameOver()

def searchFood():
  global user
  print("\nYou encounter a hawk!")
  hawk = enemy(4, "hawk", {"missed" : 0, "bit you" : 1, "bit you" : 1, "dived on you" : 3})
  results = battle(user, hawk)
  if results == True:
    print("\nIt turns out the hawk was guarding some armor\n\nYou aquire leather armor (click e to view inventory)\n")
    user.armor.upgrade([1, 2, 2, 3], "Leather Armor")
    master(["a"], "(a) Progress along path\n(e) inventory\n", [fork])
  else:
    print("\nYou loose!")
    gameOver()

def fork():
  global user
  if user.shield == False:
    print("\nYou aquire a shield!\n")
    user.shield = True
  print("You encounter a fork in the road.  Which direction?")
  master(["a", "b", "c"], "(a) Left\n(b) Middle\n(c) Right\n(e) inventory\n", [left, middle, right])

def left():
  global user
  print("\nYou encounter an angry ogre!")
  ogre = enemy(10, "ogre", {"missed" : 0, "struck" : 1, "punched" : 2, "hit" : 3, "critically hit" : 4})
  results = battle(user, ogre)
  if results == True:
    print("\nYou take the ogre's armor\n\nYou aquire chain armor (click e to view inventory)\n")
    user.armor.upgrade([1, 2, 3, 4, 5], "Chain Armor")
    master(["a"], "(a) Progress along path\n(e) inventory\n", [toTower])
  else:
    print("\nYou loose!")
    gameOver()

def middle():
  print("\nYou encounter a lush ravine.")
  master(["a", "b"], "(a) Try to jump across\n(b) Go back\n(e) inventory\n", [jump, fork])

def jump():
  print("You overestimate your jumping skills and plummet to your death.")
  gameOver()

def right():
  global user
  print("You encounter an angry ogre!")
  ogre = enemy(10, "ogre", {"missed" : 0, "punched" : 2, "punched" : 2, "hit" : 3, "critically hit" : 4})
  results = battle(user, ogre)
  if results == True:
    print("\nYou take the ogre's weapon\n\nYou aquire a mace  (click e to view inventory)\n")
    user.weapon.upgrade({"got a weak hit on" : 1, "hit" : 2, "struck" : 3, "struck" : 3, "critically hit" : 4}, {"missed" : 0, "critically hit" : 5}, "Mace")
    master(["a"], "(a) Progress along path\n(e) inventory\n", [toCastle])
  else:
    print("\nYou loose!")
    gameOver()

def toTower():
  global user
  print("You aquire healing (click 'h' to heal)\n")
  user.healing += 1
  print("You approach a tower")
  master(["a", "b"], "(a) Climb to the top\n(b) Go inside\n(e) inventory\n", [climb, into])

def climb():
  print("You successfully scale the tower\n")
  topOfTower()

def into():
  print("You enter the tower\n\nInside of the tower, there is a massive armored skeleton")
  skeleton = enemy(15, "Armored Skeleton", {"missed" : 0, "punched" : 2, "struck" : 3, "stomped on" : 4, "critically hit" : 6})
  results = battle(user, skeleton)
  if results == True:
    print("\nYou take the skeleton's armor\n\nYou aquire plate armor (click e to view inventory)\n")
    user.armor.upgrade([2, 3, 4, 5, 6], "Plate Armor")
    master(["a"], "(a) Leave tower\n(e) inventory\n", [leaveTower])
  else:
    print("\nYou loose!")
    gameOver()

def topOfTower():
  print("You aquire an worn pair of plate armor\n")
  user.armor.upgrade([1, 3, 4, 4, 5], "Old Plate Armor")
  jumpTower()

def jumpTower():
  print("How do you get down from the tower?")
  master(["a", "b", "c"], "(a) Jump into lake below\n(b) Climb down\n(c) Drop through skylight into tower\n(e) inventory\n", [toLake, climbDown, into])

def toLake():
  global user
  user.hp -= 3
  if user.hp < 1:
    print("You died upon impact")
    gameOver()
  print("You jump down successfully, but loose 3 hp on impact\n")
  master(["a"], "(a) Continue along path\n(e) inventory\n", [leaveTower])

def climbDown():
  print("You slip and plummet to your death")
  gameOver()

def leaveTower():
  print("\nYou approach a heavily armored ogre")
  ArmoredOgre = enemy(10, "Armored Ogre", {"missed" : 0, "hit" : 3, "struck" : 4, "sword-attacked" : 5, "critically hit" : 8}, [1, 1, 2])
  results = battle(user, ArmoredOgre)
  if results == True:
    print("\nYou take the ogre's sword\n\nYou aquire a katana (click e to view inventory)\n")
    user.weapon.upgrade({"got a weak hit on" : 2, "struck" : 3, "attacked" : 4, "sliced" : 5, "critically hit" : 6}, {"missed" : 0, "critically hit" : 8}, "Katana")
    master(["a"], "(a) Progress along path\n(e) inventory\n", [toCastle])
  else:
    print("\nYou loose!")
    gameOver()

def toCastle():
  global user
  print("You aquire healing (click 'h' to heal)\n")
  user.healing += 1
  print("You approach a castle")
  master(["a", "b"], "(a) Knock on door\n(b) Try to break down door\n(e) inventory\n", [knockDoor, breakDoor])

def knockDoor():
  print("\nSomehow, the door opens.\nInside is a massive serpent.\n")
  master(["a"], "(a) Fight\n(e) inventory\n", [fightSerpent])

def fightSerpent():
  serpent = enemy(25, "Serpent", {"missed" : 0, "bit" : 4, "poisoned" : 7, "whipped" : 11, "critically hit" : 15})
  results = battle(user, serpent)
  if results == True:
    print("\nThe serpent was guarding a door\n")
    master(["a"], "(a) Go in door\n(e) inventory\n", [goIn])
  else:
    print("\nYou loose!")
    gameOver()

def goIn():
  print("\nInside, there is a shiny sword plated with jewels.")
  master(["a"], "(a) Take the sword\n(e) inventory\n", [takeSword])

def takeSword():
    print("\nYou aquire a shiny jewled sword (click e to view inventory)\n")
    user.weapon.upgrade({"got a weak hit on" : 2, "struck" : 4, "attacked" : 5, "sliced" : 6, "critically hit" : 7}, {"missed" : 0, "critically hit" : 9}, "Gem Sword")
    master(["a"], "(a) Proceed to next room\n(e) inventory\n", [secRoom])

def breakDoor():
  print("You break your wrist trying to hit down the door.  -3 hp")
  user.hp -= 3
  knockDoor()

def secRoom():
  global user
  print("\nYou aquire healing (click 'h' to heal)\n")
  user.healing += 1
  print("Inside of the next room is an armed man.  He wears shiny golden armor and weilds a very extravagant sword.\n")
  master(["a", "b"], "(a) Fight\n(b) Talk\n(e) inventory\n", [finalFight, talk])

def talk():
  print("\nThe man is the king.  He is mad that you killed his serpent.\nYou try to reason with him, but nothing works.\n")
  master(["a"], "(a) Fight\n(e) inventory\n", [finalFight])

def finalFight():
  king = enemy(20, "King", {"got a weak hit on" : 3, "struck" : 4, "attacked" : 5, "sliced" : 5, "critically hit" : 8}, [2, 3, 4, 4, 8])
  results = battle(user, king)
  if results == True:
    print("You have defeated the king.\n")
    master(["a", "b"], "(a) Take his gear\n(b) Leave his gear\n(e) inventory\n", [takeKing, leave])
  else:
    print("\nYou loose!")
    gameOver()

def takeKing():
  print("\nYou aquire the king's armor (click e to view inventory)\n")
  print("You aquire the king's sword (click e to view inventory)\n")
  user.armor.upgrade([3, 4, 5, 5, 8], "Armor of the Kings")
  user.weapon.upgrade({"got a weak hit on" : 3, "struck" : 4, "attacked" : 5, "sliced" : 5, "critically hit" : 8}, {"missed" : 0, "critically hit" : 10}, "Sword of the Kings")
  print("You are now the new king!\n")
  gameOver(True)

def leave():
  print("You leave the king's armor, but find a secret trapdoor on the way out!")
  master(["a"], "(a) Go through\n(b) Leave anyways\n(e) inventory\n", [trapdoor, pit])

def trapdoor():
  print("The trapdoor was an exit to the outer world!")
  gameOver(True)

def pit():
  print("While wondering about the trapdoor, you fall into a hidden death pit")
  gameOver()

# Game over
def gameOver(win=False):
  if win == True:
    print("You win!")
  master(["a"], "(a) Restart\n(e) inventory\n(m) Main Menu\n", [start])

def initialize(dictionary, message):
  item = input('\n' + message).lower()
  while True:
    try:
      return dictionary[item]
    except:
      item = input(message).lower()

def bossRun():
  user = player(input("\nEnter your name\n> "))

  # Assignes 'a' to fist, 'b', to longsword, etc
  weapon = initialize({"a" : [{"missed" : 0, "hit" : 1, "hit" : 1, "critically hit" : 2}, {"missed" : 0, "critically hit" : 2}, "Fist"], "b" : [{"missed" : 0, "hit" : 1, "struck" : 2, "struck" : 2, "critically hit" : 3}, {"missed" : 0, "critically hit" : 3}, "Longsword"], "c" : [{"got a weak hit on" : 1, "hit" : 2, "struck" : 3, "struck" : 3, "critically hit" : 4}, {"missed" : 0, "critically hit" : 5}, "Mace"], "d" : [{"got a weak hit on" : 2, "struck" : 3, "attacked" : 4, "sliced" : 5, "critically hit" : 6}, {"missed" : 0, "critically hit" : 8}, "Katana"], "e" : [{"got a weak hit on" : 2, "struck" : 4, "attacked" : 5, "sliced" : 6, "critically hit" : 7}, {"missed" : 0, "critically hit" : 9}, "Gem Sword"], "f" : [{"got a weak hit on" : 3, "struck" : 4, "attacked" : 5, "sliced" : 5, "critically hit" : 8}, {"missed" : 0, "critically hit" : 10}, "Sword of the Kings"]}, "Choose your weapon\n(a) Fist\n(b) Longsword\n(c) Mace\n(d) Katana\n(e) Gem Sword\n(f) Sword of the Kings\n> ")

  # Assignes 'a' to none, 'b', to leather, etc
  armor = initialize({"a" : [[1], "None"], "b" : [[1, 2, 2, 3], "Leather Armor"], "c" : [[1, 2, 3, 4, 5], "Chain Armor"], "d" : [[1, 3, 4, 4, 5], "Old Plate Armor"], "e" : [[2, 3, 4, 5, 6], "Plate Armor"], "f" : [[3, 4, 5, 5, 8], "Armor of the Kings"]}, "Choose your armor\n(a) None\n(b) Leather\n(c) Chain\n(d) Old Plate\n(e) Plate\n(f) Armor of the Kings\n> ")

  # Upgrades weapon to weapon chosen
  user.weapon.upgrade(weapon[0], weapon[1], weapon[2])
  user.armor.upgrade(armor[0], armor[1])

  # Shield?
  while True:
    shield = input("\nShield?\n(a) Yes\n(b) No\n")
    if shield == 'a' or shield == 'b':
      break
  if shield == 'a':
    user.shield = True
  else:
    user.shield = False

  # Boss run game flow
  if bosses(user, enemy(4, "snake", {"missed" : 0, "bit you" : 1, "bit you" : 1, "poisoned you" : 3})) == True:
    if bosses(user, enemy(4, "hawk", {"missed" : 0, "bit you" : 1, "bit you" : 1, "dived on you" : 3})) == True:
      if bosses(user, enemy(10, "ogre", {"missed" : 0, "struck" : 1, "punched" : 2, "hit" : 3, "critically hit" : 4})) == True:
        if bosses(user, enemy(15, "Armored Skeleton", {"missed" : 0, "punched" : 2, "struck" : 3, "stomped on" : 4, "critically hit" : 6})) == True:
          if bosses(user, enemy(10, "Armored Ogre", {"missed" : 0, "hit" : 3, "struck" : 4, "sword-attacked" : 5, "critically hit" : 8}, [1, 1, 2])) == True:
            if bosses(user, enemy(25, "Serpent", {"missed" : 0, "bit" : 4, "poisoned" : 7, "whipped" : 11, "critically hit" : 15})) == True:
              if bosses(user, enemy(20, "King", {"got a weak hit on" : 2, "struck" : 4, "attacked" : 4, "sliced" : 5, "critically hit" : 8}, [2, 2, 4, 4, 8])) == True:
                print('\n' + user.name + "'s' boss run\nWeapon: " + user.weapon.name + "\nArmor: " + user.armor.name + "\nShield: " + str(user.shield) + "\nBoss run complete!")
  # Game over for boss run
  if input("\n(a) Replay\n(b) Main menu\n> ") == 'a':
    bossRun()
  else:
    menu()

# Does the boss run
def bosses(player, boss):
  results = battle(player, boss)
  if results == True:
    return True
  else:
    print('\n' + player.name + "'s boss run\nWeapon: " + player.weapon.name + "\nArmor: " + player.armor.name + "\nShield: " + str(player.shield) + "\nOut at " + boss.name.lower())

# Starts the "chain reaction" of functions
print("Welcome to Jungle Adventure!")
menu()

"""
STATS

WEAPONS         Attack Damage     Avg Damage  Jab Damage
Fist            [0, 1, 1, 2]      Avg 1.0     [0, 2]
Longsword       [0, 1, 2, 2, 3]   Avg 1.6     [0, 3]
Mace            [1, 2, 3, 3, 4]   Avg 2.6     [0, 5]
Katana          [2, 3, 4, 5, 6]   Avg 4.0     [0, 8]
Gem Sword       [2, 4, 5, 6, 7]   Avg 4.8     [0, 9]
King's Sword    [3, 4, 5, 5, 8]   Avg 5.0     [0, 10]


ARMOR           Protection        Average Protection
None            [1]               Avg 1.0
Leather Armor   [1, 2, 2, 3]      Avg 2.0
Chain Armor     [1, 2, 3, 4, 5]   Avg 3.0
Old Plate Armor [1, 3, 4, 4, 5]   Avg 3.4
Plate armor     [2, 3, 4, 5, 6]   Avg 4.0
King's Armor    [3, 4, 5, 5, 8]   Avg 5.0


ENEMIES   HP    Damage            Avg Damage  Avg Prot
Snake     4hp   [0, 1, 1, 3]      Avg 1.25    1
Hawk      4hp   [0, 1, 1, 3]      Avg 1.25    1
Ogre      10hp  [0, 1, 2, 3, 4]   Avg 2.0     1
Skeleton  15hp  [0, 2, 3, 4, 6]   Avg 3.0     1
Ogre 2    10hp  [0, 3, 4, 5, 8]   Avg 3.4     1.3
Serpent   25hp  [0, 4, 7, 11, 15] Avg 7.4     1
King      20hp  [3, 4, 5, 5, 8]   Avg 5.0     4.2

"""
