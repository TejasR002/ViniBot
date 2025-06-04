from supervisor.router_agent import router_agent_executer
import  streamlit as st
from agentmemory.inmemory import memory

st.markdown(
    """
    <style>
    .big-font {
        font-size:22px ;
    }
    .stTextInput > div > div > input {
        font-size: 20px !important;
    }
    .stButton > button {
        font-size: 20px !important;
    }
    /* Expand the expander size and font */
    [data-testid="stExpander"] {
        font-size: 20px;
        width: 100% !important;
    }

    [data-testid="stExpander"] div[role="button"] {
        font-size: 22px;
        padding: 10px;
    }

    [data-testid="stExpander"] .streamlit-expanderContent {
        font-size: 20px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Virtual Receptionist [Vini]")

if 'history' not in st.session_state:
    st.session_state.history = []

# User input box
user_input = st.chat_input("Enter your request:")

# Display chat history
for speaker, message in st.session_state.history:
    if speaker == "User":
        with st.chat_message("user"):
            st.markdown(message)
    elif speaker == "Assistant":
        with st.chat_message("Assistant"):
            st.markdown(message['output'])

# Process new user input
# if user_input:
#     # Show user's message
#     with st.chat_message("user"):
#         st.markdown(user_input)
#
#     with st.spinner("Let me find the best travel ideas for you..."):
#         agent = identify_task(user_input)
#         if agent:
#             response = route_task(agent, user_input)
#         else:
#             response = "Sorry, I couldn't understand your request."
#
#         # If response is a dictionary, extract just the main text
#         if isinstance(response, dict):
#             response = response.get("output", str(response))
#
#     # Show bot's response
#     with st.chat_message("assistant"):
#         st.markdown(response)
#
#     # Save to session state
#     st.session_state.history.append(("User", user_input))
#     st.session_state.history.append(("Bot", response))


if user_input:
    # Log user message
    with st.chat_message("user"):
        st.markdown(user_input)
    # try:
    # Supervisor processes the input
    with st.spinner("Thinking..."):
        response = router_agent_executer(user_input , memory)
        if type(response) != str:
            agent_name = response["agent"]
            agent_thought = response["agent_thought"]
            tool_used = response["tool"]
            output = response["output"]
            memory = response["memory"]
            st.session_state.history.append((
                "Assistant",
                {
                    "output": output,
                    "user_input": user_input,
                    "agent_name": agent_name,
                    "tool_used": tool_used,
                    "agent_thought": agent_thought,
                    "memory": memory
                }
            ))
    # Show bot's response
    with st.chat_message("Assistant"):
        st.markdown(response['output'])

    # Save to session state
    st.session_state.history.append(("User", user_input))
    st.session_state.history.append(("Assistant", response))
    # except Exception as e:
    #     st.error(f"Error: {str(e)}")

    # Log assistant response with metadata in history
