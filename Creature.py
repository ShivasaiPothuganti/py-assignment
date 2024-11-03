class Creature():

    def __init__(self,nick_name,description) -> None:
        self.nick_name = nick_name
        self.description = description

    def spawn(self,location):
        location.add_creature(self)
        self.current_location = location

    def get_current_location(self):
        return self.current_location
    
    def get_description(self):
        return self.descripion
    
    def get_nick_name(self):
        return self.nick_name
    
    def set_current_location(self,location):
        self.current_location = location
    
    def get_description(self,description):
        self.descripion = description
    
    def get_nick_name(self,nick_name):
        self.nick_name = nick_name

    def inspect(self):
        print(f"Hi Player , my name is {self.nick_name}, {self.descripion}")


    