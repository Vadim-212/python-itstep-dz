from random import randint

class Samurai:
    # hp = 100
    # armor = 100
    # power = 60
    # accuracy = 40
    # agility = 50

    def __init__(self, hp, armor, power, accuracy, agility):
        self.hp = hp
        self.armor = armor
        self.power = power
        self.accuracy = accuracy
        self.agility = agility
    
    def attack(self, enemy):
        return enemy.defend(self)

    def defend(self, enemy):
        damage = (enemy.power / 2) + randint(round(enemy.accuracy / 2),50)
        damage = damage / ((self.armor / 100) + 1 + self.agility / 100)
        damage = round(damage, 1)
        if damage <= 0:
            damage = 5
        self.hp -= damage
        return damage


class SamuraiBattle:
    def __init__(self, samurai1: Samurai, samurai2: Samurai):
        self.samurai1 = samurai1
        self.samurai2 = samurai2

    def battle(self):
        if self.samurai1.hp <= 0 or self.samurai2.hp <= 0:
            print("Can't start battle")
            return

        while self.samurai1.hp > 0 and self.samurai2.hp > 0:
            print(f'Samurai 1 attacks: -{self.samurai1.attack(self.samurai2)} hp to samurai 2')
            print(f'Samurai 2 attacks: -{self.samurai2.attack(self.samurai1)} hp to samurai 1')


        if self.samurai1.hp > self.samurai2.hp:
            print('First samurai win!')
        else:
            print('Second samurai win!')

if __name__ == "__main__":
    samurai1 = Samurai(100, 60, 50, 25, 40)
    samurai2 = Samurai(100, 50, 75, 35, 40)
    battle = SamuraiBattle(samurai1, samurai2)
    battle.battle()
