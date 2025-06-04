from langchain.agents import create_react_agent,AgentExecutor,Tool
from langchain_openai import ChatOpenAI
from prompts.caseGeneratorPrompt import CASEGENERATORPROMPT
from data.data import  patients_db
from DataManager.managePatient import PatientDBTools
from langchain_core.output_parsers import StrOutputParser
from config import key
from tools.tools import get_patient_data

key = key


patient_tools = PatientDBTools(patients_db)


def CaseGeneratorAgent(query:str,memory):
    # Initialize LLM
    model = ChatOpenAI(model="gpt-4o-mini", api_key=key)
    # Wrap tools properly
    tools = [
        Tool(name = "showPatientDetails",
             func = patient_tools.query_patient,
             description="uery patient record by name. from patient_db "),
    #    get_patient_data,

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
        "chat_history":memory
})
    output_parser = StrOutputParser()

    # This assumes `raw_output` is a dict like {'output': 'some string'}
    parsed_output = output_parser.invoke(response['output'])
    return parsed_output