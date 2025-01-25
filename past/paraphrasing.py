from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

#Loads the environment and gets GROQ API key
load_dotenv()
key = os.getenv("GROQ_API_KEY")

#Creates chat instance
chat = ChatGroq(temperature=0, groq_api_key= key, model_name="mixtral-8x7b-32768")

#Defines prompt for the system to use
system = ("You are an impartial editor tasked with rewriting the following text to make it more engaging and interesting. "
        "Ensure that the rewritten text maintains neutrality, fairly represents all viewpoints, and avoids any bias."
        "Keep it at approximately 50 words")
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

#Builds the chain by piping the prompt into the chat model
chain = prompt | chat
chain.invoke({"text": "Explain the importance of low latency LLMs."})

#Rewrites the text to be engaging
def rewrite_text_to_engage(input_text):

    # Invoke the chain with the input text and returns rewritten content
    response = chain.invoke({"text": input_text})

    return response.content

test = "President Trump announced key appointments to the White House Office of Communications, Public Liaison, and Cabinet Affairs. Alex Pfeiffer, Kaelan Dorr, Dylan Johnson, Johanna Persing, Dan Boyle, and Harrison Fields will all return to White House. Assistant to the President and White House Communications Director Steven Cheung will return."
print(rewrite_text_to_engage(test))