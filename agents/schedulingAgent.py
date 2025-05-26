from langchain.agents import create_react_agent,AgentExecutor,Tool
from langchain_openai import ChatOpenAI
from tools.appointmentSchedularTools import email_tool,mail_wrapper,send_email
from data.data import  appointments_schedule
from prompts.appointmentSchedularPrompt import SchedualingPrompt
from DataManager.manageAppointment import appointmentDBTools
from langchain_core.output_parsers import StrOutputParser
from config import key
key = key

#load object with dummy data for easy access for the llm
appointments = appointmentDBTools(appointments_schedule)



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