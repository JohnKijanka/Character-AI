from openai import OpenAI
import streamlit as st
import os

# Define the file paths
character_background_file = 'character_background.txt'
conversation_topics_file = 'conversation_topics.txt'
chat_history_file = 'chat_history.txt'

# Function to create a blank file if it doesn't exist
def create_blank_file_if_not_exists(filepath):
    if not os.path.exists(filepath):
        with open(filepath, 'w') as file:
            file.write("")

# Check if the character background file exists
if not os.path.exists(character_background_file):
    st.error(f"The file {character_background_file} does not exist. Please create it with the character's background information.")
else:
    # Read the character background
    with open(character_background_file, 'r') as file:
        character_background = file.read()

    # Create blank files if they do not exist
    create_blank_file_if_not_exists(conversation_topics_file)
    create_blank_file_if_not_exists(chat_history_file)

    # Read the conversation topics
    with open(conversation_topics_file, 'r') as file:
        conversation_topics = file.read()

    # Read the chat history
    with open(chat_history_file, 'r') as file:
        chat_history = file.read()

    # Initialize OpenAI API client
    client = OpenAI(
        api_key = os.environ.get('OPENAI_API_KEY')
    )

    # Streamlit app layout
    st.title("ChatGPT Character Interaction")
    st.write("Enter your message to interact with the character:")

    # User input
    user_input = st.text_input("Your message")

    if st.button("Send"):
        # Combine everything into a single prompt
        combined_prompt = f"""
        Below is the background of a character:
        {character_background}

        The character should attempt to bring up the following information in conversation if possible:
        {conversation_topics}

        Below is the past chat history the character has participated in:
        {chat_history}

        User input: {user_input}

        Respond as the character based on the above information.
        """

        # Generate a response using ChatGPT
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": combined_prompt}
            ],
            model="gpt-3.5-turbo",
        )

        # Extract the response content
        response_content = response.choices[0].message.content

        # Display the response
        st.write("### Character's Response:")
        st.write(response_content)

        # Update the chat history with the new interaction
        new_chat_entry = f"User: {user_input}\nCharacter: {response_content}\n\n"

        with open(chat_history_file, 'a') as file:
            file.write(new_chat_entry)
