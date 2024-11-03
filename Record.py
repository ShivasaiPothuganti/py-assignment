from csv import *
from Location import Location
from Directions import Direction
from Pymon import Pymon
from Item import Item
from Creature import Creature
import random

class Record():


    def __init__(self) -> None:

        self.locations = []
        self.items = []
        self.creatures = []

        self.load_locations()
        self.load_items()
        self.load_creatures()
        self.set_items_to_locations()
        self.set_creatures_to_locations()

    def load_pymon(self):
        pymon = Pymon('kinimon','white and yellow with a square face.')
        pymon.spawn(self.playground)
        return pymon

    def load_locations(self):

        file_name = "locations.csv"
        with open(file_name,mode='r') as file:
            rows = file.readlines()
            for index in range(1,len(rows)):
                current_row = [data.strip() for data in rows[index].split(',')]
                location_name = current_row[0]
                description = current_row[1]
                west_location = self.get_location_by_name(current_row[2])
                north_location = self.get_location_by_name(current_row[3])
                east_location = self.get_location_by_name(current_row[4])
                south_location = self.get_location_by_name(current_row[5])


                location = Location(location_name,description)
                location.connect(Direction.WEST,west_location)
                location.connect(Direction.NORTH,north_location)
                location.connect(Direction.EAST,east_location)
                location.connect(Direction.SOUTH,south_location)
                self.locations.append(location)

        self.playground = self.get_location_by_name('Playground')
        self.beach = self.get_location_by_name('Beach')
        self.school = self.get_location_by_name('School')

    def load_items(self):

        file_name = "items.csv"
        with open(file_name,mode='r') as file:
            rows = file.readlines()
            for index in range(1,len(rows)):
                current_row = [data.strip() for data in rows[index].split(',')]
                item_name = current_row[0]
                description = current_row[1]
                pickable = current_row[2]
                consumable = current_row[3]
                
                item = Item(item_name,description,pickable,consumable)
                self.items.append(item)

        self.apple = self.get_item_by_name("apple")
        self.magic_potion = self.get_item_by_name("potion")
        self.binocular = self.get_item_by_name("tree")
        self.tree = self.get_item_by_name("binocular")


    def get_location_by_name(self,location_name):
        for location in self.locations:
            if location.name == location_name:
                return location
        return None
    
    def get_locations(self):
        return self.locations
    
    def get_item_by_name(self,item_name):
        for item in self.items:
            if item.name == item_name:
                return item
        return None

    def set_items_to_locations(self):
        self.playground.add_item(self.tree)
        self.playground.add_item(self.magic_potion)

        self.beach.add_item(self.apple)
        self.playground.add_item(self.binocular)

    def load_creatures(self):
        file_name = "creatures.csv"
        with open(file_name,mode='r') as file:
            rows = file.readlines()
            for index in range(1,len(rows)):
                current_row = [data.strip() for data in rows[index].split(',')]
                nick_name = current_row[0]
                description = current_row[1]
                adoptable = current_row[2]
                if adoptable == "yes":
                    pymon = Pymon(nick_name,description)
                    self.creatures.append(pymon)
                else:
                    creature = Creature(nick_name,description)
                    self.creatures.append(creature)


    def set_creatures_to_locations(self):
        for creature in self.creatures:
            self.spwan_creature_to_random_location(creature)
    
    def spwan_creature_to_random_location(self,creature):
        random_location = random.choice(self.locations)
        creature.spawn(random_location)


    def get_creature_by_name(self,creature_name):
        for creature in self.creatures:
            if creature.nick_name == creature_name:
                return creature
        return None