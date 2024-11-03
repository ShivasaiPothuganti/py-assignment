class Direction():
    EAST = "east"
    WEST = "west"
    NORTH = "north"
    SOUTH = "south"

    def get_opposite_direction(direction):
        if(direction==Direction.EAST):
            return Direction.WEST
        elif(direction==Direction.WEST):
            return Direction.EAST
        elif(direction==Direction.NORTH):
            return Direction.SOUTH
        elif(direction==Direction.SOUTH):
            return Direction.NORTH
        else:
            raise Exception("Invalid direction")

    def validate_direction(direction):
        if direction in [Direction.EAST,Direction.WEST,Direction.NORTH,Direction.SOUTH]:
            return True
        return False   
        
        