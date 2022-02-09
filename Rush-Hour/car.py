# FILE : car.py
# WRITER : Adam Shtrasner


MOVE_RIGHT = 'r'
MOVE_LEFT = 'l'
MOVE_UP = 'u'
MOVE_DOWN = 'd'
HORIZONTAL = 1
VERTICAL = 0
class Car:
    """
    A car object.
    The car has a name according to its colour,
    length, location and orientation.
    The car object allows us to get its coordinates,
    move the car according to the possible moves and the movement's
    requirement, and get its name.
    """
    HORIZONTAL_MOVES = {'l': "You may move the car to the Left",
                        'r': "You may move the car to the right"}

    VERTICAL_MOVES = {'u': "You may move the car upwards",
                      'd': "You may move the car downwards"}

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        # implement your code and erase the "pass"
        self.name = name
        self.length = length
        self.location = location
        if orientation == 1 or orientation == 0:
            self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        length = self.length
        location = self.location
        coordinates = [location]
        row = location[0]
        col = location[1]
        if self.orientation == 0:
            # The orientation of the car is vertical
            for i in range(1, length):
                row += 1
                coordinates.append((row, location[1]))
            return coordinates
        if self.orientation == 1:
            # The orientation of the car is horizontal
            for k in range(1, length):
                col += 1
                coordinates.append((location[0], col))
            return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.
        if self.orientation == 0:
            return self.VERTICAL_MOVES
        return self.HORIZONTAL_MOVES


    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        coordinates = self.car_coordinates()
        min_coordinates = self.location
        max_coordinates = coordinates[len(coordinates) - 1]
        if movekey == 'u':
            return [(min_coordinates[0] - 1, min_coordinates[1])]
        if movekey == 'd':
            return [(max_coordinates[0] + 1, max_coordinates[1])]
        if movekey == 'r':
            return [(max_coordinates[0], max_coordinates[1] + 1)]
        if movekey == 'l':
            return [(min_coordinates[0], min_coordinates[1] - 1)]

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if (movekey is not MOVE_RIGHT and movekey is not MOVE_LEFT
            and movekey is not MOVE_DOWN and movekey is not MOVE_UP):
            return False
        req = self.movement_requirements(movekey)
        coord = req[0]
        if self.orientation == HORIZONTAL:
            if movekey == MOVE_RIGHT:
                self.location = (coord[0], coord[1] - (self.length - 1))
                return True
            if movekey == MOVE_LEFT:
                self.location = (coord[0], coord[1])
                return True
            return False
        if self.orientation == VERTICAL:
            if movekey == MOVE_UP:
                self.location = (coord[0], coord[1])
                return True
            if movekey == MOVE_DOWN:
                self.location = (coord[0] - (self.length-1), coord[1])
                return True
            return False


    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name
