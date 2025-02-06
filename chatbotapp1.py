import os
import json
import random
import nltk
import ssl
import streamlit as st
import csv
from nltk.tokenize import word_tokenize  # Missing import added
from nltk.stem import WordNetLemmatizer

# SSL fix for nltk
ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')
nltk.download('wordnet')

# Load intents from the JSON file
file_path = os.path.abspath("./Intent.json")    
with open(file_path, "r") as file:
    intents = json.load(file)

# Initialize lemmatizer for preprocessing
lemmatizer = WordNetLemmatizer()

# Preprocess text by tokenizing and lemmatizing
def preprocess_text(text):
    words = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(word) for word in words]

# Function to get chatbot response
def chatbot(input_text):
    input_words = preprocess_text(input_text)
    best_match = None
    max_overlap = 0

    # Check for the best matching intent based on overlapping words
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_words = preprocess_text(pattern)
            overlap = len(set(input_words) & set(pattern_words))
            if overlap > max_overlap:
                best_match = intent
                max_overlap = overlap

    if best_match:
        return random.choice(best_match["responses"])

    return "I'm still learning, please rephrase your question."

counter = 0

def main():
    global counter
    
    st.title("BIOFEAST Chatbot")
    st.write("Welcome to the Sustainable Food Practices Chatbot. Please type a message and press Enter to start the conversation.")
    
    # Check if chat log file exists, if not create it
    if not os.path.exists('chat_log.csv'):
        with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['User Input', 'Chatbot Response'])
    
    counter += 1
    
    # Display conversation history
    st.header("Conversation History:")
    with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row
        history = list(csv_reader)[-5:]  # Show the last 5 conversations
        for row in history:
            st.text(f"User: {row[0]}")
            st.text(f"Chatbot: {row[1]}")
            st.markdown("---")
    
    # User input
    user_input = st.text_input("You:", key=f"user_input_{counter}")
    
    if user_input:
        response = chatbot(user_input)
        st.text_area("Chatbot:", value=response, height=120, max_chars=None, key=f"chatbot_response_{counter}")
        
        # Save chat history
        with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([user_input, response])

        if response.lower() in ['goodbye', 'bye']:
            st.write("Thank you for chatting with me. Have a great day!")
            st.stop()

if __name__ == '__main__':
    main()
