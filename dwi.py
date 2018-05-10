import math
import os
import random
import string

script_dir = os.path.dirname(__file__)

def get_max_hp(class_name):
    if class_name in ['Berserker']:
        return(12)
    elif class_name in ['Fighter', 'Paladin', 'Dark Knight', 'Battlemaster']:
        return(10)
    elif class_name in ['Barbarian', 'Cleric', 'Ranger', 'Monk', 'Hunter', 'Vampire', 'Skirmisher', 'Slayer']:
        return(8)
    elif class_name in ['Bard', 'Druid', 'Thief', 'Trickster', 'Shaman']:
        return(6)
    else:
        return(4)

def get_damage_die(class_name):
    if class_name in ['Barbarian', 'Fighter', 'Paladin', 'Dark Knight', 'Berserker', 'Channeler', 'Slayer']:
        return('d10')
    elif class_name in ['Immolator', 'Ranger', 'Thief', 'Monk', 'Hunter', 'Vampire', 'Battlemaster']:
        return('d8')
    elif class_name in ['Bard', 'Cleric', 'Druid', 'Trickster', 'Shaman', 'Skirmisher']:
        return('d6')
    else: #wizard, necromancer
        return('d4')

class character:

    def __init__(self, id = "", name = "Jim", class_name = "Wizard", level = 1, attribute = {'str': 10, 'dex': 10, 'con': 10, 'int': 10, 'wis': 10, 'cha': 10}):
        self.name = name
        self.class_name = class_name
        self.level = level
        self.attribute = attribute
        self.id = id
        self.max_hp = get_max_hp(class_name)
        self.damage_die = get_damage_die(class_name)
        self.advanced_moves = []
        self.level_1_spells = ""
        self.level_3_spells = ""
        self.level_5_spells = ""
        self.level_7_spells = ""
        self.level_9_spells = ""

    def skill_use(self, governing_attribute):
        return(roll('2d6', get_modifier(self.attribute[governing_attribute])))

    def damage_roll(self):
        return(roll(self.damage_die))

    def update(self, new_data):
        parsable_data = new_data.splitlines()
        self.name = parsable_data[0].split(" the ")[0]
        self.class_name = (parsable_data[0].split(" the ")[1]).split(", ")[0]
        self.level = int(parsable_data[0].split(" Level ")[1])
        # will clean these up eventually, hopefully, anyway
        self.attribute['str'] = int((parsable_data[2][5:7]).strip())
        self.attribute['dex'] = int((parsable_data[3][5:7]).strip())
        self.attribute['con'] = int((parsable_data[4][5:7]).strip())
        self.attribute['int'] = int((parsable_data[5][5:7]).strip())
        self.attribute['wis'] = int((parsable_data[6][5:7]).strip())
        self.attribute['cha'] = int((parsable_data[7][5:7]).strip())
        self.max_hp = get_max_hp(self.class_name) + self.attribute['con']
        self.damage_die = get_damage_die(self.class_name)
        self.advanced_moves = parsable_data[10][15:].split(", ")
        if self.class_name in ['Wizard']:
            self.level_1_spells = parsable_data[14][9:]
            try:
                self.level_3_spells = parsable_data[15][9:]
                self.level_5_spells = parsable_data[16][9:]
                self.level_7_spells = parsable_data[17][9:]
                self.level_9_spells = parsable_data[18][9:]
            except:
                pass

    def pull_attributes(self):
        return([self.attribute['str'], self.attribute['dex'], self.attribute['con'], self.attribute['int'], self.attribute['wis'], self.attribute['cha']])

    def full_output(self):
            full_text_output = str(self.name + " the " + self.class_name + ", Level " + str(self.level) +
                    "\n----------------------------------" +
                    "\nSTR: " + str(self.attribute['str']) + " (" + str(get_modifier(self.attribute['str'])) + ")" +
                    "\nDEX: " + str(self.attribute['dex']) + " (" + str(get_modifier(self.attribute['dex'])) + ")" +
                    "\nCON: " + str(self.attribute['con']) + " (" + str(get_modifier(self.attribute['con'])) + ")" +
                    "\nINT: " + str(self.attribute['int']) + " (" + str(get_modifier(self.attribute['int'])) + ")" +
                    "\nWIS: " + str(self.attribute['wis']) + " (" + str(get_modifier(self.attribute['wis'])) + ")" +
                    "\nCHA: " + str(self.attribute['cha']) + " (" + str(get_modifier(self.attribute['cha'])) + ")" +
                    "\n----------------------------------" +
                    "\nMax HP: " + str(self.max_hp) + " | Damage Die: " + self.damage_die +
                    "\nAdvanced Moves: " + ", ".join(self.advanced_moves)
                    )
            if self.class_name in ['Wizard']:
                full_text_output += ("\n----------------------------------" +
                                     "\nLEARNED SPELL LIST" +
                                     "\nCantrips: Light, Prestidigitation, Unseen Servant"
                                     "\nLevel 1: " + self.level_1_spells
                                     )
            if self.level >= 3:
                full_text_output += "\nLevel 3: " + self.level_3_spells
            if self.level >= 5:
                full_text_output += "\nLevel 5: " + self.level_5_spells
            if self.level >= 7:
                full_text_output += "\nLevel 7: " + self.level_7_spells
            if self.level >= 9:
                full_text_output += "\nLevel 9: " + self.level_9_spells
            return(full_text_output)

def roll(dice = '2d6', modifier = 0):
    try: # gonna be for throwing just 'd8' or whatever in there
        number_of_dice = int(dice.split("d")[0])
        sides_of_dice = int(dice.split("d")[1])
    except:
        number_of_dice = 1
        sides_of_dice = int(dice[1:])
    rolls = random.sample(range(1, sides_of_dice+1), number_of_dice)
    result = sum(rolls) + modifier
    return(result)

def get_modifier(attribute):
    if attribute <= 3:
        return(-3)
    elif attribute <= 5:
        return(-2)
    elif attribute <= 8:
        return(-1)
    elif attribute <= 11:
        return(0)
    elif attribute <= 15:
        return(1)
    elif attribute <= 17:
        return(2)
    else:
        return(3)

def create(id = "", random_creation = False, attributes = {'str': 16, 'dex': 15, 'con': 13, 'int': 12, 'wis': 9, 'cha': 8}, name = 'Jim', class_name = 'Fighter', level = 1):
    if random_creation == True:
        attributes = {'str': roll('3d6'), 'dex': roll('3d6'), 'con': roll('3d6'), 'int': roll('3d6'), 'wis': roll('3d6'), 'cha': roll('3d6')}
    else:
        pass
    if id == "": #for whenever nothing is passing an ID to it, it'll instead generate one
        string_junk = string.ascii_letters + string.digits
        for _ in range(6):
            id +=  random.choice(string_junk) 
    new_character = character(id, name, class_name, level, attributes)
    print(new_character.full_output())
    save(new_character)

def load(id="", name="Jim", class_name="Wizard"): #loads from text file
    pc_list = os.listdir('pc/')
    if id != "":
        for i, elem in enumerate(pc_list):
            if id in elem:
                index_id = i
    elif (name + class_name != ""):
        for i, elem in enumerate(pc_list):
            if (name + class_name) in elem:
                index_id = i
    else:
        return("broken missing etc")
    with open("pc/" + pc_list[index_id], "r") as file:
        loaded_char = character()
        loaded_char.update(file.read())
    return(loaded_char)


def save(char): #saves to text file
    savedir = "pc" # if playercharacter == True else "npc"
    fileFull = os.path.join(script_dir, savedir, char.name + char.class_name + '-' + char.id + ".txt")
    full_save_output = char.full_output()
    with open(fileFull, "w+") as file:
        file.write(full_save_output)

def main():
#    test_file = open("testchar.txt", "r").read()
#    current_character = character()
#    current_character.update(test_file)
#    save(current_character)
    current_char = load()


if __name__ == "__main__":
    main()
