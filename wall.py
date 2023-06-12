from game_utils import  get_random_wall_data
WALL_LENGTH = 3
class Wall:
    def __init__(self, board_width, board_height):
        self.__board_width = board_width
        self.__board_height = board_height
        self.__length = WALL_LENGTH
        self.__x, self.__y, self.__orientation = get_random_wall_data()
        self.__locations = [(self.__x, self.__y)]
        for i in range(self.__length//2):
            self.__add_head()
            self.__add_tail()


    def __add_tail(self):

        last_width, last_height = self.__locations[-1]
        if self.__orientation == "Up":
            if self.__locations[-1][1] > 0:
                self.__locations.append((last_width, last_height - 1))
                return True
        if self.__orientation == "Down":
            if self.__locations[-1][1] < self.__board_height - 1:
                self.__locations.append((last_width, last_height + 1))
                return True
        if self.__orientation == "Left":
            if self.__locations[-1][0] < self.__board_width - 1:
                self.__locations.append((last_width + 1, last_height))
                return True
        if self.__orientation == "Right":
            if self.__locations[-1][0] > 0:
                self.__locations.append((last_width - 1, last_height))
                return True
        return False


    def __add_head(self):

        head_width, head_height = self.__locations[0]
        if self.__orientation == "Up":
            if self.__locations[0][1] < self.__board_height - 1:
                self.__locations.insert(0, (head_width, head_height + 1))
                return True
        if self.__orientation == "Down":
            if self.__locations[0][1] > 0:
                self.__locations.insert(0, (head_width, head_height - 1))
                return True
        if self.__orientation == "Left":
            if self.__locations[0][0] > 0:
                self.__locations.insert(0, (head_width - 1, head_height))
                return True
        if self.__orientation == "Right":
            if self.__locations[0][0] < self.__board_width - 1:
                self.__locations.insert(0, (head_width + 1, head_height))
                return True
        return False

    def remove_tail(self):
        if len(self.__locations) > 0:
            self.__locations = self.__locations[:-1]
            return True
        return False

    def remove_head(self):
        if len(self.__locations) > 0:
            self.__locations = self.__locations[1:]
            return True
        return False

    def move(self):
        self.__add_head()
        self.remove_tail()

        #     return False  # do i need it??
        # return True


    def get_locations(self):
        return self.__locations

    def get_wall_length(self):
        return self.__length


