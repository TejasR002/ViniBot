import os

from langchain.agents import create_react_agent,AgentExecutor,Tool
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

from prompts.caseGeneratorPrompt import CASEGENERATORPROMPT
from prompts.medicineInventoryPrompt import medicinePrompt
# from tools.tools import mail_wrapper
from tools.appointmentSchedularTools import email_tool,mail_wrapper,send_email
from data.data import  patients_db,appointments_schedule,medicine_inventory
from prompts.appointmentSchedularPrompt import SchedualingPrompt
from DataManager.managePatient import PatientDBTools
from DataManager.manageMedicine import  medicineDBTools
from DataManager.manageAppointment import appointmentDBTools
from langchain_core.output_parsers import StrOutputParser
from dotenv import  load_dotenv
# from langchain_community.callbacks.streamlit import (
#     StreamlitCallbackHandler,
# )

# Instantiate the tool manager with your dictionary
patient_tools = PatientDBTools(patients_db)
stock = medicineDBTools(medicine_inventory)
appointments = appointmentDBTools(appointments_schedule)




# Load API key
load_dotenv()
key = os.getenv('OPENAI_API_KEY')


# Memory for agents


class NoInput(BaseModel):
    pass

# APPPOINTMENT AGENT
def AppointmentScheduleAgent(query:str , memory):
    # Initialize LLM
    model = ChatOpenAI(model="gpt-4.1-nano", api_key=key)
    # Wrap tools properly

    tools = [
        Tool(
            name="CheckAppointmentStatus",
            func=appointments.appointment_status,
            description="check  if there is free appointment recenlty."),
        mail_wrapper,email_tool,send_email
        ,
        Tool(
            name="ListAvailableAppointment",
            func=appointments.list_available,
            description="list all available appointments from the dummy data"

        ),
        Tool(name="SlotAssignment",
             func=appointments.assign_slot,
             description="Assigns to recent available slot"

             )
    ]

    # ReceptionistTemplate="""\nYou are an intelligent agent designed to reason step-by-step and solve complex problems using external tools.\n
    #     "\nConversation history (if relevant):\n"
    #     "\n{chat_history}\n\n"
    #     "You have access to the following tools:\n"
    #     "{tools}\n\n"
    #     "When solving a problem, follow this structured format:\n\n"
    #     "Question: the user’s question\n\n"
    #     "Thought: your reasoning about what to do next\n\n"
    #     "Action: the action to take , strictly use only this [{tool_names}]\n\n"
    #     "Action Input: the input required for the action from the user {action_input}\n\n"
    #     "Observation: the result of the action\n\n"
    #     "... (repeat Thought/Action/Action Input/Observation as needed)\n\n"
    #     \n"Thought: I now know the final answer\n\n"
    #     "Final Answer: your final response to the user\n\n"
    #     "Begin below:\n\n"
    #     "Question: {input}\n\n"
    #     "Thought: {agent_scratchpad}\n\n"
    # )
    # """
    # Define the prompt template with required variables

    # Create the agent
    agent = create_react_agent(
        llm=model,
        tools=tools,
        prompt= SchedualingPrompt
    )
    agent_executor = AgentExecutor(
        tools= tools,
        agent= agent,
        verbose= True,
        max_iterations=50,
        memory=memory,
        handle_parsing_errors=True
     )
    # Call agent

    response = agent_executor.invoke({
        "input": query,

})
    print(response)
    output_parser = StrOutputParser()

    # This assumes `raw_output` is a dict like {'output': 'some string'}
    parsed_output = output_parser.invoke(response['output'])
    print(parsed_output)
    return parsed_output



# CASEGENERATOR AGENT
def CaseGeneratorAgent(query:str,memory):
    # Initialize LLM
    model = ChatOpenAI(model="gpt-4.1-nano", api_key=key)
    # Wrap tools properly
    tools = [
        Tool(name = "showPatientDetails",
             func = patient_tools.query_patient,
             description="uery patient record by name. from patient_db "),

        Tool(name="InsertPatient",
             func=patient_tools.insert_patient,
             description="Insert a new patient using 'Insert Name, Age, Condition'."),

        Tool(name="UpdatePatient",
             func=patient_tools.update_patient,
             description="Update patient record using 'Update Name, field=value, ...'."),

        Tool(name="DeletePatient",
             func=patient_tools.delete_patient,
             description="Delete a patient using 'Delete Name'."),
        # Tool(name="request_user_input",func=request_user_input,description="Ask the user for input with a custom message.")
    ]

#     prompt = PromptTemplate(
#     input_variables=["input", "agent_scratchpad", "tool_names", "tools", "chat_history"],
#     template=(
#         "You are an intelligent agent designed to reason step-by-step and solve complex problems using external tools.\n\n"
#         "If the user's current question depends on earlier conversation, refer to the relevant context provided in the chat history.\n"
#         "Use prior information, clarifications, and tool results as needed to build on earlier steps.\n\n"
#         "Conversation history (if relevant):\n"
#         "{chat_history}\n\n"
#         "You have access to the following tools:\n"
#         "{tools}\n\n"
#         "When solving a problem, follow this structured format:\n\n"
#         "Question: the user’s question\n"
#         "Thought: your reasoning about what to do next (including references to chat history if helpful)\n"
#         "Action: the action to take, should be one of [{tool_names}] (write only the name, do NOT include parentheses)\n"
#         "Action Input: the input required for the action\n"
#         "Observation: the result of the action\n"
#         "... (repeat Thought/Action/Action Input/Observation as needed)\n"
#         "Thought: I now know the final answer\n"
#         "Final Answer: your final response to the user\n\n"
#
#         "!Begin below:\n\n"
#         "Question: {input}\n"
#         "Thought: {agent_scratchpad}"
#     )
# )

    # Create the agent
    agent = create_react_agent(
        llm=model,
        tools=tools,
        prompt= CASEGENERATORPROMPT
    )
    agent_executor = AgentExecutor(
         tools= tools,
        agent= agent,
        verbose= True,
        memory=memory,
        max_iterations=50,
        handle_parsing_errors=True
     )

    # Call agent
    response = agent_executor.invoke({
        "input": query,
        "chat_history":[],
})
    output_parser = StrOutputParser()

    # This assumes `raw_output` is a dict like {'output': 'some string'}
    parsed_output = output_parser.invoke(response['output'])
    return parsed_output

# INVENTORYMANAGMENT AGENT
def MedicineInventory(query:str,memory):
    # Initialize LLM
    model = ChatOpenAI(model="gpt-4.1-nano", api_key=key)
    # Wrap tools properly
    tools = [
        Tool(name="GetStock",
             func=stock.get_stock,
             description="fetches all stock  details"
             ),
        Tool(name="Checktotalstock",
             func=stock.list_available,
             description="list all available stock in the medicine inventory"),
    ]

    # ReceptionistTemplate="""\nYou are an intelligent agent designed to reason step-by-step and solve complex problems using external tools.\n
    #     "\nConversation history (if relevant):\n"
    #     "\n{chat_history}\n\n"
    #     "You have access to the following tools:\n"
    #     "{tools}\n\n"
    #     "When solving a problem, follow this structured format:\n\n"
    #     "Question: the user’s question\n\n"
    #     "Thought: your reasoning about what to do next\n\n"
    #     "Action: the action to take , strictly use only this [{tool_names}]\n\n"
    #     "Action Input: the input required for the action from the user\n\n"
    #     "Observation: the result of the action\n\n"
    #     "If the tool call is finished and the data is received successfully stop the loop"
    #     "... (repeat Thought/Action/Action Input/Observation as needed)\n\n"
    #     \n"Thought: I now know the final answer\n\n"
    #     "Final Answer: your final response to the user\n\n"
    #     "Begin below !:\n\n"
    #     "Question: {input}\n\n"
    #     "Thought: {agent_scratchpad}\n\n"
    # )
    # """
    # # Define the prompt template with required variables
    # prompt = PromptTemplate(template=ReceptionistTemplate,input_variables=["input", "agent_scratchpad", "tool_names", "tools", "chat_history"])

    # Create the agent
    agent = create_react_agent(
        llm=model,
        tools=tools,
        prompt= medicinePrompt
    )
    agent_executor = AgentExecutor(
         tools= tools,
        agent= agent,
        verbose= True,
        memory=memory,
        max_iterations=15,
        handle_parsing_errors=True
     )

    # Call agent
    response = agent_executor.invoke({
        "input": query,

})
    output_parser = StrOutputParser()

    # This assumes `raw_output` is a dict like {'output': 'some string'}
    parsed_output = output_parser.invoke(response['output'])
    return parsed_output