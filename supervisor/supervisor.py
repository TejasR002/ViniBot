from typing import Optional

from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from typing import Union


def supervisoragent(query:str,memory)->str:

    model = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    # model2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    supervisor_prompt_template = """You are a multi-agent router responsible for selecting the best agent to handle the incoming user query. Choose the most suitable agent from the following options based on the task described in the query.:
    
        If the query is unclear and includes some greetings or other non-task-related language, respond politely and ask how can i help you.
    
    INSTRUCTIONS:
        if some one greets you then respond politely and ask how can i help you.
        break the query into steps and route each step to the appropriate agent.
        If any agent stuck at any point or need any data from the user, ask the user for input using agent's tools.
        If any agent has called the tool and got the answer successfully, stop the loop of that agent and continue with the next step
        if all the data required data is available like (name, age, gender, email, phone_no and address) then continue
        else ask the user for missing data and continue with the next step. 

    Available Agents:
    - AppointmentScheduleAgent: Schedules appointments for patient, checks available slots and book the slots on the name of patients.
    - CaseGeneratorAgent: Suitable for Getting the patient data and manage patient data , takes details from the user. and store it for further requirements
    - Maintain Inventory: This agent maintains the stock of the medicines and manupulates it . keeps count of medicine and checks the stock of available stuff.


    Routing Logic:
    1. If the query explicitly asks for an scheduling  appointment or slot booking route to **AppointmentScheduleAgent**.
    2. If the query requests or need the details like name age and other basic details , or any tool need the information about patient then route to  to **CaseGeneratorAgent**.
    3. if the query include any medicine detail or the stock of the medicine then  route to **Maintain Inventory**.

    
    User Query:
    {query}
    
    chat_history: {chat_history}
    
    Output Format:
    Return only the most suitable agent name.If agent is not clear ask the user for clarification or ask for the more details in polite way
    """
    # Define the prompt template with required variables
    router_prompt = PromptTemplate(template=supervisor_prompt_template, input_variables=['query'])

    llm_chain = LLMChain(prompt=router_prompt,llm=model,memory=memory)
    chain = llm_chain | StrOutputParser()
    response = chain.invoke({"query":query,"chat_history":memory})


    return response['text']




# if __name__ == "__main__":
#     query = "List all availableappointments "
#     print(" This is finaloutput ", router_agent_executer(query))
# print(supervisoragent("List all medicine",memory))