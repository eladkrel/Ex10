from game_utils import get_random_apple_data


class Apple:
    def __init__(self) -> None:
        """
        Init for the apple class
        """
        self.__x, self.__y = get_random_apple_data()

    def get_location(self):
        """
        :return: The location of the apple
        """
        return self.__x, self.__y
