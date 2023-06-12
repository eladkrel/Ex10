from typing import Optional
from game_display import GameDisplay
import argparse
from snake import *
from apple import *
from wall import *

class SnakeGame:

    def __init__(self, args: argparse.Namespace) -> None:
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
        # if self.__walls_num > 0:
        #     self.__walls.append(self.add_wall())
        # self.__update_board()
        # if self.__apples_num > 0:
        #     self.__apples.append(self.add_apple())
        # self.__update_board()


    def read_key(self, key_clicked: Optional[str])-> None:
        self.__key_clicked = key_clicked

    def update_objects(self)-> None:
        # if (self.__key_clicked == 'Left') and (self.__x > 0):
        #     self.__x -= 1
        # elif (self.__key_clicked == 'Right') and (self.__x < 40):
        #     self.__x += 1
        if self.__key_clicked == 'Left':
            self.__snake.set_orientation('Left')
        if self.__key_clicked == 'Right':
            self.__snake.set_orientation('Right')
        if self.__key_clicked == 'Up':
            self.__snake.set_orientation('Up')
        if self.__key_clicked == 'Down':
            self.__snake.set_orientation('Down')
        self.__snake.move()
        self.__update_board()
        if self.__round % 2 == 0 and self.__round != 0:
            for wall in self.__walls:
                wall.move()
        if len(self.__walls) < self.__walls_num and self.__round != 0:
            self.add_wall()
        if len(self.__apples) < self.__apples_num and self.__round != 0:
            self.add_apple()
        self.__remove_dead_walls()
        self.__round += 1

    def are_empty_cells(self, cells_list):
        for width, height in cells_list:
            if self.__game_board[width][height] is not None:
                return False
        return True

    def __generate_board(self):
        self.__game_board = [[None for _ in range(self.__height)] for _ in
                             range(self.__width)]
        snake_locations = self.__snake.get_locations()
        walls_locations = []
        apples_locations = []
        for wall in self.__walls:
            walls_locations.append(wall.get_locations())
        for apple in self.__apples:
            apples_locations.append(apple.get_location())
        for width, height in snake_locations:
            self.__game_board[width][height] = "black"
        for wall in walls_locations:
            for width, height in wall:
                self.__game_board[width][height] = "blue"
        for width, height in apples_locations:
            self.__game_board[width][height] = "green"

    def __update_board(self):
        self.__game_board = [[None for _ in range(self.__height)] for _ in
                             range(self.__width)]
        snake_locations = self.__snake.get_locations()
        walls_locations = []
        apples_locations = []
        for wall in self.__walls:
            walls_locations.append(wall.get_locations())
        for apple in self.__apples:
            apples_locations.append(apple.get_location())
        for width, height in snake_locations:
            self.__game_board[width][height] = "black"
        for wall in walls_locations:
            for width, height in wall:
                self.__game_board[width][height] = "blue"
        for width, height in apples_locations:
            self.__game_board[width][height] = "green"

    def __remove_dead_walls(self):
        for wall in self.__walls:
            if len(wall.get_locations()) == 0:
                self.__walls.remove(wall)

    def add_apple(self):
        is_possible = False
        apple = None
        while not is_possible:
            apple = Apple()
            apple_loc = apple.get_location()
            if self.are_empty_cells([apple_loc]):
                is_possible = True
        self.__apples.append(apple)
        self.__update_board()

    def add_wall(self):
        is_possible = False
        wall = None
        while not is_possible:
            wall = Wall(self.__width, self.__height)
            wall_loc = wall.get_locations()
            if self.are_empty_cells(wall_loc):
                is_possible = True
        self.__walls.append(wall)
        self.__update_board()

    def draw_board(self, gd: GameDisplay) -> None:
        self.__generate_board()
        for col in range(len(self.__game_board)):
            for row in range(len(self.__game_board[0])):
                if self.__game_board[col][row] is not None:
                    gd.draw_cell(col, row, self.__game_board[col][row])

    def end_round(self) -> None:
        pass

    def is_over(self) -> bool:
        return False

    def get_num_apples(self):
        return self.__apples_num

    def get_apples(self):
        return self.__apples

    def get_walls_num(self):
        return self.__walls_num

    def get_walls(self):
        return self.__walls

