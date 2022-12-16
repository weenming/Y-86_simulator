class stack:
    def __init__(self):
        self.ls = []

    def is_empty(self):
        if len(self.ls) == 0:
            return True
        else:
            return False

    def push(self, val):
        self.ls.append(val)

    def pop(self):
        res = self.ls[len(self.ls) - 1]
        self.ls.remove(self.ls[-1])
        return res

