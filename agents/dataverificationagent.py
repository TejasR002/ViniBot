from langchain.memory.chat_memory import BaseChatMemory
from langchain_openai import  ChatOpenAI
from langchain.agents import create_react_agent
from langchain.agents import  AgentExecutor
from langchain.agents.agent import AgentOutputParser
from langchain.schema.agent import AgentAction, AgentFinish
from prompts.dataverificationpropmt import verification_prompt
from tools.caseGeneratorTools import find_patient_in_data
from dotenv import  load_dotenv
from typing import Union
import re
load_dotenv()



class CustomReActOutputParser(AgentOutputParser):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        # Check if the action is 'Final Answer'
        action_match = re.search(r"Action\s*:\s*(.*)", text)
        input_match = re.search(r"Action Input\s*:\s*(.*)", text)

        if action_match and input_match:
            action = action_match.group(1).strip()
            action_input = input_match.group(1).strip().strip('"')

            # If the action is Final Answer, return finish with the output
            if action.lower() == "final answer":
                # Accept True/False as output (case insensitive)
                if action_input.lower() in ("true", "false"):
                    return AgentFinish(
                        return_values={"output": action_input},
                        log=text
                    )
                else:
                    raise ValueError(f"Final Answer input should be True or False, got: {action_input}")

            # Otherwise return AgentAction to continue
            return AgentAction(
                tool=action,
                tool_input=action_input,
                log=text
            )

        raise ValueError(f"Could not parse LLM output: `{text}`")


def dataverificationagent(query:str,memory)->bool:

    model = ChatOpenAI(model='gpt-4o-mini', temperature=0)

    tools = [find_patient_in_data]
    agent = create_react_agent(llm=model, tools=tools,prompt=verification_prompt,output_parser=CustomReActOutputParser())

    agent_executor = AgentExecutor(
        tools=tools,
        agent=agent,
        verbose=True,
        max_iterations=5,
        memory=memory,
        handle_parsing_errors=True
    )

    # Call agent
    response = agent_executor.invoke({
        "input": query,
        "chat_history":memory.buffer_as_messages
    })


    answer = response.get("output", "").strip()
    print("\ninside the data verification agent\n")
    return answer.lower() == "true"
    # # This assumes `raw_output` is a dict like {'output': 'some string'}
    # parsed_output = output_parser.invoke(response['output'])
    # x = bool(parsed_output)
    # return x



