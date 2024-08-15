""" turn into a streaming program """
import ollama

BASE_URL = "http://localhost:11434"

message = input("Enter a prompt, please: ")

response = ollama.chat(
    model="llama3",
    message=message
)

print(response)
