from game.models import Player
from game.game import Game
from game.score import ScoreHandler
from game.settings import MODES, CROSSED_SWORDS, ANGRY_FACE, SCORE_FILE
from game.exceptions import ExitGame


def create_player() -> Player:
    """Creates a new player instance by prompting for player name.
    
    Returns:
        Player: A new Player instance with the entered name.
        
    Note:
        Continuously prompts until a non-empty name is provided.
    """

    while True:
        player_name = input("Please enter your name: ").strip()
        if player_name == "":
            print("Name cannot be empty!!! ")
        else:
            return Player(player_name)
    
def choose_mode() -> int:
    """Prompts user to select game difficulty mode.
    
    Returns:
        int: Selected mode (1 for NORMAL, 2 for HARD).
        
    Raises:
        Continues prompting until valid input is received.
    """

    while True:
        mode = input("Chose mode from below : (1 - NORMAl, 2 - HARD): ").strip()
        if mode != "" and mode in MODES:
            return int(mode)
        else:
            print(f"Wrong input {ANGRY_FACE}")

def play_game() -> None:
    """Main game - creates player, selects mode and starts the game."""

    print(f" {CROSSED_SWORDS}  Game started  {CROSSED_SWORDS}")
    player = create_player()
    print(f"Player name: {player.name}")
    mode = choose_mode()
    game = Game(player, mode)
    game.play()

def show_scores() -> None:
    """Displays the current high scores from the score file."""

    print(f"{CROSSED_SWORDS} BEST RESULTS: {CROSSED_SWORDS}")
    score_handler = ScoreHandler(SCORE_FILE)
    score_handler.display()

def exit() -> None:
    """Terminates the game by raising ExitGame exception."""

    print("Quit Game")
    ExitGame()

def main() -> None:
    """Main entry point for the game application.
    
    Presents a menu and handles user selection between:
    - Starting a new game
    - Showing high scores
    - Exiting the game
    
    Note:
        Runs in infinite loop until user chooses to exit.
    """
    menu_options = {
        '1': play_game,
        '2': show_scores,
        '3': exit
    }
   
    while True:
        option = input("Chose option from below: (1 - start the game, 2 - show scores, 3 - exit): ")
        if option in menu_options:
            return menu_options[option]()
        print("Wrong option. Please, enter 1, 2 or 3.")
    
if __name__ == "__main__":
    main()