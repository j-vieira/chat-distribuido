class Room:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.messages = []

    def add_user(self, username):
        if username not in self.users:
            self.users.append(username)

    def remove_user(self, username):
        if username in self.users:
            self.users.remove(username)

    def get_users(self):
        return self.users

    def get_last_messages(self):
        return self.messages[-50:]

    def send_message(self, username, message):
        self.messages.append(f"{username}: {message}")