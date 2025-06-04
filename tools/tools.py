import os
from dotenv import  load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from data.data import patients_db
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from langchain.tools import  tool,Tool
import smtplib


#APPOINTMENT SCHDULAR TOOL
# @tool("email_creation", return_direct=True)
def email_tool(query: str) -> str:
    """Email Generator based on the query"""
    prompt = f"Generate the email body given the {query}"
    llm = ChatOpenAI(model='gpt-4.1-nano')

    response = llm.invoke(prompt)
    return response.content

#@Tool("email_creation", return_direct=True)
def mail_wrapper(query: str) -> str:
    """
    Wraps an email-sending operation based on a user query.

    Args:
        query (str): The content or intent to include in the email.

    Returns:
        str: Status or response message from the email process.
    """
    print("I am in mail wrapper" , query)
    email,query= query.split(",")
    print(email)
    print("after spliting ")
    print(query)
    return send_email(query,email)



# @tool("email_send", return_direct=True)
def send_email( query: str,email: str, subject="Appointment Schedule") -> str:
    """send the mail to given email with given subject: Appointment Schedule and body given in the function ."""
    try:
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('EMAIL_APP_PASSWORD')  # App password, not your Gmail password

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        llm = ChatOpenAI(model = "gpt-4.1-nano")
        prompt = (f"""Generate the email body given the {query} in the format "
                   
                   Name: Patient name
                   Age: Patient age
                   Condition: Patient condition
                   Email: Patient email
                   Time: Appointment time
                   Location : Shakti 
                """)
        body = llm.invoke(query)
        print(body)
        # discription = body | StrOutputParser()

        # Compose the email
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = subject  #"Appointment Schedule"
        message.attach(MIMEText(body.content, 'plain'))

        server.sendmail(sender_email, email, message.as_string())
        server.quit()

        return "\nEmail sent successfully!\n"
    except Exception as e:
        return f"\nError: {str(e)}\n"


# CASE GENERATOR TOOLS

def request_user_input(message: str) -> str:
    """Ask the user for input with a custom message."""
    return input(f"{message}\n> ")

@tool("ask for details of the new patient",return_direct=True)
def get_patient_data(patient_name: str) -> dict:
    """Asks Patient for getting the data and added them to patients_db"""
    patient_data = {}
    data = ['Address', 'Age', 'Marital_status', 'sex', 'phone_no', 'mail']
    for d in data:
        if d != 'Age' or 'phone_name':
            patient_data[d] = input(f"Enter your {d}")
        else:
            patient_data[d] = int(input(f"Enter your {d}"))
    patients_db[patient_name] = patient_data
    return patient_data


def show_details(patient_name: str) -> dict:
    """Gives the  data of the patient from patient's name"""
    patient_data = patients_db[patient_name]
    return patient_data

# SUPERVISOR TOOLS



def missing_data(query:str):
    """Checks if the required data is missing in the query"""
    required_data = ['Name', 'Age', 'Gender', 'Email', 'Phone_no', 'Address']
    missed_data = "These data are missing: "
    for data in required_data:
        if data.lower() not in query:
           missed_data = missed_data + data + ", "
    print(missed_data)
    return missed_data
