from game.settings import MAX_RECORDS_NUMBER

class PlayerRecord:
    """Represents a player's game record with name, mode and score.
    
    Attributes:
        name (str): Player's name.
        mode (str): Game mode ('NORMAL' or 'HARD').
        score (int): Player's score.
    """
    name: str
    mode: str
    score: int
    
    def __init__(self, name: str, mode: str, score: int):
        """Initialize a PlayerRecord instance.
        
        Args:
            name: Player's name.
            mode: Game mode ('NORMAL' or 'HARD').
            score: Player's score.
        """
        self.name = name
        self.mode = mode
        self.score = score

    def __gt__(self, another_record: 'PlayerRecord') -> bool:
        """Defines how records are compared for sorting.
        
        Args:
            another_record: Another PlayerRecord to compare with.
            
        Returns:
            bool: True if this record is greater than another.
        """
        if self.mode != another_record.mode:
            return self.mode == "HARD"
        return self.score > another_record.score
    
    def __eq__(self, another_record: 'PlayerRecord') -> bool:
        """Check if records represent the same player and mode.
        
        Args:
            another_record: Another PlayerRecord to compare with.
            
        Returns:
            bool: True if records have same name and mode.
        """
        return self.name == another_record.name and self.mode == another_record.mode

    def __str__(self) -> str:
        """String representation of the record.
        
        Returns:
            str: Formatted string 'name | mode | score'.
        """
        return f"{self.name} | {self.mode} | {self.score}"


class GameRecord:
    """Manages a collection of player records.
    
    Attributes:
        records (list[PlayerRecord]): List of player records.
    """
    records: list

    def __init__(self):
        """Initialize an empty GameRecord."""
        self.records = []

    def add_record(self, player_record: PlayerRecord) -> None:
        """Add or update a player record.
        
        Args:
            player_record: Record to add or update.
        """
        for i, record in enumerate(self.records):
            if player_record == record:
                if player_record > record:
                    self.records[i] = player_record
                return
            
        self.records.append(player_record)

    def prepare_records(self) -> None:
        """Sort records and trim to MAX_RECORDS_NUMBER."""

        self.records.sort(reverse = True)
        if len(self.records) > MAX_RECORDS_NUMBER:
            self.records = self.records[:MAX_RECORDS_NUMBER]


class ScoreHandler:
    """Handles loading, saving and displaying game scores.
    
    Attributes:
        game_record (GameRecord): Current game records.
        file_name (str): Path to scores file.
    """
    game_record: GameRecord
    file_name: str

    def __init__(self, file_name: str):
        """Initialize ScoreHandler and load existing records.
        
        Args:
            file_name: Path to scores file.
        """
        self.file_name = file_name
        self.read()

    def read(self) -> None:
        """Read records from file into game_record."""
        try:
            with open(self.file_name, "r") as file:
                self.game_record = GameRecord()
                for line in file:
                    if line.strip():  # Skip empty lines
                        str_record = line.split("|")
                        record = PlayerRecord(
                            str_record[0].strip(), 
                            str_record[1].strip(), 
                            int(str_record[2].strip())
                        )
                        self.game_record.records.append(record)
        except FileNotFoundError:
            self.game_record = GameRecord()

    def save(self, player_record: PlayerRecord) -> None:
        """Add a new record and save all records to file.
        
        Args:
            player_record: New record to add.
        """
        self.game_record.add_record(player_record)
        self.game_record.prepare_records()
        with open(self.file_name, "w") as file:
            for record in self.game_record.records:
                file.write(f"{record.name} | {record.mode} | {record.score}\n")

    def display(self) -> None:
        """Display all records in a formatted way."""
        if not self.game_record.records:
            print("\nNo records available yet!")
            return
        
        max_name_len = max(len(record.name) for record in self.game_record.records)
        if max_name_len < 4:  max_name_len = 4

        print("\n=== HIGH SCORES ===")
        print(f"{'Rank'} | {'Name':<{max_name_len}} | {'Mode  '} | {'Score'}")
        print("-" * (20 + max_name_len))
        
        for i, record in enumerate(sorted(self.game_record.records, reverse=True), 1):
            print(f"{i:<4} | {record.name:<{max_name_len}} | {record.mode:<6} | {record.score}")