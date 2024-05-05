from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import 
import os

from dotenv import load_dotenv

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACHING_V2"]="true"



# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def chat_summary(chat):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "I give you some whatsapp chat. give me summary of these chat in 100 words. chat append here:")
            ("Chat", {chat})
        ]
    )
    # prompt = "I give you some whatsapp chat. give me summary of these chat in 100 words. chat append here:"
    llm=Ollama(model="llama3")
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    response=chain.invoke(chat)
    return response


