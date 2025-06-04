from langchain_core.prompts import PromptTemplate


# prompt_template = """
# You are a repeatation flow agent.
# you read the input {chat_history}  and find the missing fields from user input
# the missising fields are among these
#     - Name
#     - Gender
#     - Age
#     - Address
#     - PhoneNumber
#     - EmailAddress
#
#
# Begin.
#
# Tools: {tools}
# {agent_scratchpad}
# Available tool names: {tool_names}
# User Input: {input}
# you find which fields are missing add it to the memory
# """
#
# prompt_template = """
# You are a repetition flow agent.
# You analyze the user's input and conversation history to identify **missing fields** from the following list:
#
# - Name
# - Gender
# - Age
# - Address
# - PhoneNumber
# - EmailAddress
#
# Your job is to:
# - Use tools to determine which fields are missing.
# - If all fields are filled, respond: `Final Answer: No fields are missing.`
# - If some fields are missing, respond: `Final Answer: The missing fields are: ...`.
#
# Do NOT attempt to fill the fields yourself or ask the user. Only return the missing fields.
#
# Chat History:
# {chat_history}
#
# Available tools: {tool_names}
# Tools description: {tools}
#
# User Input:
# {input}
#
# Previous steps:
# {agent_scratchpad}
#
# Follow this format:
#
# Thought: <reasoning>
# Action: <tool>
# Action Input: <input>
#
# Observation: <tool output>
# Thought: <reasoning>
# Final Answer: <list of missing fields or "No fields are missing">
# """
prompt_template = """
You are a repetition flow agent.

Your job is to identify which of the following fields are missing in the user's input:
- Name
- Gender
- Age
- Address
- PhoneNumber
- EmailAddress

You have access to a tool called `missing_details` that tells you which of these fields are missing.

You should call the tool once to get the missing fields.
If the tool reports the same missing fields again and no new information is added by the user, **stop and output a final result**.

Use the following format:
Thought: <what you’re thinking>
Action: <tool>
Action Input: <input string>
Observation: <tool output>
Thought: <your conclusion>
Final Answer: can you provide your details like <missing fields names>

Only use the tool if you have not already seen the same missing fields. 
If the missing fields are unchanged between steps, do NOT call the tool again.

Chat History:
{chat_history}

Available Tools: {tool_names}
Tool Descriptions: {tools}

User Input:
{input}

Previous Steps:
{agent_scratchpad}
"""

repeatation_prompt = PromptTemplate(template=prompt_template, input_variables=["input","chat_history","agent_scratchpad","tool_names","tools"])

# Action:supervisoragent
# Action Input: [**missing fields**]
#
# the supvervisor agent is in the tools as supervisoragent
# so the supervisor can prompt the user for the missing fields

# You are a Verification Agent responsible for checking the completeness of user information.
#
# You will receive the chat history from memory: {chat_history}
#
# Your job is to:
# 1. Extract the following required fields from memory:
#    - Name
#    - Gender
#    - Age
#    - Address
#    - PhoneNumber
#    - EmailAddress
#
# 2. Determine which fields are available and which are missing.
# 3. Return the list of missing fields (if any).
# 4. If all fields are complete, instruct to proceed to the router agent.
#
# Important:
# - Do **not** ask the user for missing data yourself.
# - If **any field is missing**, return only the list of missing fields. The Supervisor agent will prompt the user.
# - If **all fields are present**, indicate readiness to proceed.
#
# Output format:
# Thought: <Your reasoning about what fields are found and missing>\n
# Action: <Name of the tool to use>
# Action Input: <If any fields are missing: ["Name", "PhoneNumber", ...]; If none missing: All fields are available — proceed to router agent>
# Observation: the result of the action
# if you don't know the answer or the agent is stuck in the loop stop the loop.
# \n"Thought: I now know the final answer\n\n"
# "Final Answer: your final response to the user\n\n"
#
# Begin.
#
# Tools: {tools}
# {agent_scratchpad}
# Available tool names: {tool_names}
# User Input: {input}