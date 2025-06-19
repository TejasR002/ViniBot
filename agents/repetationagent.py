import os
from langchain.agents import create_react_agent,AgentExecutor,Tool
from langchain.memory.chat_memory import BaseChatMemory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from typing import Any , List
from langchain.tools import StructuredTool
from pydantic_core.core_schema import arguments_schema
from pydantic import BaseModel, Field
from config import key
from prompts.repeatation_prompt import repeatation_prompt
from supervisor import supervisor
from langchain_core.messages import BaseMessage

from tools.tools import missing_data

key = key
from agentmemory.inmemory import memory


def repeat_flow(query: str, memory) :
    from langchain.agents import create_react_agent, AgentExecutor, Tool
    from langchain_openai import ChatOpenAI
    from prompts.repeatation_prompt import repeatation_prompt
    from supervisor import supervisor
    from pydantic import BaseModel, Field
    from langchain_core.output_parsers import StrOutputParser
    # = Field(..., description="The user's input query that needs to be routed")
    # : List[BaseMessage] = Field(..., description="The memory or chat history to use for decision making")
    # class SupervisorInput(BaseModel):
    #     query: any
    #     memory: str

    tools = [
        # StructuredTool.from_function(
        #     name="supervisoragent",
        #     func=supervisor.supervisoragent,
        #     description="Route the query to the appropriate agent.",
        #     args_schema=SupervisorInput,
        # ),
        Tool.from_function(
            name="missing_details",
            func = missing_data,
            description="Based on user query identify key missing fields and return it"
        )
    ]
    model = ChatOpenAI(model="gpt-4o-mini", api_key=key)


   

    print(memory.buffer if hasattr(memory, 'buffer') else str(memory))
    
    print(query )

    agent = create_react_agent(
        llm=model,
        tools=tools,
        prompt=repeatation_prompt
    )

    agent_executor = AgentExecutor(
        tools=tools,
        agent=agent,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
        memory=memory
    )
    response = agent_executor.invoke({
     "input": query,
    })

    output_parser = StrOutputParser()
    parsed_output = output_parser.invoke(response['output'])
    print("-----------------------------------This is parsed output from the repeat_flow---------------------------------")
    print(parsed_output)
    print("-----------------------------------This is parsed output from the repeat_flow---------------------------------")
    return parsed_output


