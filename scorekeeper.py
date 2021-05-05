from __future__ import annotations
from typing import TYPE_CHECKING

import colors
import message_log

# if TYPE_CHECKING:
#     from message_log import MessageLog

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

        self.score_msgs = message_log.MessageLog()
    
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

    @property
    def game_over(self):
        print("game over son!")
        self.score_msgs.add_message(f"Energy Spent:{self.energy_spent}",colors.welcome_text)
        self.score_msgs.add_message(f">>>>>>>\n",colors.player_atk)
        self.score_msgs.add_message(f"Seek mode represents seeking an interior life wih God",colors.fov_orange)
        self.score_msgs.add_message(f">>>>>>>\n",colors.player_atk)
        self.score_msgs.add_message(f"Energy spent in Seek mode: {self.seek_energy_spent}",colors.white)
        self.score_msgs.add_message(f"""Time spent in Seek mode: 
            {
                int((self.seek_energy_spent / self.energy_spent)*100)
                if self.seek_energy_spent > 0   
                else 0
            }%""",colors.white)
        self.score_msgs.add_message(f">>>>>>>\n",colors.player_atk)
        self.score_msgs.add_message(f"Perseverance is how many times you entered seek mode vs enegy spent",colors.fov_orange)
        self.score_msgs.add_message(f"""Perseverance:\n
            {
                self.seek_energy_spent / self.energy_spent
                if self.seek_energy_spent > 0 and self.seek_mode > 0   
                else 0
            }""",colors.white)
        self.score_msgs.add_message(f">>>>>>>\n",colors.player_atk)
        self.score_msgs.add_message(f"There are 4 ways to interact with people",colors.fov_orange)
        self.score_msgs.add_message(f"Other People Energy Gain: {self.others_energy_gain}",colors.white)
        self.score_msgs.add_message(f"Assisstance: {self.assistance}",colors.white)
        self.score_msgs.add_message(f"Mutual Benfit: {self.mutual}",colors.white)
        self.score_msgs.add_message(f"Exploitation: {self.exploit}",colors.white)
        self.score_msgs.add_message(f"Reckless: {self.reckless}", colors.bar_text)
        self.score_msgs.add_message(f"PRESS ESC TO QUIT GAME", colors.welcome_text)