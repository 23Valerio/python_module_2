from game.models import Player, Enemy
from game.settings import ATTACK_PAIRS_OUTCOME, POINTS_FOR_KILLING, WIN, LOSE, WEARY_FACE, GRINNING_FACE, SKULL, SHIELD, SCORE_FILE, STR_MODES
from game.exceptions import GameOver, EnemyDown
from game.score import ScoreHandler, PlayerRecord
import sys


class Game():
    """Main game class that handles the gameplay loop and combat mechanics.
    
    Attributes:
        player (Player): The player instance.
        enemy (Enemy): Current enemy instance.
        mode (int): Game difficulty mode (1 for NORMAL, 2 for HARD).
    """
    player: Player
    enemy: Enemy
    mode: int

    def __init__(self, player: Player, mode: int):
        """Initialize the Game instance.
        
        Args:
            player: Player instance.
            mode: Game difficulty mode (1 or 2).
        """
        self.player = player
        self.mode = mode
        self.enemy = Enemy(1, mode)

    def create_enemy(self):
        """Create a new enemy with increased level and lives."""
        self.enemy.level += 1
        self.enemy.lives = self.enemy.level * self.mode

    def fight(self) -> int:
        """Execute one fight round between player and enemy.
        
        Returns:
            int: Fight result (WIN = 1, LOSE = -1 or DRAW = 0).
        """
        return ATTACK_PAIRS_OUTCOME[(self.player.select_attack(), self.enemy.select_attack())]

    def handle_fight_result(self, fight_result: int):
        """Process the outcome of a fight round.
        
        Args:
            fight_result: Result of the fight (WIN = 1, LOSE = -1 or DRAW = 0).
            
        Raises:
            GameOver: When player loses all lives.
        """  
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
            self.save_score()
            sys.exit() 
        except EnemyDown:
            self.create_enemy()
            print(f"Enemy Down - next level: {self.enemy.level}")

    def save_score(self):
        """Save player's score to the scores file."""
        score_handler = ScoreHandler(SCORE_FILE)
        new_player = PlayerRecord(self.player.name, STR_MODES[self.mode], self.player.score)
        score_handler.save(new_player)

    def play(self):
        """Game loop that continues until player loses."""
        while True:
            fight = self.fight()
            self.handle_fight_result(fight)