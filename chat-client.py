import xmlrpc.client

logged = False
username = ''


def client_menu(chat_server):
    global logged
    global username

    if not logged:
        print("Welcome to dhat! A distribuited chat")
        username = str(input("Username: "))

        if username in chat_server.list_users():
            print("Username in use.")
        else:
            logged = True


    else:

        print(
            """
                    1. Create Room.
                    2. Enter in room.
                    3. List online users.
                    4. What's up?
            """
        )

        option = int(input("> "))

        if option == 1:
            print("What is the room name to be created?")
            room_name = str(input("> "))
            print(chat_server.create_room(room_name))

        elif option == 2:
            print("Which room you want to join?")
            print(chat_server.list_rooms())
            room_name = str(input("> "))
            roomExists = chat_server.join_room(username, room_name)

            if (roomExists):
                while(True):
                    message = input("> ")
                    chat_server.send_message(username, room_name, message)
            else:
                print(f"Room does not exist.")

        elif option == 3:
            print(chat_server.list_users())

        # elif option == 4:
        # chat_server.Room.get_last_messages()


server_address = 'localhost'

binder = xmlrpc.client.ServerProxy(f'http://{server_address}:8001')

server_address, chat_server_port = binder.lookup_procedure('chat')

if chat_server_port is None:
    print("Chat service not found.")
    exit(1)

chat_server = xmlrpc.client.ServerProxy(f'http://{server_address}:{chat_server_port}')
while True:
    try:
        client_menu(chat_server)
    except KeyboardInterrupt:
        print("\nExiting...")
        break
