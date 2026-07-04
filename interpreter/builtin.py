class Builtins:

    @staticmethod
    def chap(*args):

        print(*args)

    @staticmethod
    def size(value):

        if isinstance(value, (list, str)):
            return len(value)

        raise TypeError("size() expects an array or string")
