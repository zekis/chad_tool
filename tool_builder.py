from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI   
from langchain import PromptTemplate    
    
    
def ai_new_tool(template, name, description, parameters):
    llm = OpenAI(temperature=0)