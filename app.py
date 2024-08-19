import uuid
import threading
import time
from database_model import User, Message, session

colors = {
    1: "\033[94m",  # Blue
    2: "\033[92m",  # Green
    3: "\033[93m",  # Yellow
    "reset": "\033[0m"  # Reset to default color
}


def register_user(username):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        # User is new, so welcome them and send a join message
        print(f"Welcome new User : {username}")
        user = User(username=username, color=None)
        session.add(user)
        session.commit()

        # Send a message to indicate a new user has joined
        send_system_message(f"{username} has joined the chat.", session_id)
    else:
        print(f"Welcome back User : {username}")
    return user


def assign_color_to_user(user):
    if user.color:
        return user.color

    num_assigned_colors = session.query(User).filter(User.color != None).count() + 1

    if num_assigned_colors <= 3:
        user.color = colors.get(num_assigned_colors, colors["reset"])
        session.commit()

    return user.color


def send_message(sender_name, content, session_id):
    sender = session.query(User).filter_by(username=sender_name).first()

    if sender and content:
        message = Message(content=content, sender=sender, session_id=session_id)
        session.add(message)
        session.commit()


def send_system_message(content, session_id):
    # System messages don't have a sender
    message = Message(content=content, sender=None, session_id=session_id)
    session.add(message)
    session.commit()


def update_message(message_id, new_content):
    message = session.query(Message).filter_by(id=message_id).first()

    if message:
        message.content = new_content
        session.commit()
        print(f"Message updated to: {new_content}")
    else:
        print("Message not found.")


def delete_message(message_id):
    message = session.query(Message).filter_by(id=message_id).first()

    if message:
        session.delete(message)
        session.commit()
        print("Message has been deleted.")
    else:
        print("Message not found.")


def view_messages(session_id):
    messages = session.query(Message).filter_by(session_id=session_id).all()

    for message in messages:
        if message.sender:
            sender = message.sender
            assign_color_to_user(sender)
            user_color = sender.color or colors["reset"]
            print(f"{user_color}{sender.username}: {message.content}{colors['reset']}")
        else:
            # Handle system messages (e.g., user joined)
            print(f"\033[90m{message.content}{colors['reset']}")


def list_user_messages(username, session_id):
    user = session.query(User).filter_by(username=username).first()
    if user:
        user_messages = session.query(Message).filter_by(sender=user, session_id=session_id).all()
        if user_messages:
            print(f"\n{username}'s messages:")
            for idx, message in enumerate(user_messages, start=1):
                print(f"{idx}. {message.content} (Message ID: {message.id})")
            return user_messages
        else:
            print("No messages found.")
            return None
    else:
        print("User not found.")
        return None


def poll_messages(session_id, user_name):
    last_message_count = 0
    while True:
        current_message_count = session.query(Message).filter_by(session_id=session_id).count()

        if current_message_count > last_message_count:
            view_messages(session_id)
            last_message_count = current_message_count

            print(f"{user_name} (type 'exit' to quit, 'edit' to edit, or 'delete' to delete a message): ", end="\n")

        time.sleep(0.5) # Have to optimise the timing to ensure smooth chat history view and db connection


def chat_session():
    session_id = input("Enter Session ID to join or press Enter to create a new session: ").strip()

    if not session_id:
        session_id = str(uuid.uuid4())
        print(f"New chat session created with ID: {session_id}")
    else:
        print(f"Joining chat session with ID: {session_id}")

    user_name = input("Enter your Username: ").strip()
    while user_name is None or user_name == "":
        if not user_name:
            print("Username cannot be empty.")
            user_name = input("Enter your Username: ").strip()

    user = register_user(user_name)

    user_color = assign_color_to_user(user)
    print(
        f"Welcome to the chat, {user_name}. You have been assigned the color {user_color}. Type 'exit' to leave the chat.")

    polling_thread = threading.Thread(target=poll_messages, args=(session_id, user_name), daemon=True)
    polling_thread.start()

    while True:
        print(f"{user_name} (type 'exit' to quit, 'edit' to edit, or 'delete' to delete a message): ", end="\n")
        message = input()

        if message.lower() == "exit":
            print(f"{user_name} has left the chat.")
            send_system_message(f"{user_name} has left the chat.", session_id)
            break
        elif message.lower() == "edit":
            user_messages = list_user_messages(user_name, session_id)
            if user_messages:
                try:
                    msg_number = int(input("Enter the message number you want to edit: ").strip()) - 1
                    if 0 <= msg_number < len(user_messages):
                        new_content = input("Enter the new content for the message: ").strip()
                        update_message(user_messages[msg_number].id, new_content)

                        print("\nUpdated chat history:")
                        view_messages(session_id)
                    else:
                        print("Invalid message number.")
                except ValueError:
                    print("Please enter a valid number.")
        elif message.lower() == "delete":
            user_messages = list_user_messages(user_name, session_id)
            if user_messages:
                try:
                    msg_number = int(input("Enter the message number you want to delete: ").strip()) - 1
                    if 0 <= msg_number < len(user_messages):
                        delete_message(user_messages[msg_number].id)

                        print("\nUpdated chat history:")
                        view_messages(session_id)
                    else:
                        print("Invalid message number.")
                except ValueError:
                    print("Please enter a valid number.")
        elif message:
            send_message(user_name, message, session_id)
        else:
            print("\n")


if __name__ == "__main__":
    chat_session()
