from Directions import Direction
from Creature import Creature

class Location():

    def __init__(self,name,descirption) -> None:
        self.name = name
        self.description = descirption
        self.doors = dict()
        self.creatures = list()
        self.items = list()

    def connect(self,direction,location):

        if self.has_door(direction) or location==None:
            return

        self.doors[direction] = location
        oppositeLocation = Direction.get_opposite_direction(direction)
        location.connect(oppositeLocation,self)

    def has_door(self,direction):
        return direction in self.doors and self.doors[direction] is not None

    def get_item(self,item_name):
        for item in self.items:
            if item.name == item_name:
                return item
        return None
    
    def has_creature(self,creature_name):
        return self.get_creature(creature_name) is not None

    def get_creature(self,creature_name):
        for creature in self.creatures:
            if creature.nick_name == creature_name:
                return creature
        return None

    def remove_item(self,item):
        self.items.remove(item)

    def get_connected_location(self,direction):
        if self.has_door(direction):
            return self.doors[direction]
        return None

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description 
    
    def set_name(self,name):
        self.name = name 

    def set_description(self,description):
        self.description = description 

    def set_creatures(self,creatures):
        self.creatures = creatures
    
    def set_items(self,items):
        self.items = items

    def add_creature(self,creature):
        self.creatures.append(creature)
    
    def remove_creature(self,creature):
        self.creatures.remove(creature)

    def add_item(self,item):
        self.items.append(item)

    def get_creature_names(self):
        creature_names =""
        for creature in self.creatures:
            if creature.__class__.__name__ != 'Pymon':
                creature_names += creature.nick_name

        return creature_names
    
    def get_pymon_names(self):
        creature_names =""
        for creature in self.creatures:
            if creature.__class__.__name__ == 'Pymon':
                creature_names += " "+creature.nick_name
        return creature_names

    def get_item_names(self):
        item_names = " ".join(item.name for item in self.items)
        return item_names
    
    def inspect(self):
        print(f"{self.name} has creatures {self.get_pymon_names()} {self.get_creature_names()} with {'items '+self.get_item_names() if len(self.get_item_names())>0 else ' no items'}")

    def connected_locations(self,direction):
        return self.doors

    



