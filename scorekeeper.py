
class ScoreKeeper:
    def __init__(self) -> None:
        self.energy_spent = 0 #total energy spent
        self.others_energy_gain = 0
        self.seek_mode = 0
    
        #TODO: kinds of transactions you helped people gain 

    """
       Learning Python: i don't think you need a decorator unless the setter
        does a sepcial thing to set it, but oh well 
    """
    @property
    def score(self):
        return self.energy_spent

    @score.setter
    def score(self, value: int):
        self.energy_spent = value