from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

rooms = {}
users = {}

# room vai ser um dicionario com users e messages
# rooms = {room1, room2, ..., roomN}
# room1 tambem sera um dicionario, tal que room1 tem uma estrutura de 
# 'users' e 'messages' 
# tal que, 
# room1 = {'users': 'joao', 'helio', 'laizz',
#          'messages': 'joao': 'oi!', 'helio': 'ola!', ...}
# rooms sera guardado num arquivo, futuramente.

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

def register_user(name, password):
    if name not in users:
        users[name] = User(name, password)
        return f"User {name} registered successfully."
    return f"User {name} is already registered."

def create_room(room_name):
    if room_name not in rooms:
        # Initialize room with proper structure
        rooms[room_name] = {
            'users': [],
            'messages': []
        }
        return f"Room {room_name} created successfully."
    return f"Room {room_name} already exists."

def join_room(username, room_name):
    if room_name in rooms:
        room = rooms[room_name]
        # {'messages': {}, 'users': {}}
        room['users'].append(username)

        return True
    return False
    #return f"Room {room_name} does not exist."


def send_message(username, room_name, message, recipient=None):
        
    if room_name not in rooms:
        return f"Room {room_name} does not exist."

    room = rooms[room_name]

    if recipient:
        private_room_name = f"{username}:{recipient}"
            
        if private_room_name not in rooms:
            create_room(private_room_name)
            
        private_room = rooms[private_room_name]
        private_room.send_message(username, message)
        
    else:
        if room['messages'] is None:
            room['messages'] = {}
        room['messages'].append(username + ":" + message)

    print(room['messages'][-1])

    return "Message sent successfully."

def get_last_messages(room_name):
    return rooms[room_name]['messages']

def list_rooms():
    return list(rooms.keys())

def list_users():
    return list(users.keys())
    
# falta remocao de usuarios, depois reler

def main():
    server = SimpleXMLRPCServer(('localhost', 9000), allow_none=True)
    print("Servidor de chat pronto, aguardando conexões!")

    server.register_function(create_room, "create_room")
    server.register_function(join_room, "join_room")
    server.register_function(send_message, "send_message")
    server.register_function(list_rooms, "list_rooms")
    server.register_function(list_users, "list_users")
    server.register_function(get_last_messages, "get_last_messages")

    binder = xmlrpc.client.ServerProxy('http://localhost:8001')
    binder.register_procedure('chat', 9000)

    server.serve_forever()

if __name__ == "__main__":
    main()
