import csv
from load_image import load_image


class Hero:
    def __init__(self, group, image, name, cost, move_cost, damage, attack_range, vulnerabilities, buffs, hp):
        self.group = group
        self.image = load_image(image, -1)
        self.name = name
        self.cost = cost
        self.move_cost = move_cost
        self.damage = damage
        self.attack_range = attack_range
        self.vulnerabilities = vulnerabilities
        self.buffs = buffs
        self.hp = hp

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def create_heroes_from_csv(filename):
    heroes = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            name = row[0]
            cost = int(row[1])
            move_cost = int(row[2])
            damage = int(row[3])
            attack_range = int(row[4])
            vulnerabilities = row[5]
            buffs = row[6]
            hp = int(row[7])
            image = name.lower() + '_back.png'  # Assuming the image names follow this pattern
            group = None  # Replace with the appropriate group
            hero = Hero(group, image, name, cost, move_cost, damage, attack_range, vulnerabilities, buffs, hp)
            heroes.append(hero)
    return heroes
