from entity import Entity
import names

def getName():
    return names.get_last_name()

def getUniquePerson():
    return Entity(char="T", color=(63, 127, 63), name=getName(), blocks_movement=True)

player = Entity(char="@", color=(255, 255, 255), name="Player", blocks_movement=True)
me = Entity(char="o", color=(63, 127, 63), name="You", blocks_movement=True)

