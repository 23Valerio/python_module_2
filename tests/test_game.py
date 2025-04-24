from unittest import TestCase
from unittest.mock import patch
from game.models import Player
from game.game import Game
from game.settings import WIN, LOSE, MODE_NORMAL, DRAW, WIN, LOSE


class TestGame(TestCase):
    def test_init_game(self):
        player = Player("TestPlayer")
        game = Game(player, MODE_NORMAL)
        self.assertEqual(game.player.name, "TestPlayer")
        self.assertEqual(game.enemy.lives, 1)
        self.assertEqual(game.mode, 1)

    def test_create_enemy(self):
        player = Player("TestPlayer")
        game = Game(player, MODE_NORMAL)
        game.create_enemy()
        self.assertEqual(game.enemy.level, 2)
        self.assertEqual(game.enemy.lives, 2)

    @patch('game.models.Enemy.select_attack', return_value = "Scissors")
    @patch('game.models.Player.select_attack', return_value = "Stone")
    def test_fight_win(self, mock_player_attack, mock_enemy_attack):
        player = Player("TestPlayer")
        game = Game(player, MODE_NORMAL)
        self.assertEqual(game.fight(), WIN)

    @patch('game.models.Player.select_attack', return_value = "Stone")
    @patch('game.models.Enemy.select_attack', return_value = "Stone")
    def test_fight_draw(self, mock_player_attack, mock_enemy_attack):
        player = Player("TestPlayer")
        game = Game(player, MODE_NORMAL)
        self.assertEqual(game.fight(), DRAW)

    @patch('game.models.Enemy.select_attack', return_value = "Paper")
    @patch('game.models.Player.select_attack', return_value = "Stone")
    def test_fight_lose(self, mock_player_attack, mock_enemy_attack):
        player = Player("TestPlayer")
        game = Game(player, MODE_NORMAL)
        self.assertEqual(game.fight(), LOSE)

    def test_handle_fight_result_win(self):
        player = Player("TestPlayer")
        game = Game(player, MODE_NORMAL)
        game.enemy.lives = 2
        game.handle_fight_result(WIN)
        self.assertEqual(game.player.score, 1)
        self.assertEqual(game.enemy.lives, 1)

    def test_handle_fight_result_lose(self):
        player = Player("TestPlayer")
        game = Game(player, MODE_NORMAL)
        game.handle_fight_result(LOSE)
        self.assertEqual(game.player.lives, 1)

    def test_handle_fight_result_draw(self):
        player = Player("TestPlayer")
        game = Game(player, MODE_NORMAL)
        game.handle_fight_result(DRAW)
        self.assertEqual(game.player.lives, 2)
        self.assertEqual(game.enemy.lives, 1)

    @patch('game.game.Game.create_enemy')
    def test_handle_fight_result_enemy_down_create_enemy(self, mock_create):
        player = Player("TestPlayer")
        game = Game(player, MODE_NORMAL)
        game.handle_fight_result(WIN)
        self.assertEqual(mock_create.call_count, 1)

    @patch('game.game.Game.save_score')
    def test_handle_fight_result_enemy_down_create_enemy(self, mock_save):
        player = Player("TestPlayer")
        game = Game(player, MODE_NORMAL)
        game.player.lives = 1
        with self.assertRaises(SystemExit):
            game.handle_fight_result(LOSE)
            self.assertEqual(mock_save.call_count, 1)
            self.assertEqual(SystemExit.call_count, 1)
