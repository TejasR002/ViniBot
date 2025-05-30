from langchain_openai import ChatOpenAI
from langchain_core.memory import BaseMemory
from sympy.codegen.ast import continue_

from agents.dataverificationagent import dataverificationagent
from supervisor.supervisor import supervisoragent
from agents.schedulingAgent import  AppointmentScheduleAgent
from agents.medicineAgent import MedicineInventory
from agents.caseGeneratorAgent import CaseGeneratorAgent
from dotenv import  load_dotenv
load_dotenv()
model = ChatOpenAI(model='gpt-4.1-nano', temperature=0)
from agentmemory.inmemory import memory


def router_agent_executer(query: str,memory = memory) :

    agent_name = None
    tool_used = None
    agent_thought = ""

    agent = supervisoragent(query, memory)
    updated_memory = memory.buffer
    agent_thought += f"Supervisor decided to use: {agent}\n"

    print("I am in router agent" , agent)
    if not dataverificationagent(query):
        if agent == "AppointmentScheduleAgent":
            tool_used = "AppointmentScheduleAgentTool"
            output = AppointmentScheduleAgent(query , memory)
            print(memory.buffer_as_messages)
        elif agent == "CaseGeneratorAgent":
            tool_used = "CaseGeneratorAgent"
            output = CaseGeneratorAgent(query,memory)
            print(memory.buffer_as_messages)
        elif agent == "Maintain Inventory":
            tool_used = "Maintain InventoryTool"
            output = MedicineInventory(query,memory)
            print(memory.buffer_as_messages)
        else:
            output = "Currently this feature is not available, wait for future improvements"
    else:
        return "some required data is missing, please check the data and try again,Enter name ,age, gender, email, phone_no and address"
    print("before memory")
    print(memory)
    print("after memory")
    return {"output": output, "tool": tool_used,"agent_thought": agent_thought,"agent": agent, "memory": memory.buffer_as_messages, "chat_history": memory}