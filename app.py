from database_model import User, Message, session

def register_user(username):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        user = User(username=username)
        session.add(user)
        session.commit()
    return user


def send_message(sender_name, receiver_name, content):
    sender = session.query(User).filter_by(username=sender_name).first()
    receiver = session.query(User).filter_by(username=receiver_name).first()

    if sender and receiver and content:
        message = Message(content=content, sender=sender, receiver=receiver)
        session.add(message)
        session.commit()


def view_messages(user1_name, user2_name):
    user1 = session.query(User).filter_by(username=user1_name).first()
    user2 = session.query(User).filter_by(username=user2_name).first()

    if user1 and user2:
        messages = session.query(Message).filter(
            ((Message.sender == user1) & (Message.receiver == user2)) |
            ((Message.sender == user2) & (Message.receiver == user1))
        ).all()

        for message in messages:
            print(f"{message.sender.username}: {message.content}")

def chat_session():
    user1 = input("Enter User 1 Name: ")
    user2 = input("Enter User 2 Name: ")

    register_user(user1)
    register_user(user2)

    while True:
        print(f"{user1} (type 'exit' to quit): ", end="")
        message = input()

        if message == "exit":
            break

        send_message(user1, user2, message)
        view_messages(user1, user2)

def validate_message_content(content):
    if len(content.strip()) == 0:
        return False
    # Add more validation if necessary
    return True

if __name__ == "__main__":
    chat_session()