
class ScoreKeeper:
    def __init__(self) -> None:
        self.energy_spent = 0 #total energy spent
        self.others_energy_gain = 0 #energy that other people gained in total through your tasks
        self.seek_mode = 0 #times enetered seek mode
        self.seek_energy_spent = 0 #energy spent in seek mode

        #type of tasks with other people
        self.exploit = 0 #gain energy while other person loses
        self.mutual = 0 #both people gain energy
        self.assistance = 0 #lose energy while the other person gains
        self.reckless = 0 #both people lose energy
    
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
    
    def tasks_done(self):
        return self.exploit + self.mutual + self.assistance + self.reckless
