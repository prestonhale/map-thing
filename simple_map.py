import math

# TODO Features:
# Player position on map
# Discover areas as the player progresses
# Doors that appear on map

# TODO:
# Remove extraneous horizontal connectors
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

    # creates a "Position" from a string like "2, 3"
    @staticmethod
    def from_string(input_string):
        x, y = input_string.split(",")
        int_x = int(x.strip())
        int_y = int(y.strip())
        return Position(int_x, int_y)
    
    def forward(self):
        return Position(self.x, self.y + 1)

    def backward(self):
        return Position(self.x, self.y - 1)

    def left(self):
        return Position(self.x - 1, self.y)

    def right(self):
        return Position(self.x + 1, self.y)

class Map:
    def display(self):
        empty = "".center(5)
        vertical_connector = "|".center(5)
        room = "o".center(5, "-")
        print(empty + room + empty)
        print(empty + vertical_connector + empty)
        print(room + room + room)
        print(empty + vertical_connector + empty)
        print(empty + room + empty)
    
    # Room Interface
    # left
    # right
    # forward
    # back 
    def generate_map_from_first_room(self, first_room):
        # =====================================================================
        # Generate a dictionary mapping string describing a position to strings
        # describing a room
        # 
        # E.g. {"0, 4": "connector"}
        # =====================================================================
        map_dict = {}
        queue = [(Position(0,0), first_room)]

        while len(queue) > 0:
            print("=====")
            for (b, v) in queue:
                print(f"{b}, {v}")
            # Add room to dictionary of positions
            cur_pos, cur_room = queue.pop()
            map_dict[str(cur_pos)] = "room"

            # Add connectors to dictionary of positions
            # also add connected rooms to "to-do" list
            # TODO: Ugly
            if str(cur_pos.forward()) not in map_dict and cur_room.forward is not None:
                map_dict[str(cur_pos.forward())] = "connector"
                queue.append((cur_pos.forward().forward(), cur_room.forward))
            if str(cur_pos.backward()) not in map_dict and cur_room.backward is not None:
                map_dict[str(cur_pos.backward())] = "connector"
                queue.append((cur_pos.backward().backward(), cur_room.backward))
            if str(cur_pos.right()) not in map_dict and cur_room.right is not None:
                map_dict[str(cur_pos.right())] = "connector"
                queue.append((cur_pos.right().right(), cur_room.right))
            if str(cur_pos.left()) not in map_dict and cur_room.left is not None:
                map_dict[str(cur_pos.left())] = "connector"
                queue.append((cur_pos.left().left(), cur_room.left))

        print(map_dict)
        # =====================================================================
        # Turn map dictionary into a 2d array that represents the map
        # TODO: I hate using strings here, look into python "enums"``
        # 
        # E.g. 
        # [
        #   ["empty", "empty", "room", "empty", "empty"],
        #   ["room", "connector", "room", "connector", "room"],
        #   ["empty", "empty", "room", "empty", "connector"],
        #   ["empty", "empty", "room", "empty", "room"],
        #   ["empty", "empty", "room", "empty", "empty"],`
        #   ["empty", "empty", "room", "connector", "room"]
        # ]
        # =====================================================================
        
        # Get the height and width of the map by finding the mininum and
        # maximum x and y value
        # Why do we do this? We're going to index into an array. Array indices
        # can't be negative.
        # TODO: This generally feels gross but I don't know why?
        min_x = math.inf
        max_x = -math.inf
        min_y = math.inf
        max_y = -math.inf
        for key in map_dict.keys():
            position = Position.from_string(key)
            if position.x > max_x:
                max_x = position.x
            if position.x < min_x:
                min_x = position.x
            if position.y > max_y:
                max_y = position.y
            if position.y < min_y:
                min_y = position.y
        height = (max_y - min_y) + 1 # Off by one, I am dumb
        width = (max_x - min_x) + 1
        print(height)
        print(width)
            



# =============================================================================
#                                       Test
# =============================================================================
class Room:
    forward = None
    backward = None
    left = None
    right = None

first = Room()
second = Room()
third = Room()
fourth = Room()
fifth = Room()

first.forward = second
second.backward = first

second.left = third
third.right = second

second.right = fourth
fourth.left = second

second.forward = fifth
fifth.backward = second

map = Map()
map.generate_map_from_first_room(first)
# map.display()