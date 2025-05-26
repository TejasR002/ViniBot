from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from agents.agents import  AppointmentScheduleAgent,CaseGeneratorAgent,MedicineInventory
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import  load_dotenv
load_dotenv()
# model2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash" )
# model2.invoke("Hello")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
def SuperVisorAgent(query:str)->str:

    model = ChatOpenAI(model='gpt-4.1-nano', temperature=0)
    model2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    router_prompt_template = """You are a multi-agent router responsible for selecting the best agent to handle the incoming user query. Choose the most suitable agent from the following options based on the task described in the query.:
    
    INSTRUCTIONS:
        If any agent stuck at any point or need any data from the user, ask the user for input using agent's tools.
        If any agent has called the tool and got the answer successfully, stop the loop of that agent and continue with the next step

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

    Output Format:
    Return only the most suitable agent name. If no agent is clearly suitable, default to **CaseGeneratorAgent**.
    """
    # Define the prompt template with required variables
    router_prompt = PromptTemplate(template=router_prompt_template, input_variables=['query'])

    chain = router_prompt | model | StrOutputParser()
    response = chain.invoke({"query":query})
    print("I am in supervisor " , response)

    return response


def router_agent_executer(query: str) :

    agent_name = None
    tool_used = None
    agent_thought = ""

    agent = SuperVisorAgent(query)
    agent_thought += f"Supervisor decided to use: {agent}\n"

    print("I am in router agent" , agent)

    if agent == "AppointmentScheduleAgent":
        tool_used = "AppointmentScheduleAgentTool"
        output = AppointmentScheduleAgent(query , memory)
    elif agent == "CaseGeneratorAgent":
        tool_used = "CaseGeneratorAgent"
        output = CaseGeneratorAgent(query,memory)
    elif agent == "Maintain Inventory":
        tool_used = "Maintain InventoryTool"
        output = MedicineInventory(query,memory)
    else:
        output = "Currently this feature is not available, wait for future improvements"
    return {"output": output, "tool": tool_used,"agent_thought": agent_thought,"agent": agent, "memory": memory.buffer, "chat_history": memory.chat_memory,}

# if __name__ == "__main__":
#     query = "List all available appointments "
#     print("This is final output" , router_agent_executer(query))