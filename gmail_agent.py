from langchain_community.agent_toolkits import GmailToolkit
import getpass
import os
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import pandas as pd


## types of AI invokations from google API. 
## create_gmail_draft, send_gmail_message, search_gmail, get_gmail_message, get_gmail_thread
# Load in the variables from your enviornment



load_dotenv()

## use these imports  pass in your credentias and allow access to 
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)


# get_gmail_credentials you need to pass in the different authorizations from the api
credentials = get_gmail_credentials(
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
    token_file="token.json"
)

api_resource = build_resource_service(credentials=credentials)

# able to interact with API
toolkit = GmailToolkit(api_resource=api_resource)


tools = toolkit.get_tools()


# create instructions for prompting
instructions = """You are an assistant."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)



# allows for how much creativity is in the prompt
llm = ChatOpenAI(temperature=.7)

# allows you to create an agent from the open AI tools you passed in. 
agent = create_openai_tools_agent(llm, toolkit.get_tools(), prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True, 
)

# agen allows for you to execute a message
output = agent_executor.invoke({"input": "search through the last 3 messages i recieved and tell me what they are."})

email_data = output.get('output')

print(email_data)

