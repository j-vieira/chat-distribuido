from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

import Users
import User

import Rooms
import Room

class ChatServer:
    def __init__(self):
        self.rooms = {}
        self.users = {}

    def create_room(self, room_name):
        if room_name not in self.rooms:
            self.rooms[room_name] = Room(room_name)
            return f"Room {room_name} created successfully."
        
        return f"Room {room_name} already exists."

    def join_room(self, username, room_name):
        
        if room_name in self.rooms:
            room = self.rooms[room_name]
            room.add_user(username)
            
            return {
                "users": room.get_users(),
                "messages": room.get_last_messages(),
            }
        
        return f"Room {room_name} does not exist."

    def send_message(self, username, room_name, message, recipient=None):
        
        if room_name not in self.rooms:
            return f"Room {room_name} does not exist."

        room = self.rooms[room_name]

        if recipient:
            private_room_name = f"{username}:{recipient}"
            
            if private_room_name not in self.rooms:
                self.create_room(private_room_name)
            
            private_room = self.rooms[private_room_name]
            private_room.send_message(username, message)
        
        else:
            room.send_message(username, message)

        return "Message sent successfully."

    def list_rooms(self):
        return self.rooms.keys()

    def list_users(self):
        return {'a':1, 'b':2}
    
# falta remocao de usuarios, depois reler

def main():
    chat_server = ChatServer()

    server = SimpleXMLRPCServer(('localhost', 9000), allow_none=True)
    print("Servidor de chat pronto, aguardando conexões!")

    server.register_function(chat_server.create_room, "create_room")
    server.register_function(chat_server.join_room, "join_room")
    server.register_function(chat_server.send_message, "send_message")
    server.register_function(chat_server.list_rooms, "list_rooms")
    server.register_function(chat_server.list_users, "list_users")

    binder = xmlrpc.client.ServerProxy('http://localhost:8001')
    binder.register_procedure('chat', 9000)

    server.serve_forever()

if __name__ == "__main__":
    main()
