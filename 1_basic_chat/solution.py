""" this is the solution to creating a basic chat interaction with Ollama """

import ollama

BASE_URL = "http://localhost:11434"

message = input("Enter a prompt, please: ")

response = ollama.chat(
    model="llama3",
    message=message
)

print(response)
