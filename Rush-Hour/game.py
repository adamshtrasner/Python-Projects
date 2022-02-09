# FILE : game.py
# WRITER : Adam Shtrasner

class Game:
    """
    A game object.
    This specific game object is about the "rush hour" game.
    The mission is to move cars objects in the board object
    and get one horizontal car in the target location.
    If you manage to to that - you win.
    """

    EXIT = '!'
    START_GAME = "Welcome to the 'rush hour' game!"
    CAR_INPUT = "Choose the car you want to move and the direction \n" \
                "you want to move it: 'name of car', 'direction': \n"
    INVALID_INPUT = "You chose an invalid input! \n type again or exit the game"
    INVALID_MOVE = "You tried to move a car that does not exist \n  or" \
                   "tried to move a car in an impossible way \n" \
                   "or tried to move a car to a place that is not empty. \n" \
                   "type again or exit the game"
    WIN_MSG = "You've won the game!"

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        # implement your code here (and then delete the next line - 'pass')
        self.board = board
        pass

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        # implement your code here (and then delete the next line - 'pass')
        target = self.board.target_location()
        win_coord = self.board.cell_content(target)
        if win_coord != None:
            if CARS_DICT[win_coord][2] == 1:
                return 1
        print("The valid inputs for cars are: \n" + str(CAR_COLOURS) + "And the valid"
                "directions are: \n 'u' - up, 'd' - down, 'l' - left, 'r' - right")
        move_car = input(self.CAR_INPUT)
        if move_car == self.EXIT:
            return -1
        name = move_car[0]
        direction = move_car[2]
        flag = False
        for key in CAR_COLOURS:
            if name == key:
                flag = True
                break
        if not flag:
            return -2
        if direction is not 'u' and direction is not 'd' and direction is not 'l' and direction is not 'r':
            return -2
        if self.board.move_car(name, direction):
            return 0
        return -3

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # implement your code here (and then delete the next line - 'pass')R
        print(self.START_GAME)
        while True:
            print(self.board)
            turn = self.__single_turn()
            if turn == -1:
                break
            if turn == -2:
                print(self.INVALID_INPUT)
            if turn == -3:
                print(self.INVALID_MOVE)
            if turn == 0:
                continue
            if turn == 1:
                print(self.WIN_MSG)
                break


if __name__ == "__main__":
    from board import Board
    from car import Car
    import sys, helper

    board = Board()
    CARS_DICT = helper.load_json(sys.argv[1])
    CAR_COLOURS = {'Y': "Yellow", 'B': "Blue", 'O': "Orange",
                   'W': "White", 'G': "Green", 'R': "Red"}
    for key in CARS_DICT:
        for k in CAR_COLOURS:
            if key == k:
                length = CARS_DICT[key][0]
                if length < 2 or length > 4:
                    break
                location = (CARS_DICT[key][1][0], CARS_DICT[key][1][1])
                orient = CARS_DICT[key][2]
                board.add_car(Car(key, length, location, orient))
            else:
                pass
    game = Game(board)
    game.play()
