

class UserData:
    def __init__(self, id=0, faces=None, name=""):
        self.id = id
        self.faces = faces if faces is not None else []  # Avoid mutable default argument
        self.name = name

 