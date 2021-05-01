from __future__ import annotations

from typing import TYPE_CHECKING

from tasks import calcEnergy
import input_handles
from renderer import render_task
from scorekeeper import ScoreKeeper

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity
    from input_handles import TaskHandler, MainEventHandler
    


"""
Learning Python: 
@property decorator makes a method a property of the class.
Returns the private instance attribute value self.__XYZ. 
So, we can now use the XYZ() method as a property to get the value of the XYZ attribute.
"""

class Action:
    """ all subclasses must invoke a perform method that takes:
        @params: 
            - entity: thing that will be changed (either player or entities)
        
        engine:  the game engine context
    """
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """
        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.
        """
        raise NotImplementedError()
    



class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class GameModeAction(Action):
    def perform(self) -> None:
        return self.engine.rerender()
        #TODO: take set of entities and change color pallete based on game mode

class WaitAction(Action):
    def perform(self) -> None:
        pass

#super class that will hold the movement from the input handle
class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy
    
    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)
    
    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)
    
    #each subclass needs a perform method
    def perform(self) -> None:
        raise NotImplementedError()

#perform movement action if not blocking, else do initiate task 
class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        # dest_x = entity.x + self.dx
        # dest_y = entity.y + self.dy

        if self.target_actor:
            return InitiateAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

#equivalent of melee actions
class InitiateAction(ActionWithDirection):        
    
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            return  # No entity to attack.

        self.engine.event_handler=input_handles.TaskHandler(self.engine)
        target.fighter.energy -= 1 #energy of other people always is 1, as in one task per person 


#this is the action that lowers the players energy (or not) and adds to the score
class HandleTaskAction(Action): 
    """
        params:
        decision: accept task or not
        motivation: to calulcate energy gain/loss (from Task class)
        special: bool if you get energy, not lose
        T energy gain: to add to scorekeeper
    """
    def perform(self, decision: bool, motivation: int, t_energyGain: int, special: bool) -> None: 
        if decision:
            print("you accept the task")
            if not special: 
                energy = calcEnergy(motivation, special)
                self.entity.fighter.energy -= energy
                self.engine.message_log.add_message(f"you accept the task and lose -{energy} energy")
                
                #track how much energy spent in seek mode
                if self.engine.mode == "seek":
                    self.engine.scorekeeper.seek_energy_spent += energy

                self.engine.scorekeeper.score += energy

            else:
                energy = calcEnergy(motivation, special)
                self.entity.fighter.energy += energy
                self.engine.message_log.add_message(f"you accept the task and gain +{energy} energy")
            
            #HANDLING SCORE

            #add energy other person gains/loses to t_energy_gain score
            self.engine.scorekeeper.others_energy_gain += t_energyGain

            if t_energyGain < 0 and special:
                self.engine.scorekeeper.exploit += 1
            elif t_energyGain < 0 and not special:
                self.engine.scorekeeper.assistance += 1
            elif t_energyGain > 0 and special:
                self.engine.scorekeeper.mutual += 1
            else:
                self.engine.scorekeeper.reckless += 1
                        
        else:
            print("no")
            self.engine.message_log.add_message("you move onwards")
                
        self.entity.fighter.resume() #return back to playing
        # self.engine.event_handler=MainEventHandler(self.engine) #does same thing but as above

        print(self.engine.scorekeeper.score)
        
        

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy #dest_xy precalculates position of entity plus distance :)

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return #destination is blocked by entity

        
        self.entity.move(dx=self.dx, dy=self.dy)

