import random

from typing import TYPE_CHECKING

from effects import Effect
from renderer import render_task


if TYPE_CHECKING:
    from input_handles import TaskHandler

#using random.random() without seed as RNG may be naive but oof barely a game at this point hehe
#TODO: at least add seed
    
#scale of 1 to 10, 10 being highest motivation possible for task
def motivation(effect: Effect) -> int:
    if effect:
        if effect.type == "hope":
            return 10
        elif effect.type == "demotivation":
            return 1
        else: #if effect is blindess or clarity
            return random.randint(1, 10)
    #if there is no effect:
    else:
        # scaled value = min + (value * (max - min))
        return random.randint(1, 10)

#other person can gain (or lose) up to 20 energy
def t_energyGain() -> int:
    return random.randint(-17, 17)

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


def create_task(effect: Effect):
    return {
        "motivation": motivation(effect),
        "T Energy Gain": t_energyGain(),
        "special": special()
    }

