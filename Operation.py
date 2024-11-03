from Directions import Direction
import sys
from Exceptions import ChallengeLostException
from Exceptions import NoPymonsLeft
from Record import Record
from Pymon import Pymon
class Operation():

    def __init__(self):
        self.setup()
        self.pets = [self.pymon]
        self.current_pymon = self.pets[0]
        self.record = Record()
        self.moves_made = 0

    def show_menu(self):
        print("Please issue a command to your pymon ")
        print("1) Inspect pymon")
        print("2) Inspect current location")
        print("3) move")
        print("4) Pick an Item ")
        print("5) View Inventory ")
        print("6) Challenge a creature ")
        print("7) Exit the program ")

    def setup(self):
        self.pymon = Pymon('kimimon','a starter pymon')
        record = Record()
        self.locations = record.get_locations()
        record.spwan_creature_to_random_location(self.pymon)

    def start_game(self):
        self.show_menu()
        self.take_command_until_exit()

    def print_pets_name(self):
        if len(self.pets) == 0:
            print("You dont have any pets")

        for pet in self.pets:
            print(pet.nick_name,end=" ")
            print()

    def get_pet(self,pet_name):
        for pet in self.pets:
            if pet.nick_name == pet_name:
                return pet
        return None

    def has_pet(self,pet_name):
        return self.get_pet(pet_name) is not None 
    
    def operate(self,command):
        if command==1:
            print("\t 1) inspect current pymon ")
            print("\t 2) List and select a benched Pymon to use : ")
            option = int(input("select an option "))
            if option == 1:
                self.inspect_pymon()
            elif option == 2:
                self.print_pets_name()
                pymon_name_to_swap = input("Enter a pymon name to swap ")
                if not self.has_pet(pymon_name_to_swap):
                    print(f"You dont have {pymon_name_to_swap} with you")
                else:
                    pymon_to_swap = self.get_pet(pymon_name_to_swap)
                    self.current_pymon = pymon_to_swap

        elif command==2:
            self.inspect_location()
        elif command==3:
            self.move_pymon()
        elif command==4:
            self.pick_an_item()
        elif command==5:
            self.view_pymon_inventory()
            if not self.current_pymon.is_inventory_empty():
                print("\t a) Select an item to use  ")
                option = input("enter item name (n to cancel) : ")
                if option!='n':
                    self.select_item_to_use(option)

        elif command==6:
            self.challenge_creature()
        elif command==7:
            self.exit_game()
        else:
            print('Please provide a valid command')
    
    def select_item_to_use(self,item_name):
        if not self.current_pymon.is_inventory_empty() and len(self.current_pymon.get_non_battle_items()) !=0:
            item = self.current_pymon.get_item(item_name)
            self.current_pymon.use_item(item)

    def take_command_until_exit(self):
        while(True):
            try:
                command = int(input("Your command: "))
                self.operate(command)
            except Exception as e:
                self.show_menu()
                print(f"Enter a valid command {e}")

    def exit_game(self):
        sys.exit()

    def inspect_pymon(self):
        self.current_pymon.inspect()

    def view_pymon_inventory(self):
        if self.current_pymon.is_inventory_empty():
            print("No items in the inventory")
        else:
            self.current_pymon.view_inventory()
    
    def inspect_location(self):
        self.current_pymon.inspect_current_location()

    
    def challenge_creature(self):
        creature_name = input("Challenge who:")
        current_location = self.current_pymon.get_current_location()
        creature_exists = current_location.has_creature(creature_name)

        if creature_exists:
            print(f"{creature_name} gladly accpeted your challenge! Ready for battle!")
            print("The first pymon to win 2 of encounters will win the battle")
            try:
               captured_creature =  self.current_pymon.challenge(creature_name)
               self.add_pymon(captured_creature)
               print(f"Congrats! You have won the battle and adopted a new Pymon called {creature_name}!")
            except Exception:
                print("You have lost the challenge and lost your pymon")
                self.remove_current_pymon()
        else:
            print(f"Creature doesn't exist in {self.current_pymon.get_current_location().get_name()}")
                
    def add_pymon(self,pymon):
        self.pets.append(pymon)
        location = self.current_pymon.get_current_location()
        location.remove_creature(pymon)

    def remove_current_pymon(self):
        self.pets.remove(self.current_pymon)
        self.record.spwan_creature_to_random_location(self.current_pymon)
        print(f"{self.current_pymon.nick_name} has fled ")
        if len(self.pets)==0:
            print("You have no more pymons with you ")
            print("You lost the game")
            sys.exit()
        else:
            self.current_pymon = self.pets[0]
            print(f"Your new pymon is {self.current_pymon.nick_name}")

    def pick_an_item(self):
        item_name = input("Picking what:")
        try:
            self.current_pymon.pick_an_item(item_name)
            print(f"You picked up {item_name} from the ground")
        except:
            print("Item is not pickable")

    def move_pymon(self):
        direction = input("Moving to which direction?:")
        is_valid_direction = Direction.validate_direction(direction)
        current_location = self.current_pymon.get_current_location()
        is_location_connected = current_location.has_door(direction)
        if(is_valid_direction and is_location_connected):
            self.moves_made+=1
            for pet in self.pets:
                pet.move(direction)
            if(self.moves_made%2==0):
                self.current_pymon.decrease_energy()
            if(self.current_pymon.energy==0):
                print(f"{self.current_pymon.nick_name} is out of energy ")
                self.remove_current_pymon()

            print(f"You travelled {direction} and arrived at {self.current_pymon.get_current_location().get_name()}")
        else:
            print(f"There is no door to the {direction}. Pymon remains at its current location")
    

    
