""" this is the solution to creating a streaming chat interaction with Ollama """
import ollama

BASE_URL = "http://localhost:11434"

def get_input():
    """ gets input from user """
    return input("enter your llm prompt here")

def run_chat(message):
    """ runs the ollama chat """
    response = ollama.chat(
        model="llama3",
        messages=[
            { 'role': 'user', 'content': message}
        ],
        stream=True
    )

    return response

def main():
    """ execute the program """
    message = get_input()
    response = run_chat(message)

    for chunk in response:
        print(chunk['message']['content'], end='', flush=True)


if __name__ == "__main__":
    main()
