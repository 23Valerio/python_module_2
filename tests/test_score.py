from unittest import TestCase
from unittest.mock import patch
from game.settings import STR_MODES, MAX_RECORDS_NUMBER
from game.score import PlayerRecord, GameRecord, ScoreHandler

class TestPlayerRecord(TestCase):

    def test_init_player_record(self):
        player_record = PlayerRecord("JohnDoe", STR_MODES[1], 10)
        self.assertEqual(player_record.name, "JohnDoe")
        self.assertEqual(player_record.mode, "NORMAL")
        self.assertEqual(player_record.score, 10)

    def test_equality_true(self):
        player_record = PlayerRecord("JohnDoe", STR_MODES[1], 10)
        the_same_player_record = PlayerRecord("JohnDoe", STR_MODES[1], 10)
        self.assertTrue(player_record == the_same_player_record)

    def test_equality_false(self):
        player_record = PlayerRecord("JohnDoe", STR_MODES[1], 10)
        another_player_record = PlayerRecord("JaneDoe", STR_MODES[1], 10)
        self.assertFalse(player_record == another_player_record)

    def test_comparison_modes(self):
        player_record = PlayerRecord("JohnDoe", STR_MODES[2], 10)
        another_player_record = PlayerRecord("JaneDoe", STR_MODES[1], 10)
        self.assertTrue(player_record > another_player_record)
        self.assertFalse(another_player_record > player_record)

    def test_comparison_scores(self):
        player_record = PlayerRecord("JohnDoe", STR_MODES[1], 20)
        another_player_record = PlayerRecord("JaneDoe", STR_MODES[1], 10)
        self.assertTrue(player_record > another_player_record)
        self.assertFalse(another_player_record > player_record)

    def test_string_record(self):
        player_record = PlayerRecord("JohnDoe", STR_MODES[1], 20)
        self.assertEqual(str(player_record), "JohnDoe | NORMAL | 20")

class TestGameRecord(TestCase):

    def test_init_game_record(self):
        game_record = GameRecord()
        self.assertEqual(game_record.records, [])

    def test_add_record_new_player(self):
        player_record = PlayerRecord("JohnDoe", STR_MODES[1], 10)
        game_record = GameRecord()
        game_record.add_record(player_record)
        self.assertIn(player_record, game_record.records)

    def test_add_record_update_player(self):
        game_record = GameRecord()
        player_1 = PlayerRecord("JohnDoe", STR_MODES[1], 10)
        game_record.add_record(player_1)
        player_2 = PlayerRecord("JohnDoe", STR_MODES[1], 25)
        game_record.add_record(player_2)
        self.assertEqual(len(game_record.records), 1)
        self.assertEqual(game_record.records[0].name, "JohnDoe")
        self.assertEqual(game_record.records[0].mode, "NORMAL")
        self.assertEqual(game_record.records[0].score, 25)

    def test_add_record_different_player(self):
        game_record = GameRecord()
        player_1 = PlayerRecord("JohnDoe", STR_MODES[1], 10)
        player_2 = PlayerRecord("JaneDoe", STR_MODES[2], 100)
        game_record.add_record(player_1)
        game_record.add_record(player_2)
        self.assertEqual(len(game_record.records), 2)
        self.assertIn(player_2, game_record.records)

    def test_prepare_records(self):
        game_record = GameRecord()
        game_record.add_record(PlayerRecord("Thor", STR_MODES[2], 100))
        game_record.add_record(PlayerRecord("Thor", STR_MODES[1], 200))
        game_record.add_record(PlayerRecord("Loki", STR_MODES[1], 10))
        game_record.add_record(PlayerRecord("Hulk", STR_MODES[2], 10))
        game_record.add_record(PlayerRecord("Thanos", STR_MODES[1], 150))

        game_record.prepare_records()

        self.assertEqual(game_record.records[0].mode, 'HARD')
        self.assertEqual(game_record.records[0].name, 'Thor')

        self.assertEqual(game_record.records[1].mode, 'HARD')
        self.assertEqual(game_record.records[1].name, 'Hulk')

        self.assertEqual(game_record.records[2].name, 'Thor')
        self.assertEqual(game_record.records[3].name, 'Thanos')
        self.assertEqual(game_record.records[4].name, 'Loki')

    def test_prepare_records(self):
        game_record = GameRecord()
        for i in range(MAX_RECORDS_NUMBER + 5):
            game_record.add_record(PlayerRecord(f"Player_{i}", STR_MODES[1], 10 * i))

        game_record.prepare_records()
        self.assertEqual(len(game_record.records), MAX_RECORDS_NUMBER)

class TestScoreHandler(TestCase):
    @patch('game.score.ScoreHandler.read')
    def test_score_handler_init(self, mock_read):
        score_handler = ScoreHandler("File_Name")
        self.assertEqual(score_handler.file_name, "File_Name")
        self.assertEqual(mock_read.call_count, 1)