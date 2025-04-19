from game.settings import PLAYER_LIVES, ALLOWED_ATTACKS, POINTS_FOR_FIGHT, ICONS, ANGRY_FACE
from game.exceptions import GameOver, EnemyDown
import random

class Player:
    """Represents a player in the game with name, lives and score attributes.
    
    Attributes:
        name (str): Player's name.
        lives (int): Number of lives.
        score (int): Current game score.
    """
    name: str
    lives: int
    score = 0

    def __init__(self, name: str):
        """Initializes the Player instance.
        
        Args:
            name: The name of the player.
        """
        self.name = name
        self.lives = PLAYER_LIVES
        self.score = 0

    def select_attack(self) -> str:
        """Prompts player to select an attack and validates input.
        
        Returns:
            The selected attack as string ('Stone', 'Scissors' or 'Paper').
            
        Note:
            Continues prompting until valid input is received.
        """
        while True:
            attack = input(f"\nChoose attack: 1 - stone {ICONS['Stone']} 2 - scissors {ICONS['Scissors']} 3 - paper {ICONS['Paper']} -  ")
            if attack in ALLOWED_ATTACKS:
                print(f"You choose {ICONS[ALLOWED_ATTACKS[attack]]} - {ALLOWED_ATTACKS[attack]}")
                return ALLOWED_ATTACKS[attack]
            print(f"Wrong input {ANGRY_FACE}")
            
    def decrease_lives(self):
        """Reduces player's lives by POINTS_FOR_FIGHT.
        
        Raises:
            GameOver: When lives reach zero or below - player has lost.
        """
        self.lives -= POINTS_FOR_FIGHT
        if self.lives <= 0:
            raise GameOver()

    def add_score(self, points: int):
        """Increases player's score.
        
        Args:
            points: Number of points to add to score.
        """
        self.score += points

class Enemy:
    """Represents an enemy character with lives and level attributes.
    
    Attributes:
        lives (int): Number of lives.
        level (int): Current enemy level.
    """
    lives: int
    level: int

    def __init__(self, level: int, mode: int):
        """Initializes the Enemy instance.
        
        Args:
            level: The enemy's level (affects lives).
            mode: Game difficulty mode (affects lives calculation).
        """
        self.lives = level * mode
        self.level = level

    def select_attack(self) -> str:
        """Randomly selects an attack for the enemy.
        
        Returns:
            The selected attack as string ('Stone', 'Scissors' or 'Paper').
        """
        attack = random.choice(list(ALLOWED_ATTACKS.values()))
        print(f"Enemy choose {ICONS[attack]} - {attack}")
        return attack
    
    def decrease_lives(self):
        """Reduces enemy's lives by POINTS_FOR_FIGHT.
        
        Raises:
            EnemyDown: When lives reach zero or below - enemy has lost.
        """
        self.lives -= POINTS_FOR_FIGHT
        if self.lives <= 0:
            raise EnemyDown()