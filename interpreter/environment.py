class Environment:

    def __init__(self, parent=None):

        self.variables = {}
        self.parent = parent

    def set(self, name, value):

        self.variables[name] = value

    def get(self, name):

        if name in self.variables:
            return self.variables[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise NameError(f"Variable '{name}' is not defined")