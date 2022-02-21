import math


class Ship:
    """
    an ship object
    it has a location which is a coordinate on (x,y) axis
    it has a speed on each axis and heading which is the direction of ship's head
    and a radius of the ship to know if something get crushed with the ship
    """

    def __init__(self, location_x, speed_x, location_y, speed_y, heading=0):
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__heading = heading  # direction in degrees
        self.__radius = 1

    def move_in_x(self, min_x, max_x):
        """
        changing the location on the x axis
        :param min_x: the minimum limit of the screen in the x coordinate
        :param max_x:the maximum limit of the screen in the x coordinate
        """
        new_spot = min_x + (self.__location_x + self.__speed_x - min_x) % (max_x - min_x)
        self.__location_x = new_spot

    def move_in_y(self, min_y, max_y):
        """
        changing the location on the y axis
        :param min_y:the minimum limit of the screen in the y coordinate
        :param max_y:the maximum limit of the screen in the y coordinate
        """
        new_spot = min_y + (self.__location_y + self.__speed_y - min_y) % (max_y - min_y)
        self.__location_y = new_spot

    def change_heading_right(self):
        """
        moving the direction of the ship right
        """
        self.__heading -= 7

    def change_heading_left(self):
        """
        moving the direction of the ship right
        """
        self.__heading += 7

    def accelerate(self):
        """
        accelerate the ship
        :return:
        """
        new_speed_x = self.__speed_x + math.cos(math.radians(self.__heading))
        new_speed_y = self.__speed_y + math.sin(math.radians(self.__heading))
        self.__speed_x, self.__speed_y = new_speed_x, new_speed_y

    def get_location_x(self):
        """
        :return: the x of the coordinate location of the ship's location
        """
        return self.__location_x

    def get_location_y(self):
        """
        :return:the y of the coordinate location of the ship's location
        """
        return self.__location_y

    def get_heading(self):
        """
        :return: the direction of the ship's movement
        """
        return self.__heading

    def get_radius(self):
        """
        :return: radius of the ship
        """
        return self.__radius

    def get_speed_x(self):
        """
        :return: the speed of the ship on the x axis
        """
        return self.__speed_x

    def get_speed_y(self):
        """
        :return: the speed of the ship on the y axis
        """
        return self.__speed_y

    def get_torpedo_speed(self):
        """
        calculate the speed that needed for torpedo
        :return:
        """
        return self.__speed_x + 2 * math.cos(math.radians(self.__heading)),\
               self.__speed_y + 2 * math.sin(math.radians(self.__heading))

    def get_torpedo_info(self):
        """
        :return: the information that the game need for create torpedo
        """
        speed_x, speed_y = self.get_torpedo_speed()
        return self.get_location_x(), speed_x, self.get_location_y(), speed_y, self.get_heading()