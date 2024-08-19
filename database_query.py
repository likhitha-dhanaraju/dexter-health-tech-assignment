from sqlalchemy import inspect
from database_model import engine, session, User, Message

# Check the database location
print(f"Database URL: {engine.url}")

# Inspecting the tables
inspector = inspect(engine)
print(f"Tables in the database: {inspector.get_table_names()}")

# Query and print all users and messages
users = session.query(User).all()
messages = session.query(Message).all()

print("\nUsers:")
for user in users:
    print(f"{user.id}: {user.username}")

print("\nMessages:")
for message in messages:
    print(f"{message.id}: {message.content} from {message.sender.username} to {message.receiver.username}")









