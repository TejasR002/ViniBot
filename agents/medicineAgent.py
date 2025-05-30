import os
from langchain.agents import create_react_agent,AgentExecutor,Tool
from langchain_openai import ChatOpenAI
from prompts.medicineInventoryPrompt import medicinePrompt
from data.data import  medicine_inventory
from DataManager.manageMedicine import  medicineDBTools
from langchain_core.output_parsers import StrOutputParser
from config import key
key = key


stock = medicineDBTools(medicine_inventory)


def MedicineInventory(query:str,memory):
    # Initialize LLM
    model = ChatOpenAI(model="gpt-4o-mini", api_key=key)
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
        "chat_history":memory.chat_memory.messages

})
    output_parser = StrOutputParser()

    # This assumes `raw_output` is a dict like {'output': 'some string'}
    parsed_output = output_parser.invoke(response['output'])
    return parsed_output