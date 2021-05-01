import random

from typing import TYPE_CHECKING

from entity import Actor, Entity
from renderer import render_task

if TYPE_CHECKING:
    from input_handles import TaskHandler

#using random.random() without seed as RNG may be naive but oof barely a game at this point hehe
#TODO: at least add seed
    
#scale of 1 to 10, 10 being highest motivation possible for task
def motivation() -> int:
    # scaled value = min + (value * (max - min))
    return int(1 + (random.random() * 9))

#other person can gain (or lose) up to 20 energy
def t_energyGain() -> int:
    return int(-17 + (random.random() * 34))

#special are standard coin flips, doesn't mean rare
def special() -> bool:
    if random.random() > 0.5:
        return False
    return True;

def calcEnergy(motivation: int, special: bool) -> int:
    #padding is a random number 0 to 7 to add to energy gain/loss
    padding = int(random.random() * 7)
    if special:
        return motivation + padding
    else:
        #higher motivation -> lose less energy) + padding
        return  int((1/motivation * 10) + padding)


def create_task():
    return {
        "motivation": motivation(),
        "T Energy Gain": t_energyGain(),
        "special": special()
    }

