class Item():

    def __init__(self,name,description,pickable,consumable) -> None:
        self.name = name
        self.description = description
        self.pickable = pickable
        self.consumable = consumable
    
    def is_pickable(self):
        if self.pickable == 'yes':
            return True
        return False
    
    def is_consumable(self):
        if self.consumable == 'yes':
            return True
        return False
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
        