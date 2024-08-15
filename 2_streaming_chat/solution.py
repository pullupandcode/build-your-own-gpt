""" this is the solution to creating a streaming chat interaction with Ollama """
import ollama

BASE_URL = "http://localhost:11434"

message = input("enter your prompt, please: ")

response = ollama.chat(
    model="llama3",
    messages=[
        { 'role': 'user', 'content': message}
    ],
    stream=True
)

for chunk in response:
    print(chunk['message']['content'], end='', flush=True)
