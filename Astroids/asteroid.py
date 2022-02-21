class Asteroid:
    """
    An Asteroid Object.
    an asteroid has a location on the screen(x and y),
    has a speed(starts with speed - 0), a size and a radius.
    """

    def __init__(self, location_x, speed_x, location_y, speed_y, size):
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__size = size
        self.__radius = size * 10 - 5

    def get_location_x(self):
        """
        :return: location of the asteroid on the X axis.
        """
        return self.__location_x

    def get_location_y(self):
        """
        :return: location the the asteroid on the Y axis.
        """
        return self.__location_y

    def get_size(self):
        """
        :return: size of the asteroid.
        """
        return self.__size

    def get_radius(self):
        """
        :return: radius of the asteroid.
        """
        return self.__radius

    def get_speed_x(self):
        """
        :return: speed of the asteroid on the x axis.
        """
        return self.__speed_x

    def get_speed_y(self):
        """
        :return: speed of the asteroid in the Y axis.
        """
        return self.__speed_y

    def move_in_x(self, min_x, max_x):
        """
        Changes the location of the asteroid on the x axis.
        :param min_x: minimum limit of the screen in the x axis.
        :param max_x: maximum limit of the screen in the x axis.
        """
        new_spot = min_x + (self.__location_x + self.__speed_x - min_x) % (max_x - min_x)
        self.__location_x = new_spot

    def move_in_y(self, min_y, max_y):
        """
        Changes the location of the asteroid on the y axis.
        :param min_y: minimum limit of the screen in the y axis.
        :param max_y: maximum limit of the screen in the y axis.
        """
        new_spot = min_y + (self.__location_y + self.__speed_y - min_y) % (max_y - min_y)
        self.__location_y = new_spot

    def has_intersection(self, obj):
        """
        :param obj: An object of ship or torpedo.
        :return returns True if the object hit the asteroid,
        False otherwise.
        """
        distance = ((obj.get_location_x() - self.__location_x)
                    ** 2 + (obj.get_location_y() - self.__location_y) ** 2) ** 0.5
        if distance <= self.__radius + obj.get_radius():
            return True
        return False

