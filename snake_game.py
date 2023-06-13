from typing import Optional
from game_display import GameDisplay
import argparse
from snake import *
from apple import *
from wall import *


class SnakeGame:
    def __init__(self, args: argparse.Namespace) -> None:
        """
        Init for SnakeGame object.
        :param args: Namespace of all the game arguments.
        """
        self.__is_snake = not args.debug
        if self.__is_snake:
            self.__snake = Snake(args.width, args.height)
        self.__width = args.width
        self.__height = args.height
        self.__walls = []
        self.__apples = []
        self.__game_board = [[None for _ in range(self.__height)] for _ in
                             range(self.__width)]
        self.__update_board()
        self.__walls_num = args.walls
        self.__apples_num = args.apples
        self.__round = 0
        self.__max_rounds = args.rounds
        self.__score = 0
        self.__suicide = False

    def read_key(self, key_clicked: Optional[str]) -> None:
        self.__key_clicked = key_clicked

    def update_objects(self) -> None:
        """
        Function handles all object interactions.
        """
        walls_locations = []
        if self.__is_snake:
            if self.__key_clicked == 'Left':
                self.__snake.set_orientation('Left')
            if self.__key_clicked == 'Right':
                self.__snake.set_orientation('Right')
            if self.__key_clicked == 'Up':
                self.__snake.set_orientation('Up')
            if self.__key_clicked == 'Down':
                self.__snake.set_orientation('Down')
            if not self.__snake.move():
                self.__suicide = True
        self.__update_board()
        if self.__round % 2 == 0 and self.__round != 0:
            for wall in self.__walls:
                wall.move()
        self.__remove_dead_walls()
        if len(self.__walls) < self.__walls_num and self.__round != 0:
            self.add_wall()
        self.__remove_dead_apples()
        if len(self.__apples) < self.__apples_num and self.__round != 0:
            self.add_apple()

        if self.__is_snake:
            for wall in self.__walls:
                walls_locations.append(wall.get_locations())
            snake_locations = self.__snake.get_locations()
            for wall in walls_locations:
                for snake_cell in snake_locations[2:]:
                    if snake_cell in wall:
                        self.__split_snake(snake_cell)
                        break

    def __split_snake(self, snake_cell) -> None:
        """
        Function splits the snake of the game
        :param snake_cell: The cell of collision between wall and snake
        """
        snake_locations = self.__snake.get_locations()
        i = snake_locations.index(snake_cell)
        length = len(snake_locations) - 1
        num_to_remove = length - i
        for x in range(num_to_remove):
            self.__snake.remove_tail()

    def are_empty_cells(self, cells_list) -> bool:
        """
        Function checks if a list of cells are in empty places
        :param cells_list: A list of cells
        :return: True if all cells are empty, False otherwise
        """
        for width, height in cells_list:
            if width > self.__width - 1 or width < 0 or height > \
                    self.__height - 1 or height < 0:
                continue
            if self.__game_board[width][height] is not None:
                return False
        return True

    def __generate_board(self) -> None:
        """
        Function generates a printable board of the game with all the
        objects placed on the board.
        """
        self.__game_board = [[None for _ in range(self.__height)] for _ in
                             range(self.__width)]
        # snake_locations = self.__snake.get_locations()
        walls_locations = []
        apples_locations = []
        for wall in self.__walls:
            walls_locations.append(wall.get_locations())
        for apple in self.__apples:
            apples_locations.append(apple.get_location())
        if self.__is_snake:
            snake_locations = self.__snake.get_locations()
            for width, height in snake_locations:
                if width > self.__width - 1 or width < 0 or height > \
                        self.__height - 1 or height < 0:
                    continue
                else:
                    self.__game_board[width][height] = "black"
        for wall in walls_locations:
            for width, height in wall:
                if width > self.__width - 1 or width < 0 or height > \
                        self.__height - 1 or height < 0:
                    continue
                else:
                    self.__game_board[width][height] = "blue"
        for width, height in apples_locations:
            self.__game_board[width][height] = "green"

    def __update_board(self) -> None:
        """
        Function updates the locations of the object on the board mid-round.
        """
        self.__game_board = [[None for _ in range(self.__height)] for _ in
                             range(self.__width)]
        # snake_locations = self.__snake.get_locations()
        walls_locations = []
        apples_locations = []
        for wall in self.__walls:
            walls_locations.append(wall.get_locations())
        for apple in self.__apples:
            apples_locations.append(apple.get_location())
        if self.__is_snake:
            snake_locations = self.__snake.get_locations()
            for width, height in snake_locations:
                if width > self.__width - 1 or width < 0 or height > \
                        self.__height - 1 or height < 0:
                    continue
                else:
                    self.__game_board[width][height] = "black"
        for wall in walls_locations:
            for width, height in wall:
                if width > self.__width - 1 or width < 0 or height > \
                        self.__height - 1 or height < 0:
                    continue
                else:
                    self.__game_board[width][height] = "blue"
        for width, height in apples_locations:
            self.__game_board[width][height] = "green"

    def __remove_dead_walls(self) -> None:
        """
        Function checks if any of the walls in the game are dead (0 length)
        and if a wall is dead it is removed.
        """
        all_cells = self.all_cells()
        for wall in self.__walls:
            wall_coordinates = wall.get_locations()
            wall_still_in = False
            for wall_cell in wall_coordinates:
                if wall_cell in all_cells:
                    wall_still_in = True
                    break
            if not wall_still_in:
                self.__walls.remove(wall)

    def __remove_dead_apples(self) -> None:
        """
        Function checks if any of the apples in the game are dead (eaten or
        passed on) and if an apple is dead it is removed.
        """
        if self.__is_snake:
            snake_locations = self.__snake.get_locations()
        all_walls_cells = []
        for wall in self.__walls:
            wall_coordinates = wall.get_locations()
            all_walls_cells.append(wall_coordinates)

        for apple in self.__apples:
            apple_still_okay = True
            apple_coordinates = apple.get_location()
            if self.__is_snake:
                if apple_coordinates in snake_locations:
                    apple_still_okay = False
                    self.__snake.grow(3)
                    self.__score += int(self.__snake.get_length()**0.5)
            for wall in all_walls_cells:
                if apple_coordinates in wall:
                    apple_still_okay = False
                    break
            if not apple_still_okay:
                self.__apples.remove(apple)

    def all_cells(self) -> list:
        """
        Function returns all the cells on the board.
        :return: A list of all the cells on the board.
        """
        all_cells = []
        for row in range(len(self.__game_board)):
            for col in range(len(self.__game_board[0])):
                all_cells.append((row, col))
        return all_cells

    def add_apple(self) -> None:
        """
        Function tried to add an apple to the game
        """
        apple = Apple()
        apple_loc = apple.get_location()
        if self.are_empty_cells([apple_loc]):
            self.__apples.append(apple)
            self.__update_board()

    def add_wall(self) -> None:
        """
        Function tries to add a wall to the game
        """
        wall = Wall(self.__width, self.__height)
        wall_loc = wall.get_locations()
        if self.are_empty_cells(wall_loc):
            self.__walls.append(wall)
            self.__update_board()

    def draw_board(self, gd: GameDisplay) -> None:
        """
        Function draws the game board to the screen
        :param gd: Game display object to print to screen
        """
        self.__generate_board()
        for col in range(len(self.__game_board)):
            for row in range(len(self.__game_board[0])):
                if self.__game_board[col][row] is not None:
                    gd.draw_cell(col, row, self.__game_board[col][row])

    def end_round(self) -> None:
        """
        Function keeps track of the amount of game iterations
        """
        self.__round += 1

    def is_over(self) -> bool:
        """
        Function checks if the game is over according to the rules.
        :return: True if game should end, False otherwise.
        """
        if self.__suicide:
            return True
        walls_locations = []
        if self.__max_rounds != -1:
            if self.__round == self.__max_rounds + 1:
                return True
        if self.__is_snake:
            snake_locations = self.__snake.get_locations()
            snake_head = snake_locations[0]
            snake_neck = snake_locations[1]
            for wall in self.__walls:
                walls_locations.append(wall.get_locations())
            for wall in walls_locations:
                if snake_head in wall or snake_neck in wall:
                    return True

            snake_head_x = snake_head[0]
            snake_head_y = snake_head[1]
            if snake_head_x > self.__width - 1 or snake_head_x < 0 or \
                    snake_head_y > self.__height - 1 or snake_head_y < 0:
                return True
            return False

    def get_num_apples(self) -> int:
        """
        Get the num of apples that should be on the board.
        :return: Num of apples that should be on board.
        """
        return self.__apples_num

    def get_apples(self) -> list:
        """
        :return: The list of apples on the board
        """
        return self.__apples

    def get_walls_num(self) -> int:
        """
        :return: The amount of walls that should be on board.
        """
        return self.__walls_num

    def get_walls(self) -> list:
        """
        :return: returns a list of the walls on the game
        """
        return self.__walls

    def get_score(self) -> int:
        """
        :return: The current game score
        """
        return self.__score
