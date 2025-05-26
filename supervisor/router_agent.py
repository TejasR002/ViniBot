from langchain.memory import ConversationBufferMemory
from supervisor.supervisor import supervisoragent
from agents.schedulingAgent import  AppointmentScheduleAgent
from agents.medicineAgent import MedicineInventory
from agents.caseGeneratorAgent import CaseGeneratorAgent
from dotenv import  load_dotenv
load_dotenv()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
def router_agent_executer(query: str) :

    agent_name = None
    tool_used = None
    agent_thought = ""

    agent = supervisoragent(query)
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
    return {"output": output, "tool": tool_used,"agent_thought": agent_thought,"agent": agent, "memory": memory.buffer, "chat_history": memory.chat_memory}