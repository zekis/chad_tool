from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import config
import json
    
def ai_new_tool(template, name, description, parameters):

    prompt_template = """Assistant is designed to answer programming questions by providing python code.

{history}
Human: {human_input}
Assistant:"""

    prompt = PromptTemplate(
        input_variables=["history", "human_input"], 
        template=prompt_template
    )


    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0), 
        prompt=prompt, 
        verbose=True, 
        memory=ConversationBufferWindowMemory(k=2),
    )
    output = chatgpt_chain.predict(human_input=f"Alter the following code to {description} with these parameters {parameters}: {template}")

    print(output)

    return output

def ai_edit_tool(original, name, description, parameters, changes, feedback):

    prompt_template = """Assistant is designed to answer programming questions by providing python code.

{history}
Human: {human_input}
Assistant:"""

    prompt = PromptTemplate(
        input_variables=["history", "human_input"], 
        template=prompt_template
    )


    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0), 
        prompt=prompt, 
        verbose=True, 
        memory=ConversationBufferWindowMemory(k=2),
    )
    output = chatgpt_chain.predict(human_input=f"""Alter the following code with objective: {description}
    Including these parameters {parameters}
    Proposed changes: {changes}
    Additional Notes: {feedback}


    Original Code:{original}
    
    """)

    print(output)
    return output

def ai_review_response(original, name, description, parameters, values, response, feedback):
    prompt_template = """Assistant is designed to answer programming questions by providing python code.

{history}
Human: {human_input}
Assistant:"""

    prompt = PromptTemplate(
        input_variables=["history", "human_input"], 
        template=prompt_template
    )


    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0), 
        prompt=prompt, 
        verbose=True, 
        memory=ConversationBufferWindowMemory(k=2),
    )
    example = '{"test_result": "pass"} or {"test_result": "fail", "recommended_changes": "missing import os"}'
    output = chatgpt_chain.predict(human_input=f"""Responding in only JSON, using the following parameters "test_result": "pass/fail", "recommended_changes": "changes"
    Please review the response: {response} 
    Confirm if it has met the objectives to {description}
    With these parameters: {values}
    Additional Notes: {feedback}


    Original Code:{original}
    

    Example AI Response: {example}
    """)

    print(output)

    return json.loads(output)

def ai_suggest_test_parameters(original, name, description, parameters):
    prompt_template = """Assistant is designed to answer programming questions by providing python code.

{history}
Human: {human_input}
Assistant:"""

    prompt = PromptTemplate(
        input_variables=["history", "human_input"], 
        template=prompt_template
    )


    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0), 
        prompt=prompt, 
        verbose=True, 
        memory=ConversationBufferWindowMemory(k=2),
    )
    example = '{"parameter_name": "parameter_value"}'
    output = chatgpt_chain.predict(human_input=f"""Responding in only JSON, return test parameters for {parameters} to assist in testing the code below
    To meet the objectives to {description}
    
    
    Original Code:{original}
    

    Example AI Response: {example}
    """)

    print(output)

    return json.loads(output)