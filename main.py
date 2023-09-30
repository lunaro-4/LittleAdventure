from __future__ import annotations
import random


class Entity:
    name = 'unnamed entity' 

    def __init__(self, max_health : int, attack: int = random.randrange(1,30), defence : int = random.randrange(1,30) ):
        if 0< attack <= 30 or  0< defence <= 30 :
            pass
        else:
            raise ValueError("Both 'attack' and 'defence' must be between 1 and 30")
        self.max_health = max_health
        self.attack = attack
        self.defence = defence
        self.alive:bool = True
        self.current_health: int = self.max_health

    def receive_damage(self,damage):
        self.current_health -= damage
        if self.current_health <= 0:
            self.current_health = 0
            self.alive = False

    def attack_action(self,target: Entity ):
        attack_mod = self.attack - target.defence
        if attack_mod <=0:
            print(f'Attack against {target.__class__.name} is ineffective!')
        else:
            damage = 0
            for _ in range(attack_mod):
                roll = random.randrange(1,6)
                if roll >=5:
                    damage += 1
            target.receive_damage(damage)
            print(f'{self.__class__.name} deal {damage} damage to {target.__class__.name}!')
        return True
        
class Player(Entity):
    name = 'You'
    potions = 4

    def heal(self):
        if self.__class__.potions >0:
            self.current_health += round(self.max_health * 0.3)
            self.__class__.potions -=1
            if self.current_health > self.max_health:
                self.current_health = self.max_health
            return True
        else:
            return False

    def get_info(self):
        print(f'This is {self.__class__.name}!\n')
        print(f'Health: {self.current_health}')
        print(f'Attack: {self.attack}')
        print(f'Defence: {self.defence}')
        print(f'Potions left: {self.__class__.potions}')

class Monster(Entity):
    name = 'Gnargl'
    description ='It looks hungry and dangerous!' 

    def get_info(self):
        print(f'This is a feral {self.__class__.name}! {self.__class__.description}\n')
        if self.alive == True:
            print(f'Health: {self.current_health}')
            print(f'Attack: {self.attack}')
            print(f'Defence: {self.defence}')
        else:
            print('This creature is dead')


class GameEngine:
    def __init__(self, turn = 1 , info = False) -> None:
        self.turn = turn
        self.info = info

    def quit(self):
        print('See you later!')
        exit()
    def victory(self):
        print('\
                You are victoriuos!\n\
                You have defeated all the monsters and secured an invaluable trasure!\n\
                Come back if you wish to join new adventure!\n')
        self.quit()

    def gameloop(self, player: Player, enemies: List[Monster]):
        if player.alive == False:
            print('\
                    You suffer a defeat! Luck was not on your side this time\n\
                    Come back again\n')
            self.quit()
        alive_enemies = dict()
        alive_enemies.clear()
        for enemy in range(len(enemies)):
            if enemies[enemy].alive:
                alive_enemies[str(enemy+1)] = enemies[enemy]
        turn_state = False
        if self.turn == 1 or self.info == True:
            player.get_info() 
            print('\n\n') 
            for enemy in range(len(enemies)):
                print(f'Gnargl {enemy+1}')
                enemies[enemy].get_info()
                print('\n\n') 
            self.info = False
        print(f'Turn {self.turn} \n\n Your move!\n\n')
        print("What is your next move?")
        x = input("[A]ttack/[D]rink potion/[I]nfo/[F]lee(quit)")
        print('\n')
        if x in  ['A','a']:
            loop = False
            while loop == False:
                print('This enemies are still alive:')
                for enemy in alive_enemies.keys():
                    print(f'Gnargl {enemy}', end='  ')
                print('')
                target = input('Type enemy number or [C] to cancel:')
                if target in ['C', 'c']:
                    loop = True
                else:
                    try:
                        player.attack_action(alive_enemies[target])
                        loop = True
                        turn_state = True
                        if alive_enemies[target].alive == False:
                            alive_enemies.pop(target)
                            print(f'Gnargl {target} has fallen!')
                        else:
                            print(f'Gnargl {target} has {alive_enemies[target].current_health} health left')
                        print('')
                    except:
                        print('Choose valid target, or type [C] to cancel')
                        print('')
        elif x in ['D','d']:
            turn_state = player.heal()
            if turn_state :
                print('You used one of your potions!')
                print(f'You now have {player.current_health} health and {player.potions} potins left')
            else:
                print('You have run out of potions! Try something else')
        elif x in ['I','i']:
            self.info = True
        elif x in ['F','f']:
            confirm = input('Are you shure? [y/N]:')
            if confirm in ['y','yes','Yes','Y']:
                self.quit()
            else:
                pass
        else:
            print('Unrecognised Command!')
            x = ''

        if len(alive_enemies) == 0:
            self.victory()

        if turn_state == True:
            print('\nEnemies make their move!\n') 
            for enemy in alive_enemies.values():
                enemy.attack_action(player)
            turn_state = False
            print(f'You have {player.current_health} health left') 
        if x != '':
            self.turn +=1
        print('\n')


if __name__ == '__main__':
    ge = GameEngine()
    while True:
        x = input('Welcome! Would you like to embark on a quest? [y/N]:')
        if x in ['y','yes','Yes','Y']:
            break
        elif x in ['n','no','No','N','']:
            ge.quit()
            break
        else:
            print("I didn't get that, please repeat") 
            x = ''
    player1 = Player(max_health = 30, attack= 20, defence = 5)
    gnargl1 = Monster(max_health = 20, attack= 12, defence = 0)
    gnargl2 = Monster(max_health = 20, attack= 12, defence = 0)
    gnargl3 = Monster(max_health = 20, attack= 12, defence = 0)
    
    enemies = [gnargl1, gnargl2, gnargl3]

    print('\n\nYou encounter pack of feral gnargl! Here is the situation:\n')
    while True:
        ge.gameloop(player1,enemies)

