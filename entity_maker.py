from components.ai import OtherPerson
from components.fighter import Fighter
from entity import Actor
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
        ai_cls=OtherPerson
)

player = Actor(
    char="@", 
    color=(255, 255, 255), 
    name="Player", 
    fighter=Fighter(energy=100),
    ai_cls=OtherPerson,
    
)

# me = Entity(char="o", color=(63, 127, 63), name="You", blocks_movement=True)

