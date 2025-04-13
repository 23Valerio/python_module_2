class GameOver(Exception):
    """Raised if the user has no lives left"""


class EnemyDown(Exception):
    """Raised if the enemy has no lives left"""


class ExitGame(Exception):
    """Raised if user choose command to exit the game"""