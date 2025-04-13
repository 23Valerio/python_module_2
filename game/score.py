

class PlayerRecord:
    name: str
    mode: int
    score: int

    def __init__(self, name: str, mode: int, score: int):
        self.name = name
        self.mode = mode
        self.score = score

    def __gt__(self):
        pass

    def __str__(self):
        pass


class GameRecord:
    records: PlayerRecord

    def __init__(self):
        self.records = []

    def add_record(self):
        pass


class ScoreHandler:
    game_record: GameRecord
    file_name: str

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.game_record = GameRecord



