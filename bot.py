import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button, END
import random
import json

class ChatBotApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")
        self.intents = self.load_intents()

        self.text_widget = Text(root, height=10, width=50)
        self.text_widget.pack(padx=10, pady=10)
        self.text_widget.insert(END, "ChatBot: Hello! How can I assist you?\n")
        self.text_widget.configure(state='disabled')

        self.scrollbar = Scrollbar(root, command=self.text_widget.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.input_entry = Entry(root, width=50)
        self.input_entry.pack(padx=10, pady=10)

        self.send_button = Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

    def load_intents(self):
        with open('intents.json', 'r') as file:
            intents_data = json.load(file)
        return intents_data['intents']

    def send_message(self):
        user_input = self.input_entry.get().lower().strip()
        self.display_message(f"You: {user_input}\n")
        self.input_entry.delete(0, 'end')

        response = self.get_response(user_input)
        self.display_message(f"ChatBot: {response}\n")

    def get_response(self, user_input):
        user_input = user_input.lower()
        for intent in self.intents:
            if any(keyword.lower() in user_input for keyword in intent['keywords']):
                return random.choice(intent['responses'])
        return "I'm sorry, I don't understand that."

    def display_message(self, message):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(END, message)
        self.text_widget.configure(state='disabled')
        self.text_widget.see(END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApplication(root)
    root.mainloop()
