from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.get_env("OPENAI_API_KEY")
llm = OpenAI(api_key=openai_api_key)
template = """you are BizBuddy AI, a helpful Assistant. Answer the following questions: {user_message}"""

prompt = PromptTemplate(input_variables=['user_message'], template=template)
llm_chain = LLMChain(llm=llm, prompt=prompt)


def generate_response(user_message: str) -> str:
    try:
        response = llm_chain.run(user_message)
        return response

    except Exception as e:
        raise Exception(f"Error generating response: {e}")
