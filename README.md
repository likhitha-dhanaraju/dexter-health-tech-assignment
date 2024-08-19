# Chat Application

## Overview

This chat application allows multiple users to communicate in real time via the terminal. Messages are stored in a database, and users can perform various actions such as sending, editing, and deleting messages. The application is designed to handle basic user interactions and validations with a focus on clean, modular, and readable code.

## Requirements

1. **Users**: Two or more users should be able to exchange messages.
2. **Chat/Conversations**: Messages should be stored in a database.
3. **Validations**: Basic validation must be implemented (e.g., empty messages, character limits, valid usernames, etc.).
4. **Code Quality**: The code should be clean, modular, and readable.

## Features

1. **User Interaction**:
    - Users can send messages via the terminal.
    - Messages are color-coded based on the user.

2. **User Registration**:
    - Users register with a username.
    - The system acknowledges both new and existing usernames.

3. **Session Management**:
    - Users can leave the chat by typing 'exit'.

4. **Chat History**:
    - Users can view the chat history for the current session.

5. **Message Editing**:
    - Users can edit their previous messages.

6. **Message Deletion**:
    - Users can delete their messages.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/likhitha-dhanaraju/dexter-health-tech-assignment.git
   cd chat-application
   ```

2. **Install Dependencies**:

Ensure you have Python installed. Then, install the required packages using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Database**:

Make sure your database is correctly configured in database_model.py. You may need to create the necessary tables in your database.

## Usage

### Run the Application

Start the chat session by running:

```bash
python chat_application.py
```

## Interact with the Application

- Enter a session ID or press Enter to create a new session.
- Enter your username when prompted.
- Type messages to send them.
- Use commands like `edit` or `delete` to modify or remove your messages.
- Type `exit` to leave the chat session.

## Development Timeline

- **Hour 1**:
  - Initial setup of the database.
  - Develop the basic application structure.
  - Error debugging and basic validations.

- **Hours 2 and 3**:
  - Update features based on requirements.
  - Parallel testing of new features.

- **Hour 4**:
  - Final testing and implementation of finishing touches.

## Code Structure

- `chat_application.py`: Main script for running the chat application.
- `database_model.py`: Defines the database schema and models.
- `requirements.txt`: Lists the Python dependencies.

## Implementation Details

### Why This Approach
- Database Integration: Using a database ensures messages are persistently stored and can be managed efficiently.
- Threading for Polling: Implementing a separate thread for polling messages allows the main thread to handle user input without blocking message retrieval.
- Color Coding: Assigning colours to users enhances the readability of chat messages, making it easier to differentiate between users.

### Planned Features Not Yet Completed
- User Presence Indicators: Ideally, the application would display real-time notifications when users join or leave the chat.
- Advanced Validation: Additional validations such as message length limits or content filtering were planned but not implemented due to time constraints.
- Quoting previous messages while replying
