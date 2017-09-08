class Node:
    root_id_counter = 0

    def __init__(self, parent=None):
        self.left = None
        self.right = None
        self.parent = parent
        self.level = 0 if not parent else parent.level + 1
        if not parent:
            self.id = Node.root_id_counter
            Node.root_id_counter += 1
        self.weight = 0
        self.final = True
        self.feature = None
        self.feature_index = None
        self.cut_value = 0

    def __str__(self):
        if self.final:
            return f'{self.level*"  "}{self.weight}'
        else:
            return (f'{self.level*"  "}{self.feature} < {self.cut_value}\n'
                    f'{self.left}\n'
                    f'{self.right}')

    def __iter__(self):
        return [self].__iter__()

    @property
    def root(self):
        if self.parent:
            return self.parent.root
        else:
            return self
