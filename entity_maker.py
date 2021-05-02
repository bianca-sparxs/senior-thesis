from components.ai import OtherPerson
from components.fighter import Fighter
from components.consumable import HealingConsumable
from entity import Actor, Item
import names
import colors

##TODO: entity object carries gamemode as attribute in order to change color
def getName():
    return names.get_last_name()

def getUniquePerson():
    return Actor(
        char="T", 
        color=(63, 127, 0), 
        name=getName(),
        fighter=Fighter(energy=1), 
        ai_cls=OtherPerson
)

player = Actor(
    char="@", 
    color=(255, 255, 255), 
    name="Player", 
    fighter=Fighter(energy=100),
    ai_cls=OtherPerson,
    
)

food = Item(
    char="%",
    color=(127, 0, 255),
    name="Food",
    consumable=HealingConsumable(amount=7),
)

# me = Entity(char="o", color=(63, 127, 63), name="You", blocks_movement=True)

