class Parent():
    static = 1
    def __init__(self):
        pass

class Child(Parent):
    def __init__(self):
        super(Child, self).__init__()

if __name__ == "__main__":
    p = Parent()
    p2 = Parent()
    Parent.static = 2
    c = Child()
    print(c.static)