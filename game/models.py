from game.settings import PLAYER_LIVES, ALLOWED_ATTACKS, POINTS_FOR_FIGHT, ICONS, ANGRY_FACE
from game.exceptions import GameOver, EnemyDown
import random

class Player:
    name: str
    lives: int
    score = 0

    def __init__(self, name: str):
        self.name = name
        self.lives = PLAYER_LIVES
        self.score = 0

    def select_attack(self):
        while True:
            attack = input(f"\nChoose attack: 1 - stone {ICONS['Stone']} 2 - scissors {ICONS['Scissors']} 3 - paper {ICONS['Paper']} -  ")
            if attack in ALLOWED_ATTACKS:
                print(f"You choose {ICONS[ALLOWED_ATTACKS[attack]]} - {ALLOWED_ATTACKS[attack]}")
                return ALLOWED_ATTACKS[attack]
            print(f"Wrong input {ANGRY_FACE}")
            
    def decrease_lives(self):
        self.lives -= POINTS_FOR_FIGHT
        if self.lives <= 0:
            raise GameOver()

    def add_score(self, points: int):
        self.score += points

class Enemy:
    lives: int
    level: int

    def __init__(self, level: int, mode: int):
        self.lives = level * mode
        self.level = level

    def select_attack(self):
        attack = random.choice(list(ALLOWED_ATTACKS.values()))
        print(f"Enemy choose {ICONS[attack]} - {attack}")
        return attack
    
    def decrease_lives(self):
        self.lives -= POINTS_FOR_FIGHT
        if self.lives <= 0:
            raise EnemyDown()