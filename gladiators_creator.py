import database
import json
import random

GLADIATORS_NUMBER = 100

def check(random_index, names_to_save):
    if formatted_names[random_index] in names_to_save:
        return check(random_index+1, names_to_save)
    return formatted_names[random_index]

with open('russian_names.json', encoding="utf-8-sig") as file:
    json_data = json.load(file)

formatted_names = []
for human in json_data:
    if len(human['Name'])<5:
        formatted_names.append(human['Name'])

names_to_save = []
for i in range(GLADIATORS_NUMBER):
    random_index = random.randint(0,len(formatted_names)-1)
    name = check(random_index, names_to_save)
    names_to_save.append(name)

DATABASE = database.Database('database.db')
for i in names_to_save:
    DATABASE.execute(f'''insert into gladiators 
    (
        name,
        attack_power,
        hp,
        max_hp,
        crit_chance,
        accuracy,
        evasion,
        owner,
        is_dead,
        level,
        winstreak

    ) VALUES
    (
        '{i}', 10, 100, 100, 1, 1, 1, NULL, 0, 1, 0
    )''')