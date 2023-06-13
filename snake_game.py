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
        self.__score = 0  # NEW
        self.__suicide = False
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
        if not self.__snake.move():
            self.__suicide = True
        self.__update_board()
        if self.__round % 2 == 0 and self.__round != 0:
            for wall in self.__walls:
                wall.move()
        self.__remove_dead_walls() # CHANGED PLACE
        if len(self.__walls) < self.__walls_num and self.__round != 0:
            self.add_wall()
        self.__remove_dead_apples() # NEW
        if len(self.__apples) < self.__apples_num and self.__round != 0:
            self.add_apple()
        # self.__remove_dead_walls()
        # self.__round += 1

    def are_empty_cells(self, cells_list):  # CHANGED IT
        for width, height in cells_list:
            if width > self.__width-1 or width < 0 or height > self.__height-1 or height < 0:  # NEW LINE
                continue
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
            if width > self.__width-1 or width < 0 or height > self.__height-1 or height < 0:  # NEW
                continue  # NEW
            else:  # NEW
                self.__game_board[width][height] = "black"  # NEW
        for wall in walls_locations:
            for width, height in wall:
                if width > self.__width-1 or width < 0 or height > self.__height-1 or height < 0:  # NEW
                    continue  # NEW
                else:  # NEW
                    self.__game_board[width][height] = "blue"  # NEW
                # self.__game_board[width][height] = "blue"
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
            if width > self.__width-1 or width < 0 or height > self.__height-1 or height < 0:  # NEW
                continue # NEW
            else:  # NEW
                self.__game_board[width][height] = "black"  # NEW
        for wall in walls_locations:
            for width, height in wall:
                if width > self.__width-1 or width < 0 or height > self.__height-1 or height < 0:  # NEW
                    continue  # NEW
                else:  # NEW
                    self.__game_board[width][height] = "blue"  # NEW
                # self.__game_board[width][height] = "blue"
        for width, height in apples_locations:
            self.__game_board[width][height] = "green"

    # def __remove_dead_walls(self):
    #     for wall in self.__walls:
    #         if len(wall.get_locations()) == 0:
    #             self.__walls.remove(wall)


    def __remove_dead_walls(self):  # NEW
        all_cells = self.all_cells()
        for wall in self.__walls:
            wall_coordinates = wall.get_locations()
            wall_still_in = False
            # print(wall_coordinates)
            for wall_cell in wall_coordinates:
                if wall_cell in all_cells:
                    wall_still_in = True
                    break
            if not wall_still_in:
                self.__walls.remove(wall)
                # new_wall = Wall(self.__width, self.__height)  # NEW
                # self.__walls.append(new_wall)  # NEW


    def __remove_dead_apples(self):  # NEW
        snake_locations = self.__snake.get_locations()
        all_walls_cells = []
        for wall in self.__walls:
            wall_coordinates = wall.get_locations()
            all_walls_cells.append(wall_coordinates)

        for apple in self.__apples:
            apple_still_okay = True
            apple_coordinates = apple.get_location()
            if apple_coordinates in snake_locations:
                apple_still_okay = False
                self.__snake.grow(3)
                self.__score += int(self.__snake.get_length()**0.5)
                print(self.__snake.get_length())
            for wall in all_walls_cells:
                if apple_coordinates in wall:
                    apple_still_okay = False
                    break
            if not apple_still_okay:
                self.__apples.remove(apple)







    def all_cells(self):
        all_cells = []
        for row in range(len(self.__game_board)):
            for col in range(len(self.__game_board[0])):
                all_cells.append((row, col))
        return all_cells




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

    def end_round(self) -> None: # NEW
        self.__round += 1


    def is_over(self) -> bool:  # NEW
        if self.__suicide:
            return True
        walls_locations = []
        if self.__max_rounds != -1:
            if self.__round == self.__max_rounds + 1:
                return True
        snake_locations = self.__snake.get_locations()
        snake_head = snake_locations[0]
        snake_head_x = snake_head[0]
        snake_head_y = snake_head[1]
        for wall in self.__walls:
            walls_locations.append(wall.get_locations())
        for wall in walls_locations:
            if snake_head in wall:
                return True
        if snake_head_x > self.__width-1 or snake_head_x < 0 or snake_head_y > self.__height-1 or snake_head_y < 0:
            return True
        return False

    def get_num_apples(self):
        return self.__apples_num

    def get_apples(self):
        return self.__apples

    def get_walls_num(self):
        return self.__walls_num

    def get_walls(self):
        return self.__walls

    def get_score(self):  # NEW
        return self.__score



