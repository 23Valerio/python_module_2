from unittest import TestCase
from game.models import Player, Enemy
from game.settings import PLAYER_LIVES, ALLOWED_ATTACKS, POINTS_FOR_FIGHT, MODE_NORMAL, MODE_HARD
from game.exceptions import GameOver, EnemyDown
from unittest.mock import patch

class TestPlayer(TestCase):

    def test_player_init(self):
        player = Player("TestPlayer")
        self.assertEqual(player.name, "TestPlayer")
        self.assertEqual(player.lives, PLAYER_LIVES)
        self.assertEqual(player.score, 0)

    @patch('builtins.input', side_effect=['1'])
    def test_select_attack_valid(self, mock_input):
        player = Player("TestPlayer")
        attack = player.select_attack() 
        self.assertEqual(attack, ALLOWED_ATTACKS["1"])
 
    @patch('builtins.input', side_effect=['4', 'g', '', '2'])
    def test_select_attack_invalid(self, mock_input):
        player = Player("TestPlayer")
        attack = player.select_attack() 
        self.assertIn(attack, ALLOWED_ATTACKS.values())
        self.assertEqual(mock_input.call_count, 4)

    def test_decrease_lives(self):
        player = Player("TestPlayer")
        player.decrease_lives()
        self.assertEqual(player.lives, 1)

    def test_decrease_lives_game_over(self):
        player = Player("TestPlayer")
        player.lives = 1
        with self.assertRaises(GameOver):
            player.decrease_lives()
    
    def test_add_score_with_no_score(self):
        player = Player("TestPlayer")
        player.add_score(POINTS_FOR_FIGHT)
        self.assertEqual(player.score, 1)

    def test_add_score_with_ten(self):
        player = Player("TestPlayer")
        player.score = 10
        player.add_score(POINTS_FOR_FIGHT)
        self.assertEqual(player.score, 11)


class TestEnemy(TestCase):

    def test_enemy_init_normal_mode(self):
        enemy = Enemy(1, MODE_NORMAL)
        self.assertEqual(enemy.lives, 1)
        self.assertEqual(enemy.level, 1)
    
    def test_enemy_init_hard_mode(self):
        enemy = Enemy(1, MODE_HARD)
        self.assertEqual(enemy.lives, 2)
        self.assertEqual(enemy.level, 1)

    @patch("random.choice")
    def test_select_attack(self, mock_choice):
        enemy = Enemy(1, MODE_NORMAL)
        mock_choice.return_value = ALLOWED_ATTACKS['1']
        self.assertEqual(enemy.select_attack(), 'Paper')

    def test_decrease_lives_still_has_lives_points(self):
        enemy = Enemy(1, MODE_HARD)
        enemy.decrease_lives()
        self.assertEqual(enemy.lives, 1)

    def test_decrease_lives_enemy_down(self):
        enemy = Enemy(1, MODE_NORMAL)
        with self.assertRaises(EnemyDown):
            enemy.decrease_lives()
