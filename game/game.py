from game.models import Player, Enemy
from game.settings import ATTACK_PAIRS_OUTCOME, POINTS_FOR_KILLING, WIN, LOSE, WEARY_FACE, GRINNING_FACE, SKULL, SHIELD
from game.exceptions import GameOver, EnemyDown
import sys


class Game():
    player: Player
    enemy: Enemy
    mode: int

    def __init__(self, player: Player, mode: int):
        self.player = player
        self.mode = mode
        self.enemy = Enemy(1, mode)

    def create_enemy(self):
        self.enemy.level += 1
        self.enemy.lives = self.enemy.level * self.mode

    def fight(self):
        return ATTACK_PAIRS_OUTCOME[(self.player.select_attack(), self.enemy.select_attack())]

    def handle_fight_result(self, fight_result: int):
        try:
            if fight_result == WIN:
                print(f"You Win! {GRINNING_FACE} Lives left - {self.player.lives}")
                self.player.add_score(POINTS_FOR_KILLING * self.mode)
                self.enemy.decrease_lives()
            elif fight_result == LOSE:
                self.player.decrease_lives()
                print(f"Enemy Win! {SKULL} Lives left - {self.player.lives}")
            else:
                print(f"Draw  {SHIELD}  game continues")
        except GameOver:
            print(f"You Lose! {WEARY_FACE} Game Over!")
            print(f"Your score: {self.player.score}")
            sys.exit() 
        except EnemyDown:
            self.create_enemy()
            print(f"Enemy Down - next level: {self.enemy.level}")
            pass
    def save_score(self):
        pass

    def play(self):
        while True:
            fight = self.fight()
            self.handle_fight_result(fight)


