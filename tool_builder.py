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
    Return only the code:


    Original Code:{original}
    
    """)

    print(output)
    return(output)

def ai_review_response(original, name, description, parameters, values, response, feedback):
    count = 10
    while count > 0:
        
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
        example = '{"test_result": "pass"} or {"test_result": "fail", "recommended_changes": "description of change"}'
        output = chatgpt_chain.predict(human_input=f"""Responding in only JSON, using the following parameters "test_result": "pass/fail", "recommended_changes": "description of change"
        Be careful to always use double quotes for strings in the json string 
        Please review the previous output: {response} 
        Confirm if it has met the objectives to {description}
        With these parameters: {values}
        Additional Notes: {feedback}


        Original Code:{original}
        

        Example AI Response: {example}
        """)

        print(output)
        try:
            return json.loads(output)
        except Exception as e:
            feedback = f'result must be in JSON format. As an example {example}'
            count -= 1
            pass
    return {"test_result": "fail"}

def ai_suggest_test_parameters(original, name, description, parameters):
    count = 2
    feedback = ""
    while count > 0:
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
        Be careful to always use double quotes for strings in the json string 
        To meet the objectives to {description}
        Feedback: {feedback}
        
        
        Original Code:{original}
        

        Example AI Response: {example}
        """)

        print(output)
        try:
            response = json.loads(output)
            print(f"TESTER - GET_PARAMETERS - {response}")
            return response
        except Exception as e:
            print(f"TESTER - GET_PARAMETERS - error: {e}")
            feedback = f'result must be in JSON format enclosed in double quotes. {e}'
            count -= 1
            pass
    return None