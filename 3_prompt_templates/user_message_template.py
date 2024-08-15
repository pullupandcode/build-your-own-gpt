""" this is how we create a chat template to use for our LLM """
from langchain_community.llms.ollama import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

BASE_URL = "http://localhost:11434"

llm = Ollama(
    base_url=BASE_URL,
    model='llama3',
)

what = input("What programming topic do you want to learn about? ")
language = input("What programming language do you want to learn this in? ")

# Prompt template
prompt = PromptTemplate.from_template(
    "Explain the programming concept of {what} in {language}."
)

# Chain using model and formatting
chain = prompt | llm| StrOutputParser()

response = chain.invoke({"what": what, "language": language})

print(response)
