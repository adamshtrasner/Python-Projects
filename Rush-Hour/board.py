# FILE : board.py
# WRITER : Adam Shtrasner


from car import Car


class Board:
    """
    A board object.
    The board is constructed out of rows and columns.
    every location in the board represents a coordinate
    in which you can put a car object and move it
    accordingly (according to whether the locations are empty or not).
    The board also has a target location.
    """

    def __init__(self, rows=7, columns=7):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.rows = rows
        self.columns = columns
        self.cars = []
        self.board_list = [['_'] * self.columns for row in range(self.rows)]
        for i in range(len(self.board_list)):
            if i == self.target_location()[0]:
                self.board_list[i].append('X')

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
        board = ""
        for row in self.board_list:
            board = board + " ".join(row) + '\n'
        return board

    def update_board(self, car):
        """
        :param car: car object of car.
        This function updates the board according to the given car.
        """
        car_coords = car.car_coordinates()
        for coord in car_coords:
            self.board_list[coord[0]][coord[1]] = car.get_name()

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        cells = []
        for i in range(self.rows):
            for k in range(self.columns):
                cells.append((i, k))
        cells.append(self.target_location())
        return cells

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        poss_moves = []
        for car in self.cars:
            name = car.get_name()
            min_coord = car.car_coordinates()[0]
            coords = car.car_coordinates()
            max_coord = coords[len(coords) - 1]
            if car.possible_moves() == car.HORIZONTAL_MOVES:
                right, left = car.HORIZONTAL_MOVES['r'], car.HORIZONTAL_MOVES['l']
                if min_coord[1] != 0:
                    if self.cell_content((min_coord[0], min_coord[1] - 1)) == None:
                        poss_moves.append((name, 'l', left))
                if max_coord[1] != self.columns:
                    if self.cell_content((max_coord[0], max_coord[1] + 1)) == None:
                        poss_moves.append((name, 'r', right))
            if car.possible_moves() == car.VERTICAL_MOVES:
                up, down = car.VERTICAL_MOVES['u'], car.VERTICAL_MOVES['d']
                if min_coord[0] != 0:
                    if self.cell_content((min_coord[0] - 1, min_coord[1])) == None:
                        poss_moves.append((name, 'u', up))
                if max_coord[0] != self.rows - 1:
                    if self.cell_content((max_coord[0] + 1, max_coord[1])) == None:
                        poss_moves.append((name, 'd', down))
        return poss_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3, 7)
        return (3, 7)

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        # implement your code and erase the "pass"
        row = coordinate[0]
        col = coordinate[1]
        if self.board_list[row][col] == '_' or self.board_list[row][col] == 'X':
            return None
        return self.board_list[row][col]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"
        for c in self.cars:
            if c.get_name() == car.get_name():
                return False
        car_coords = car.car_coordinates()
        for coord in car_coords:
            if coord == self.target_location():
                pass
            elif not (coord[0] < self.rows) or not (coord[1] < self.columns)\
                    or (self.cell_content(coord) != None) or (coord[0] < 0)\
                    or (coord[1] < 0):
                return False
        self.cars.append(car)
        self.update_board(car)
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        flag = False
        for car in self.cars:
            if name == car.get_name():
                c = car
                flag = True
                break
        if not flag:
            return False
        for moves in self.possible_moves():
            if moves[0] == name and moves[1] == movekey:
                for coord in c.car_coordinates():
                    self.board_list[coord[0]][coord[1]] = '_'
                for c1 in self.cars:
                    if name == c1.get_name():
                        self.cars.remove(c1)
                        break
                c.move(movekey)
                self.add_car(c)
                return True
        return False


