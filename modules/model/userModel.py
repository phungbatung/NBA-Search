class User:
    def __init__(self, id, username, password, email, name):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.name = name

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}', name='{self.name}')"