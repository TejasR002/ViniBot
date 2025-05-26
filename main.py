from supervisor.supervisor import router_agent_executer
import  streamlit as st
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

user_input = st.text_input("Enter your request:")

if st.button("Submit"):
    if user_input:
        # Log user message
        st.session_state.history.append(("User", user_input))

        try:
            # Supervisor processes the input
            with st.spinner("Thinking..."):
                response = router_agent_executer(user_input)
                agent_name = response["agent"]
                agent_thought = response["agent_thought"]
                tool_used = response["tool"]
                output = response["output"]

                # # Display agent reasoning and tool usage immediately
                # with st.expander("🤖 Agent Info", expanded=True):
                #     st.markdown(f"**UserQuery:** {user_input}")
                #     st.markdown(f"**Agent Used:** {agent_name}")
                #     st.markdown(f"**Tool Used:** {tool_used}")
                #     st.markdown(f"**Agent Thought:**\n```\n{agent_thought}\n```")
                #     st.markdown(f"**Output:** {output}")
                st.session_state.history.append((
                    "Assistant",
                    {
                        "output": output,
                        "user_input": user_input,
                        "agent_name": agent_name,
                        "tool_used": tool_used,
                        "agent_thought": agent_thought,
                    }
                ))
        except Exception as e:
            st.error(f"Error: {str(e)}")

        # Log assistant response with metadata in history

for x in st.session_state.history:
    print("******************************************************************************************************************************")
    print(x)

#
for sender, message in st.session_state.history:
    # if sender == "User":
    #     st.markdown(f"**👤 {sender}:** {message}")
    # elif sender == "Assistant":
    if isinstance(message, dict):
    # st.markdown(f"**🤖 {sender}:** {message['output']}")
        with st.expander("🤖 Agent Info", expanded=True):
            st.markdown(f'<div class="big-font"><b>UserQuery:</b> {message["user_input"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="big-font"><b>Agent Used:</b> {message["agent_name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="big-font"><b>Tool Used:</b> {message["tool_used"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="big-font"><b>Agent Thought:</b></div><div class="big-font"><b>{message["agent_thought"]}</b>',unsafe_allow_html=True)
            st.markdown(f'<div class="big-font"><b>Agent Output:</b> {message["output"]}</div>', unsafe_allow_html=True)
        # else:
        #     st.markdown(f"**🤖 {sender}:** {message}")

