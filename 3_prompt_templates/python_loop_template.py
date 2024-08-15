""" this is how we create a chat template to use for our LLM, with user input """

from langchain_community.llms import ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

BASE_URL = "http://localhost:11434"

model = ollama.Ollama(
    base_url=BASE_URL,
    model='llama3',
)

what = "loop"
language = "python"

# Prompt template
prompt = PromptTemplate.from_template(
    "Explain the programming concept of {what} in {language}."
)

# Chain using model and formatting
chain = prompt | model | StrOutputParser()

response = chain.invoke({"what": what, "language": language})

print(response)
