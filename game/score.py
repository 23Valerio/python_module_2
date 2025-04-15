from game.settings import MAX_RECORDS_NUMBER

class PlayerRecord:
    name: str
    mode: str
    score: int

    def __init__(self, name: str, mode: str, score: int):
        self.name = name
        self.mode = mode
        self.score = score

    def __gt__(self, another_record):
        if self.mode != another_record.mode:
            return self.mode == "HARD"
        return self.score > another_record.score
    
    def __eq__(self, another_record):
        return self.name == another_record.name and self.mode == another_record.mode

    def __str__(self):
        return f"{self.name} | {self.mode} | {self.score}"


class GameRecord:
    records: list

    def __init__(self):
        self.records = []

    def add_record(self, player_record: PlayerRecord):
        for i, record in enumerate(self.records):
            if player_record == record:
                if player_record > record:
                    self.records[i] = player_record
                return
            
        self.records.append(player_record)

    def prepare_records(self):
        self.records.sort(reverse = True)
        if len(self.records) > MAX_RECORDS_NUMBER:
            self.records = self.records[:MAX_RECORDS_NUMBER]


class ScoreHandler:
    game_record: GameRecord
    file_name: str

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.read()

    def read(self):
        with open(self.file_name, "r") as file:
            self.game_record = GameRecord()
            for line in file:
                str_record = line.split("|")
                record = PlayerRecord(str_record[0].strip(), str_record[1].strip(), int(str_record[2].strip()))
                self.game_record.records.append(record)

    def save(self, player_record: PlayerRecord):
        self.game_record.add_record(player_record)
        self.game_record.prepare_records()
        with open(self.file_name, "w") as file:
            for record in self.game_record.records:
                file.write(f"{record.name} | {record.mode} | {record.score}\n")

    def display(self):
        for record in self.game_record.records:
            print(str(record))



