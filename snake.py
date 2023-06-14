class Snake:
    def __init__(self, board_width, board_height, length=3,
                 orientation="Up") -> None:
        """
        Init for the Snake object.
        :param board_width: the width of the board in the game
        :param board_height: the height of the board in the game
        :param length: start length of snake
        :param orientation: the starting orientation of the snake
        """
        self.__board_width = board_width  # NEW
        self.__board_height = board_height  # NEW
        self.__width = board_width // 2
        self.__height = board_height // 2
        self.__length = length
        self.__orientation = orientation
        self.__locations = []
        self.__grow = 0
        for i in range(self.__length):
            self.__add_tail()

    def __add_tail(self) -> bool:
        """
        Function adds a tail to the snake based on direction
        :return: True if operation successful, False otherwise
        """
        if len(self.__locations) == 0:
            self.__locations.append((self.__width, self.__height))
            return True
        else:
            last_width, last_height = self.__locations[-1]
            if self.__orientation == "Up":
                self.__locations.append((last_width, last_height - 1))
                return True
            if self.__orientation == "Down":
                self.__locations.append((last_width, last_height + 1))
                return True
            if self.__orientation == "Left":
                self.__locations.append((last_width + 1, last_height))
                return True
            if self.__orientation == "Right":
                self.__locations.append((last_width - 1, last_height))
                return True
        return False

    def __add_head(self) -> bool:
        """
        Function adds a head to the snake based on orientation.
        :return: True if operation successful, False otherwise
        """
        if len(self.__locations) == 0:
            self.__locations.append((self.__width, self.__height))
            return True
        else:
            head_width, head_height = self.__locations[0]
            if self.__orientation == "Up":
                self.__locations.insert(0, (head_width, head_height + 1))
                return True
            if self.__orientation == "Down":
                self.__locations.insert(0, (head_width, head_height - 1))
                return True
            if self.__orientation == "Left":
                self.__locations.insert(0, (head_width - 1, head_height))
                return True
            if self.__orientation == "Right":
                self.__locations.insert(0, (head_width + 1, head_height))
                return True
        return False

    def remove_tail(self) -> bool:
        """
        Function removes tail from snake.
        :return: True if operation successful, False otherwise
        """
        if len(self.__locations) > 0:
            self.__locations = self.__locations[:-1]
            return True
        return False

    def move(self) -> bool:
        """
        Function moves the snake 1 block based on direction
        :return: True if operation successful, False otherwise
        """
        self.__add_head()
        if self.__grow <= 0:
            self.remove_tail()
        else:
            self.__grow -= 1
            self.__length += 1
        if self.__locations[0] in self.__locations[1:]:
            # Snake hit itself
            return False
        return True

    def get_locations(self) -> list:
        """
        :return: all locations of the snake
        """
        return self.__locations

    def get_head(self):
        """
        :return: location of head of the snake
        """
        return self.__locations[0]

    def get_orientation(self) -> str:
        """
        :return: str of orientation of the snake
        """
        return self.__orientation

    def set_orientation(self, orientation) -> bool:
        """
        Function sets the orientation of the game only if the new direction
        is legal
        :param orientation: str of the direction
        :return: True if operation successful, False otherwise
        """
        if self.__orientation == "Up" and orientation == "Down":
            return False
        if self.__orientation == "Down" and orientation == "Up":
            return False
        if self.__orientation == "Right" and orientation == "Left":
            return False
        if self.__orientation == "Left" and orientation == "Right":
            return False
        self.__orientation = orientation
        return True

    def grow(self, num) -> None:
        """
        Function adds to the amount of blocks the snake should grow
        :param num: The amount of block to grow
        """
        self.__grow += num

    def get_length(self) -> int:
        """
        :return: The length of the snake
        """
        return self.__length

    def remove_head(self):
        self.__locations = self.__locations[1:]
