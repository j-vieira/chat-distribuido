import sys
import threading
import xmlrpc.client
from datetime import datetime

logged = False
username = ''
currentMessagesQuantity = 0


def get_hidden_input(prompt, timeout=1):

    user_input = []
    stop_event = threading.Event()

    def read_input():
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while not stop_event.is_set():
            char = sys.stdin.read(1)  # Lê um caractere
            if char == '\n':  # Enter finaliza a entrada
                break
            user_input.append(char)

        sys.stdout.write('\r' + ' ' * (len(prompt) + len(''.join(user_input))) + '\r')
        sys.stdout.flush()

    input_thread = threading.Thread(target=read_input, daemon=True)
    input_thread.start()

    input_thread.join(timeout)
    stop_event.set()

    if not user_input:
        return ""

    return ''.join(user_input)


def client_menu(chat_server):
    global logged
    global username
    global currentMessagesQuantity

    if not logged:
        print("Welcome to dhat! A distribuited chat")
        username = str(input("Username: "))

        if username in chat_server.list_users():
            print("Username in use.")
        else:
            chat_server.register_user(username)
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

        option = str(input("> "))

        if option == "1":
            print("What is the room name to be created?")
            room_name = str(input("> "))
            print(chat_server.create_room(room_name))

        elif option == "2":
            print("Which room you want to join?")
            rooms = chat_server.list_rooms()
            for room in rooms:
                print(room)

            room_name = str(input("> "))
            roomExists = chat_server.join_room(username, room_name)

            current_time = datetime.now().strftime('%H:%M')

            if roomExists:
                oldMessages = chat_server.get_last_messages(room_name)
                firstMessage = 0
                lastMessage = len(oldMessages)
                if lastMessage-50 > 0:
                    firstMessage = lastMessage - 50

                for i in range(firstMessage, lastMessage):
                    currentMessagesQuantity += 1
                    print(current_time + " | " + oldMessages[i])

                while True:
                    x = 0
                    message = get_hidden_input("")
                    if message == "exit":
                        break
                    while x < 30000:
                        if message == "":
                            x += 1
                        else:
                            splittedMessage = message.split(" ")
                            isPrivate = (splittedMessage[0] == "/pv")
                            if isPrivate:
                                recipient = splittedMessage[1]
                                chat_server.send_message(username, room_name, message, recipient)
                            else:
                                chat_server.send_message(username, room_name, message)
                            break

                    messages = chat_server.get_last_messages(room_name)

                    if len(messages) > currentMessagesQuantity: # faz o receive_messages
                        for i in range(currentMessagesQuantity, len(messages)):
                            sender = messages[i].split(':')[0]
                            if sender != username:
                                print(current_time + " | " + messages[i])
                        currentMessagesQuantity += 1
            else:
                print(f"Room does not exist.")

        elif option == "3":
            onlineUsers = chat_server.list_users() # precisa ser conectado numa sala
            for i in range(0, len(onlineUsers)):
                print(onlineUsers[i])
        elif option == "4":
            room_name = str(input("Room name: "))
            oldMessages = chat_server.get_last_messages(room_name)
            firstMessage = 0
            lastMessage = len(oldMessages)
            if lastMessage - 50 > 0:
                firstMessage = lastMessage - 50

            for i in range(firstMessage, lastMessage):
                print(oldMessages[i])
        else:
            print("Invalid option, put a number in range 1 to 4!")




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
