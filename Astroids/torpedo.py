class Torpedo:
    """
    a torpedo object
    it has a location which is coordinate (x,y) on a graph
    it has a speed on each axis and heading which is the direction of torpedo's head
    and a radius of the torpedo to know if something get crushed with the torpedo
    """
    def __init__(self, location_x, speed_x, location_y, speed_y, heading):
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__heading = heading
        self.__radius = 4
        self.__life_span = 200

    def get_location_x(self):
        """
        :return: the location ot the object on the x axis
        """
        return self.__location_x

    def get_location_y(self):
        """
        :return:the location ot the object on the y axis
        """
        return self.__location_y

    def get_speed_x(self):
        """
        :return:the speed of the torpedo on the x axis
        """
        return self.__speed_x

    def get_speed_y(self):
        """
        :return:the speed of the torpedo on the y axis
        """
        return self.__speed_y

    def get_heading(self):
        """
        :return:the direction of the torpedo's movement
        """
        return self.__heading

    def get_radius(self):
        """
        :return: radius of the torpedo
        """
        return self.__radius

    def get_life_span(self):
        """
        :return: how many loops the torpedo done the maximum is 200
        """
        return self.__life_span

    def move_in_x(self, min_x, max_x):
        """
        changing the location of the ship on x axis
        :param min_x: the minimum limit of the screen in the x coordinate
        :param max_x: the miaximum limit of the screen in the x coordinate
        """
        new_spot = min_x + (self.__location_x + self.__speed_x - min_x) % (max_x - min_x)
        self.__location_x = new_spot

    def move_in_y(self, min_y, max_y):
        """
        changing the location of the ship on x axis
        :param min_y: the minimum limit of the screen in the y coordinate
        :param max_y: the maximum limit of the screen in the y coordinate
        """
        new_spot = min_y + (self.__location_y + self.__speed_y - min_y) % (max_y - min_y)
        self.__location_y = new_spot

    def subtract_life_span(self):
        """
        subtract the life spans of the torpedo
        """
        self.__life_span -= 1


