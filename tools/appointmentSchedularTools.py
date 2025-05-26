import os
from langchain_core.tools import  tool
from dotenv import  load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib






@tool("email_creation", return_direct=True)
def email_tool(query: str) -> str:
    """Email Generator based on the query"""
    prompt = f"Generate the email body given the {query}"
    llm = ChatOpenAI(model='gpt-4.1-nano')

    response = llm.invoke(prompt)
    return response.content

@tool("email_creation", return_direct=True)
def mail_wrapper(query: str) -> str:
    """sends the appointment mail to the patient's email id, it recieves the email id and the query seperated by comma, e.g 2x3osjs@gmail.com <- mail extracted from the query given by the user, the query given by the user.."""
    print("I am in mail wrapper", query)
    email, query = query.split(",")
    print(email)
    print("after spliting ")
    print(query)
    return send_email(query, email)


@tool("email_send", return_direct=True)
def send_email(query: str, email: str, subject="Appointment Schedule") -> str:
    """send the mail to given email with given subject: Appointment Schedule and body given in the function ."""
    try:
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('EMAIL_APP_PASSWORD')  # App password, not your Gmail password

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        llm = ChatOpenAI(model="gpt-4.1-nano")
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
        message['Subject'] = subject  # "Appointment Schedule"
        message.attach(MIMEText(body.content, 'plain'))

        server.sendmail(sender_email, email, message.as_string())
        server.quit()

        return "\nEmail sent successfully!\n"
    except Exception as e:
        return f"\nError: {str(e)}\n"