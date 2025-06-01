from streamlit import chat_input
from sympy.codegen.ast import continue_

# OLD CODE OF AGENT
from data.data import patients_db
from agents.dataverificationagent import dataverificationagent
from langchain.memory import ConversationBufferMemory
from supervisor.router_agent import router_agent_executer
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
        # try:
            # Supervisor processes the input
        with st.spinner("Thinking..."):
            response = router_agent_executer(user_input)
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
            else:
                st.session_state.history.append(("Assistant", response))
        # except Exception as e:
        #     st.error(f"Error: {str(e)}")

        # Log assistant response with metadata in history

for x in st.session_state.history:
    print("******************************************************************************************************************************")
    print(x)
#
for sender, message in st.session_state.history:
     # if sender == "User":
     #     st.markdown(f"**👤 {sender}:** {message}")
     #    elif sender == "Assistant":
     if isinstance(message, dict):
         st.markdown(f"**🤖 {sender}:** {message['output']}")
         with st.expander("🤖 Agent Info", expanded=True):
                st.markdown(f'<div class="big-font"><b>UserQuery:</b> {message["user_input"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="big-font"><b>Agent Used:</b> {message["agent_name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="big-font"><b>Tool Used:</b> {message["tool_used"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="big-font"><b>Agent Thought:</b></div><div class="big-font"><b>{message["agent_thought"]}</b></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="big-font"><b>Agent Output:</b> {message["output"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="big-font"><b>Agent Memory:</b></div><div class="big-font"><b>{message["memory"]}</b></div>', unsafe_allow_html=True)
     else:
        st.markdown(f"**🤖 {sender}:** {message}")

# NEW CODE WITH FORM PART 1

# from supervisor.router_agent import router_agent_executer
# import streamlit as st
#
# # ---------------- STYLE ---------------- #
# st.markdown(
#     """
#     <style>
#     .big-font {
#         font-size:22px ;
#     }
#     .stTextInput > div > div > input {
#         font-size: 20px !important;
#     }
#     .stButton > button {
#         font-size: 20px !important;
#     }
#     [data-testid="stExpander"] {
#         font-size: 20px;
#         width: 100% !important;
#     }
#     [data-testid="stExpander"] div[role="button"] {
#         font-size: 22px;
#         padding: 10px;
#     }
#     [data-testid="stExpander"] .streamlit-expanderContent {
#         font-size: 20px;
#         padding: 20px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
#
# # ---------------- INIT SESSION ---------------- #
# st.title("Virtual Receptionist [Vini]")
#
# if 'history' not in st.session_state:
#     st.session_state.history = []
#
# if 'patient_db' not in st.session_state:
#     st.session_state.patient_db = [patients_db
#         # {
#         #     'name': 'John Doe',
#         #     'address': '123 Main St',
#         #     'phone': '1234567890',
#         #     'sex': 'Male',
#         #     'age': 35,
#         #     'email': 'john@example.com'
#         # },
#         # {
#         #     'name': 'Johnathan Doe',
#         #     'address': '456 Elm St',
#         #     'phone': '9876543210',
#         #     'sex': 'Male',
#         #     'age': 40,
#         #     'email': 'johnathan@example.com'
#         # }
#     ]
#
# if 'form_submitted' not in st.session_state:
#     st.session_state.form_submitted = False
#
# if 'user_input' not in st.session_state:
#     st.session_state.user_input = ""
#
# # ---------------- CLEAR INPUT CALLBACK ---------------- #
# def clear_input():
#     st.session_state.query_input = " "
#
# # ---------------- PATIENT HANDLER ---------------- #
#
#
#
# # Optional reset
# if st.session_state.form_submitted:
#     if st.button("Reset Form"):
#         st.session_state.form_submitted = False
#
# # ---------------- CHATBOT INTERFACE ---------------- #
#
# chat_input = st.text_input("Enter your request:")
# if dataverificationagent(chat_input):
#     # Controlled input field for patient name
#     # st.text_input("Enter patient's name", key='user_input')
#     #
#     # if st.session_state.user_input:
#     #     matches = [
#     #         p for p in st.session_state.patient_db
#     #         if st.session_state.user_input.lower() in p['name'].lower()
#     #     ]
#     #
#     #     if matches:
#     #         st.success(f"Found {len(matches)} matching patient(s). Please select the correct one.")
#     #
#     #         selected_index = st.radio(
#     #             "Select a patient",
#     #             options=list(range(len(matches))),
#     #             format_func=lambda i: f"{matches[i]['name']} ({matches[i]['age']} y/o, {matches[i]['email']})"
#     #         )
#     #
#     #         selected_patient = matches[selected_index]
#     #
#     #         st.write("### Selected Patient Details")
#     #         for k, v in selected_patient.items():
#     #             st.write(f"**{k.capitalize()}**: {v}")
#     #
#     #         st.button("Confirm Patient", on_click=clear_input)
#     #
#     #     elif not st.session_state.form_submitted:
#     #         st.warning("No matching patient found. Please enter details manually.")
#
#         with st.form("patient_form"):
#             name = st.text_input("Name", value=st.session_state.user_input)
#             address = st.text_input("Address")
#             phone = st.number_input("Phone Number",min_value=1000000000,max_value=9999999999)
#             sex = st.selectbox("Sex", ["Male", "Female", "Other"])
#             age = st.number_input("Age", min_value=0, max_value=120)
#             email = st.text_input("Email Address")
#             submitted = st.form_submit_button("Submit")
#
#             if submitted:
#                 errors = []
#                 if not name.strip():
#                     errors.append("Name is required.")
#                 if not address.strip():
#                     errors.append("Address is required.")
#                 if not phone.strip():
#                     errors.append("Phone number is required.")
#                 if not email.strip():
#                     errors.append("Email address is required.")
#                 if age == 0:
#                     errors.append("Age must be greater than 0.")
#
#                 if errors:
#                     for error in errors:
#                         st.error(error)
#                 else:
#                     new_record = {
#                          f"{name.strip()}":
#                         {
#                         "Address": address.strip(),
#                         "PhoneNumber": phone.strip(),
#                         "Gender": sex,
#                         "Age": age,
#                         "EmailAddress": email.strip() }
#                     }
#                     st.session_state.patient_db.append(new_record)
#                     st.session_state.form_submitted = True
#                     st.success("Patient information saved!")
#                 clear_input()
# if st.button("Submit"):
#     if chat_input:
#         st.session_state.history.append(("User", chat_input))
#         try:
#             with st.spinner("Thinking..."):
#                 response = router_agent_executer(chat_input)
#                 agent_name = response["agent"]
#                 agent_thought = response["agent_thought"]
#                 tool_used = response["tool"]
#                 output = response["output"]
#                 st.session_state.history.append((
#                     "Assistant",
#                     {
#                         "output": output,
#                         "user_input": chat_input,
#                         "agent_name": agent_name,
#                         "tool_used": tool_used,
#                         "agent_thought": agent_thought,
#                     }
#                 ))
#         except Exception as e:
#             st.error(f"Error: {str(e)}")
#
# # ---------------- CHAT HISTORY ---------------- #
# for sender, message in st.session_state.history:
#     if isinstance(message, dict):
#         with st.expander("🤖 Agent Info", expanded=True):
#             st.markdown(f'<div class="big-font"><b>UserQuery:</b> {message["user_input"]}</div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="big-font"><b>Agent Used:</b> {message["agent_name"]}</div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="big-font"><b>Tool Used:</b> {message["tool_used"]}</div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="big-font"><b>Agent Thought:</b></div><div class="big-font"><b>{message["agent_thought"]}</b></div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="big-font"><b>Agent Output:</b> {message["output"]}</div>', unsafe_allow_html=True)

# # NEW CODE WITH FORM PART 2
# from langchain.memory import ConversationBufferMemory
# import streamlit as st
# from data.data import patients_db
# from agents.dataverificationagent import dataverificationagent
# from supervisor.router_agent import router_agent_executer
#
# # ---------------- CSS STYLING ---------------- #
# st.markdown(
#     """
#     <style>
#     .big-font { font-size:22px; }
#     .stTextInput > div > div > input,
#     .stButton > button {
#         font-size: 20px !important;
#     }
#     [data-testid="stExpander"] {
#         font-size: 20px;
#         width: 100% !important;
#     }
#     [data-testid="stExpander"] div[role="button"] {
#         font-size: 22px;
#         padding: 10px;
#     }
#     [data-testid="stExpander"] .streamlit-expanderContent {
#         font-size: 20px;
#         padding: 20px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
#
# # ---------------- SESSION STATE INIT ---------------- #
# st.title("Virtual Receptionist [Vini]")
# if "shared_memory" not in st.session_state:
#     st.session_state.shared_memory = ConversationBufferMemory(memory_key="chat_history")
# if 'query_input' not in st.session_state:
#     st.session_state.query_input = ""
#
# if 'reset_query' not in st.session_state:
#     st.session_state.reset_query = False
#
# if "history" not in st.session_state:
#     st.session_state.history = []
#
# if "patient_db" not in st.session_state:
#     st.session_state.patient_db = patients_db
#
# if "form_submitted" not in st.session_state:
#     st.session_state.form_submitted = False
#
# if "final_patient_data" not in st.session_state:
#     st.session_state.final_patient_data = None
#
#
# # ---------------- MAIN LOGIC ---------------- #
# query = st.text_input(
#     "Enter your request:",
#     value="" if st.session_state.reset_query else st.session_state.query_input,
#     key="query_input"
# )
# # Reset the flag so future input is preserved
# if st.session_state.reset_query:
#     st.session_state.reset_query = False
#  # Safe update after rendering
# if query:
#     # Run data verification agent
#     is_new_data_needed = dataverificationagent(query)
#
#     if is_new_data_needed:
#         st.info("No existing patient data found. Please enter new details.")
#
#         with st.form("patient_form"):
#             name = st.text_input("Name")
#             address = st.text_input("Address")
#             phone = st.text_input("Phone Number")
#             sex = st.selectbox("Sex", ["Male", "Female", "Other"])
#             age = st.number_input("Age", min_value=0, max_value=120)
#             email = st.text_input("Email Address")
#             submitted = st.form_submit_button("Submit")
#
#             if submitted:
#                 errors = []
#                 if not name.strip(): errors.append("Name is required.")
#                 if not address.strip(): errors.append("Address is required.")
#                 if not phone.strip(): errors.append("Phone is required.")
#                 if not email.strip(): errors.append("Email is required.")
#                 if age <= 0: errors.append("Age must be greater than 0.")
#
#                 if errors:
#                     for error in errors:
#                         st.error(error)
#                 else:
#                     st.session_state.final_patient_data = {
#                         f"{name.strip()}":
#                         {"Address": address.strip(),
#                         "PhoneNumber": phone.strip(),
#                         "Gender": sex,
#                         "Age": age,
#                          "EmailAddress": email.strip()}
#                     }
#                     st.session_state.patient_db.update(st.session_state.final_patient_data)
#                     st.session_state.form_submitted = True
#                     st.success("Patient information saved!")
#     else:
#         st.info("Existing patients found. Please select one:")
#         matched_patients = [
#             p for p in st.session_state.patient_db
#             if query.lower() in p.get("Name", "").lower()
#         ]
#
#         if matched_patients:
#             selected_patient = st.radio(
#                 "Select a patient",
#                 matched_patients,
#                 format_func=lambda p: f"{p['Name']} ({p['Age']} y/o, {p['EmailAddress']})"
#             )
#
#             if st.button("Confirm Patient"):
#                 st.session_state.final_patient_data = selected_patient
#                 st.success("Patient selected successfully.")
#         else:
#             st.warning("No matching patients found. Please try again or enter manually.")
#
# print(f"Final patient data: {st.session_state.final_patient_data}")
# query_with_data = query + "here is patient data: " + str(st.session_state.final_patient_data) if st.session_state.final_patient_data else query
# # ---------------- ROUTER AGENT ---------------- #
# if st.session_state.final_patient_data:
#     if st.button("Continue to Process Request"):
#         try:
#             st.session_state.history.append(("User", query))
#             with st.spinner("Routing your request..."):
#                 response = router_agent_executer(query_with_data,st.session_state.shared_memory)
#                 st.session_state.history.append((
#                     "Assistant",
#                     {
#                         "output": response["output"],
#                         "user_input": query_with_data,
#                         "agent_name": response["agent"],
#                         "tool_used": response["tool"],
#                         "agent_thought": response["agent_thought"],
#                     }
#                 ))
#         except Exception as e:
#             st.error(f"Error: {str(e)}")
#         # Reset final patient state to avoid re-processing
#         st.session_state.final_patient_data = None
#         st.session_state.form_submitted = False
#         st.session_state.reset_query = True
#         st.rerun()
#
# # ---------------- HISTORY UI ---------------- #
# for sender, message in st.session_state.history:
#     if isinstance(message, dict):
#         with st.expander("🤖 Agent Info", expanded=True):
#             st.markdown(f'<div class="big-font"><b>UserQuery:</b> {message["user_input"]}</div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="big-font"><b>Agent Used:</b> {message["agent_name"]}</div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="big-font"><b>Tool Used:</b> {message["tool_used"]}</div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="big-font"><b>Agent Thought:</b></div><div class="big-font"><b>{message["agent_thought"]}</b></div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="big-font"><b>Agent Output:</b> {message["output"]}</div>', unsafe_allow_html=True)
