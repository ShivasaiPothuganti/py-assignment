from Creature import Creature
import random
from Enums.Outcome import Outcome
from Exceptions import ChallengeLostException
class Pymon(Creature):

    def __init__(self, nick_name, description) -> None:
        super().__init__(nick_name, description)
        self.energy = 3
        self.inventory = list()
        self.immunity = False
        self.battle_mode = False

    def pick_an_item(self,item_name):
        item = self.current_location.get_item(item_name)
        if item is not None and item.is_pickable():
            self.inventory.append(item)
            self.current_location.remove_item(item)
        else:
            raise Exception("Item is not pickable")
        
    def view_inventory(self):
        item_names = " ".join(item.name for item in self.inventory)
        print(f'You are carrying : {item_names}')

    def get_item(self,item_name):
        for item in self.inventory:
            if item.name == item_name:
                return item
        return None
    
    def use_item(self,item):

        if not self.has_item(item.name):
            print(f"You dont have {item.name} in your inventory")
            return

        if item.consumable == 'yes':
            if item.name == 'apple':
                if self.energy<3:
                    print("energy increased by one point")
                    self.increase_energy()
                else:
                    print("Energy is full")
                    
                self.remove_item(item)
            elif item.name=='potion':
                if self.battle_mode:
                    print("Your immunity is activated ")
                    self.immunity = True
                    self.remove_item(item)
                else:
                    print("Can only be used in a battle")

        elif item.name =='binocular':

            print("Please select one of the options :")
            print(" current")
            print(" north")
            print(" east")
            print(" west")
            print(" south")
            selected_direction = input("Enter your direction here : ")
            if selected_direction not in ['current','north','east','west','south']:
                print("Invalid selection")
            else:
                self.peek_to_direction(selected_direction)

    def has_item(self,item_name):
        return self.get_item(item_name) is not None
    
    def peek_to_direction(self,selected_direction):
        items = self.current_location.get_item_names()
        creature_names = self.current_location.get_creature_names()
        pymon_names = self.current_location.get_pymon_names()

        locations_in_all_directions =  "" 
        for direction,location in self.current_location.doors.items():
            locations_in_all_directions+=' '+f'in the {direction} is a {location.name}'

        if selected_direction == 'current':
            print(f'A {creature_names}, {pymon_names},with items {items} and{locations_in_all_directions}')
        else:
            if not self.current_location.has_door(selected_direction):
                print("This direction leads no where")
            else:
                doors = self.current_location.doors;
                item_names_of_location = doors[selected_direction].get_item_names()
                creature_names_of_location = doors[selected_direction].get_creature_names()
                print(f"In the {selected_direction} There seems to be a {doors[selected_direction].name} with { item_names_of_location if len(item_names_of_location)>0 else 'no items' } , and {creature_names_of_location if len(creature_names_of_location)>0 else 'no creatures'} , ")


    
    def challenge(self,creature_name):
        encounters_won = 0
        allowed_encounters_to_loose = 2
        encounters_lost =0
        total_encounters = 0
        max_encounters = 3
        creature = self.current_location.get_creature(creature_name)
        print("First encounter!")
        self.battle_mode = True
        while self.energy >0 and total_encounters < max_encounters:
            
            if not self.immunity and self.has_item('potion'):
                use_potion = input("You have magic potion , do you want to use it (y/n) : ")
                if use_potion=="y":
                    magical_potion = self.get_item('potion')
                    self.use_item(magical_potion)
                    allowed_encounters_to_loose+=1
                    max_encounters = 4

            pymon_move = self.__choose_move()
            print(f"you issued {pymon_move}!")
            wild_pymon_move = self.__choose_move_for_wild_pymon()
            print(f"your opponent issued {wild_pymon_move}")
            battle_result = self.get_battle_result(pymon_move,wild_pymon_move)
            if battle_result == Outcome.TIE:
                print(f"{pymon_move} vs {wild_pymon_move}, Draw no one wins")
                continue
            elif battle_result == Outcome.PYMON_WINS:
                encounters_won+=1
                print(f"{pymon_move} vs {wild_pymon_move}: {pymon_move} wins! You won {encounters_won} encounter")
            else:
                encounters_lost += 1
                print("setting allowed encounters ",allowed_encounters_to_loose)
                allowed_encounters_to_loose -= 1
                print("allowed encounters to loose",allowed_encounters_to_loose)
                if not self.immunity: 
                    self.decrease_energy()
                    print(f"{pymon_move} vs {wild_pymon_move}: {wild_pymon_move} wins! You lost {encounters_lost} encounter and 1 energy")
                else:
                    self.immunity = False
                    print(f"{pymon_move} vs {wild_pymon_move}: {wild_pymon_move} wins! You lost {encounters_lost} encounter")
             

            total_encounters+=1
            
            if encounters_won == 2:
                return creature
            elif allowed_encounters_to_loose == 0:
                raise ChallengeLostException()
        
        self.battle_mode = False

    def  get_battle_result(self,pymon_move,wild_pymon_move):
        if pymon_move == wild_pymon_move:
            return Outcome.TIE
        elif (pymon_move == 'rock' and wild_pymon_move == 'scissor') or (pymon_move=='papper' and wild_pymon_move=='rock') or (pymon_move=='scissor' and wild_pymon_move=='papper'):
            return Outcome.PYMON_WINS
        else:
            return Outcome.WILD_PYMON_WINS

    def remove_item_by_name(self,item_name):
        item = self.get_item(item_name)
        self.remove_item(item)

    def remove_item(self,item):
        if item is not None:
            self.inventory.remove(item)

    def __choose_move(self):
        while True:
            pymon_move = input("Your turn (r)ock), (p)aper), or (s)cissor? :")
            if pymon_move not in ['r','p','s']:
                print("invalid move choose again")
            else:
                return self.get_relavant_move(pymon_move)

    def get_relavant_move(self,move_name):
        if move_name=='p':
            return 'papper'
        elif move_name=='r':
            return 'rock'
        else:
            return 'scissor'
            
    def __choose_move_for_wild_pymon(self):
        return random.choice(['rock','papper','scissor'])
    
        
    def is_inventory_empty(self):
        return len(self.inventory) == 0

    def move(self,direction):
        if direction in self.current_location.doors:
            new_location = self.current_location.doors[direction]
            new_location.add_creature(self)
            self.current_location.creatures.remove(self)
            self.current_location = new_location

    def increase_energy(self,energy=1):
        if(self.energy<3):
            self.energy += energy


    def get_non_battle_items(self):
        non_battle_items = []
        for item in self.inventory:
            if item.name != 'potion':
                non_battle_items.append(item)
        return non_battle_items

    def decrease_energy(self,energy=1):
        if(self.energy>0):
            self.energy -= energy

    def set_energy(self,energy):
        self.energy = energy

    def inspect(self):
        print(f"Hi player, my name is {self.nick_name}, I am {self.description}.\nMy energy level is {self.energy}/3. What can I do to help you?")

    def inspect_current_location(self):
        print(f"You are at a {self.current_location.get_name()}, {self.current_location.get_description()}")
        self.current_location.inspect()