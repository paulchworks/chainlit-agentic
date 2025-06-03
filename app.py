import chainlit as cl
import boto3
import json
import logging
import pprint
from datetime import datetime
#import dotenv 

# Load environment variables from .env file
#dotenv.load_dotenv()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Set up logging
logging.basicConfig(
    format='[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set up AWS clients
region = 'us-west-2'
session = boto3.Session(region_name=region)
lambda_client = session.client('lambda')
bedrock_agent_runtime_client = session.client('bedrock-agent-runtime')

# Define the invokeAgent function
def invokeAgent(query, session_id, enable_trace=True, session_state=dict()):
    end_session = False
    agentResponse = bedrock_agent_runtime_client.invoke_agent(
        inputText=query,
        agentId='',
        agentAliasId='',
        sessionId=session_id,
        enableTrace=enable_trace, 
        endSession=end_session,
        sessionState=session_state
    )
    
    event_stream = agentResponse['completion']
    try:
        for event in event_stream:        
            if 'chunk' in event:
                data = event['chunk']['bytes']
                if enable_trace:
                    logger.info(f"Final answer ->\n{data.decode('utf8')}")
                agent_answer = data.decode('utf8')
                return agent_answer
            elif 'trace' in event:
                if enable_trace:
                    logger.info(json.dumps(event['trace'], indent=2, cls=DateTimeEncoder))
            else:
                raise Exception("unexpected event.", event)
    except Exception as e:
        raise Exception("unexpected event.", e)

@cl.on_chat_start
async def start_chat():
    # Initialize session state
    cl.user_session.set("messages", [])
    cl.user_session.set("sessionId", "None")
    
    # Add title and header
    await cl.Message(content="# Multi-Agent Collaboration\n## using Amazon Bedrock Agents").send()
    await cl.Message(content="**Orchestrator Agent:**").send()

@cl.on_message
async def main(message: cl.Message):
    # Get session state
    messages = cl.user_session.get("messages")  # type: list
    sessionId = cl.user_session.get("sessionId")
    
    # Append user message
    messages.append({"role": "user", "content": message.content})
    
    # Get agent response
    result = invokeAgent(message.content, sessionId)
    messages.append({"role": "assistant", "content": result})
    
    # Update session state
    cl.user_session.set("messages", messages)
    
    # Send assistant response
    await cl.Message(content=result).send()

# Add footer using on_stop to ensure it's shown after all messages
@cl.on_stop
async def show_footer():
    await cl.Message(content="For inquiries, contact PaulchWorks").send()
