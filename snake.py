class Snake:
    def __init__(self, board_width, board_height, length=3, orientation="Up"):
        self.__width = board_width // 2
        self.__height = board_height // 2
        self.__length = length
        self.__orientation = orientation
        self.__locations = []
        self.__grow = 0
        for i in range(self.__length):
            self.__add_tail()

    def __add_tail(self):

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

    def __add_head(self):
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

    def remove_tail(self):
        if len(self.__locations) > 0:
            self.__locations = self.__locations[:-1]
            return True
        return False

    def move(self):
        self.__add_head()
        if self.__grow == 0:
            self.remove_tail()
        else:
            self.__grow -= 1
        if self.__locations[0] in self.__locations[1:]:
            # Snake hit itself
            return False
        return True


    def get_locations(self):
        return self.__locations

    def get_orientation(self):
        return self.__orientation

    def set_orientation(self, orientation):
        if self.__orientation == "UP" and orientation == "Down":
            return False
        if self.__orientation == "Down" and orientation == "UP":
            return False
        if self.__orientation == "Right" and orientation == "Left":
            return False
        if self.__orientation == "Left" and orientation == "Right":
            return False
        self.__orientation = orientation
        return True
