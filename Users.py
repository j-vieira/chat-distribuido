import User

class Users:
    def __init__(self):
        self.users = {}

    def register_user(self, name, password):
        if name not in self.users:
            self.users[name] = User(name, password)
            return f"User {name} registered successfully."
        return f"User {name} is already registered."

    def list_users(self):
        return list(self.users.keys())