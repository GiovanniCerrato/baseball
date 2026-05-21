from dataclasses import dataclass

@dataclass
class Team:
    teamCode: str
    name:str
    year:int
    salarioTotale:float

    def __hash__(self):
        return hash(self.teamCode)
    def __eq__(self,other):
        return self.teamCode == other.teamCode
    def __str__(self):
        return f"{self.name} ({self.teamCode}) "