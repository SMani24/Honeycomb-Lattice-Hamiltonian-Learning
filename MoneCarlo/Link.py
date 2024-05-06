class Link:
    def __init__(self, number):
        self.__spin = 0 # the state of the link, either |0> or |1>
        self.__phase = 1 # either 1 or -1
        self.__number = number
    