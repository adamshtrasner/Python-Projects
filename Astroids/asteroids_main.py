import random
import sys, math


from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo


DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    """
    A GameRunner object.
    The main runner of the Asteroids Game.
    The object gets a screen with maximum and minimum
    x and y coordinates which are the screen's limit.
    The game starts with an initial 0 score, a ship(a Ship object) and
    asteroids(a Asteroid object). The number of asteroids is being set according to the
    player's input. The default choice is 5 asteroids.
    The ship can shoot torpedoes(a Torpedo object).
    The purpose of the game is to shoot all of the asteroids in the screen
    (If the screen has no asteroids - you win the game).
    if the ship intersects with an asteroid more than 2 times, You lose the game.
    """

    def __init__(self, asteroids_amount=5):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = Ship(self.get_random_x(), 0, self.get_random_y(), 0)
        self.__life = 3
        self.__score = 0
        self.__torpedo_lst = []
        self.__asteroid_lst = []
        self.add_asteroids(asteroids_amount)

    def add_asteroids(self, asteroids_amount):
        """
        The program registers the asteroids to the screen according to the given number.
        :param asteroids_amount: the number of asteroids
        """
        for i in range(asteroids_amount):
            self.__asteroid_lst.append(Asteroid(self.get_random_x(), random.randint(1, 5), self.get_random_y()
                                                , random.randint(1, 5), 3))
            if self.__asteroid_lst[i].has_intersection(self.__ship):
                self.__asteroid_lst.pop()
                i -= 1
            else:
                self.__screen.register_asteroid(self.__asteroid_lst[i], 3)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()


    def _game_loop(self):
        """
        The main loop of the game.
        checks if there are no asteroids,
        if the player pressed the 'q' button(wants to quit),
        moves the ojects according to the pressed key,
        checks intersections between the objects,
        add torpedoes and removes asteroids accordingly.
        """
        self.if_no_asteroids()
        self.if_quit_game()
        self.move_objects()
        self.if_add_torpedo()
        self.subtract_life_span()
        self.check_intersection()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def move_objects(self):
        """
        The program moves the objects in the screen
        """
        self.move_ship()
        if self.__asteroid_lst:
            self.move_asteroids()
        if self.__torpedo_lst:
            self.move_torpedo()

    def get_random_x(self):
        """
        :return: a random x coordinate
        """
        return random.randint(self.__screen_min_x, self.__screen_max_x)

    def get_random_y(self):
        """
        :return: a random y coordinate
        """
        return random.randint(self.__screen_min_y, self.__screen_max_y)

    def move_ship(self):
        """
        The program moves the ship according to the pressed
        keys and draw it to the screen
        """
        if self.__screen.is_left_pressed():
            self.__ship.change_heading_left()

        if self.__screen.is_right_pressed():
            self.__ship.change_heading_right()

        if self.__screen.is_up_pressed():
            self.__ship.accelerate()

        self.__ship.move_in_x(self.__screen_min_x, self.__screen_max_x)
        self.__ship.move_in_y(self.__screen_min_y, self.__screen_max_y)
        self.__screen.draw_ship(self.__ship.get_location_x(), self.__ship.get_location_y(), self.__ship.get_heading())

    def move_asteroids(self):
        """
        The program moves the asteroids and draws them in the screen.
        """
        for asteroid in self.__asteroid_lst:
            asteroid.move_in_x(self.__screen_min_x, self.__screen_max_x)
            asteroid.move_in_y(self.__screen_min_y, self.__screen_max_y)
            self.__screen.draw_asteroid(asteroid, asteroid.get_location_x(), asteroid.get_location_y())

    def move_torpedo(self):
        """
        The program moves the torpedo and draws it to the screen.
        """
        for torpedo in self.__torpedo_lst:
            torpedo.move_in_x(self.__screen_min_x, self.__screen_max_x)
            torpedo.move_in_y(self.__screen_min_y, self.__screen_max_y)
            self.__screen.draw_torpedo(torpedo, torpedo.get_location_x(), torpedo.get_location_y(),
                                       torpedo.get_heading())

    def check_intersection(self):
        """
        The program checks if there's an intersection between the ship
        and an asteroid and if a torpedo is being shot - if there's
        an intersection between a torpedo and an asteroid.
        """
        if self.check_ship_intersection():
            if not self.ship_intersection():
                self.__screen.end_game()
                sys.exit()
        self.check_torpedo_intersection()

    def check_ship_intersection(self):
        """
        :return: return True if the ship hits an asteroid,
        False otherwise.
        """
        for asteroid in self.__asteroid_lst:
            if asteroid.has_intersection(self.__ship):
                self.__asteroid_lst.remove(asteroid)
                self.__screen.unregister_asteroid(asteroid)
                return True
        return False

    def ship_intersection(self):
        """
        :return: True if the ship has more lives to play with,
        False otherwise(the ship has 0 lives - you lose the game)
        """
        self.__life -= 1
        self.__screen.remove_life()
        if self.__life == 0:
            self.__screen.show_message("The ship got crushed", "You've lost the game!")
            return False
        self.__screen.show_message("The ship got crushed!", "You lost 1 soul")
        return True

    def check_torpedo_intersection(self):
        """
        The program checks if a torpedo hits an asteroid.
        If so, it removes the torpedo from the torpedo list.
        It also removes the torpedo is its life span is 0.
        """
        for asteroid in self.__asteroid_lst:
            for torpedo in self.__torpedo_lst:
                if asteroid.has_intersection(torpedo):
                    self.torpedo_intersection(asteroid, torpedo)
                # added: life span of a torpedo
                else:
                    if torpedo.get_life_span() == 0:
                        self.__torpedo_lst.remove(torpedo)
                        self.__screen.unregister_torpedo(torpedo)

    def torpedo_intersection(self, asteroid, torpedo):
        """
        :param asteroid: An Asteroid object.
        :param torpedo: A torpedo object.
        The program unregisters the specific torpedo from the screen
        and divides the asteroid accordingly (if the radius is l
        """
        self.__torpedo_lst.remove(torpedo)
        self.__screen.unregister_torpedo(torpedo)
        self.__asteroid_lst.remove(asteroid)
        self.__screen.unregister_asteroid(asteroid)
        if asteroid.get_size() > 1:
            self.add_2_asteroid(asteroid, torpedo)
        self.update_score(asteroid.get_size())

    def add_2_asteroid(self, asteroid, torpedo):
        """
        The program divides an asteroid that's been hit into 2 asteroids,
        and register them to the screen.
        :param asteroid: An Asteroid object.
        :param torpedo: A Torpedo object.
        """
        size = asteroid.get_size() - 1
        loc_x = asteroid.get_location_x()
        loc_y = asteroid.get_location_y()
        new_speed_x = torpedo.get_speed_x() + asteroid.get_speed_x() / \
                      (asteroid.get_speed_x() ** 2 + asteroid.get_speed_y() ** 2) ** 0.5
        new_speed_y = torpedo.get_speed_y() + asteroid.get_speed_y() / \
                      (asteroid.get_speed_x() ** 2 + asteroid.get_speed_y() ** 2) ** 0.5
        self.__asteroid_lst.append(Asteroid(loc_x, new_speed_x, loc_y, - new_speed_y, size))
        self.__screen.register_asteroid(self.__asteroid_lst[-1], size)
        self.__screen.draw_asteroid(self.__asteroid_lst[-1], loc_x, loc_y)
        self.__asteroid_lst.append(Asteroid(loc_x, - new_speed_x, loc_y, new_speed_y, size))
        self.__screen.register_asteroid(self.__asteroid_lst[-1], size)
        self.__screen.draw_asteroid(self.__asteroid_lst[-1], loc_x, loc_y)

    def if_add_torpedo(self):
        """
        The program allows the ship to shoot torpedoes only if there
        are no more than 10 torpedoes on the screen.
        """
        if self.__screen.is_space_pressed():
            if len(self.__torpedo_lst) < 10:  # added: a limit of 10 torpedoes
                loc_x, speed_x, loc_y, speed_y, heading = self.get_torpedo_info()
                self.__torpedo_lst.append(Torpedo(loc_x, speed_x, loc_y, speed_y, heading))
                self.__screen.register_torpedo(self.__torpedo_lst[-1])
                self.__screen.draw_torpedo(self.__torpedo_lst[-1], loc_x, loc_y, heading)

    def subtract_life_span(self):
        """
        The program subtracts the life span of
        a torpedo by 1(each iteration of the game loop)
        """
        for torpedo in self.__torpedo_lst:
            if torpedo.get_life_span() == 0:
                self.__torpedo_lst.remove(torpedo)
                self.__screen.unregister_torpedo(torpedo)
            else:
                torpedo.subtract_life_span()

    def get_torpedo_speed(self):
        return self.__ship.get_speed_x() + 2 * math.cos(math.radians(self.__ship.get_heading())),\
               self.__ship.get_speed_y() + 2 * math.sin(math.radians(self.__ship.get_heading()))

    def get_torpedo_info(self):
        speed_x, speed_y = self.get_torpedo_speed()
        return self.__ship.get_location_x(), speed_x, self.__ship.get_location_y(), speed_y, self.__ship.get_heading()

    def if_no_asteroids(self):
        """
        If there are no more asteroids in the screen, the program ends the game.
        """
        if not self.__asteroid_lst:
            self.__screen.show_message("Win!", "Congratulations! You've won the game!")
            sys.exit()

    def if_quit_game(self):
        """
        If the player presses the 'q' button, The program ends the game.
        """
        if self.__screen.should_end():
            self.__screen.show_message("Exit", "Exit the game")
            sys.exit()

    def update_score(self, size):
        """
        :param size: the size of the asteroid.
        The program upgrades the score according to the size
        of the asteroid which had been hit.
        """
        if size == 3:
            self.__score += 20
        elif size == 2:
            self.__score += 50
        elif size == 1:
            self.__score += 100
        self.__screen.set_score(self.__score)




def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
