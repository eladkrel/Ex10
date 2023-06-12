from game_utils import get_random_apple_data


class Apple:
    def __init__(self):
        self.__x, self.__y = get_random_apple_data()

    def get_location(self):
        return self.__x, self.__y
