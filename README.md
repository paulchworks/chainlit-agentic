Pet Store Chatbot with Amazon Bedrock Muilt-Agent Workflow and Chainlit

![image](https://github.com/user-attachments/assets/3c1cb871-da7e-4a1a-b16e-467c781ab4a3)

This is a Chainlit-based chatbot interface for a pet store application powered by Amazon Bedrock Multi-Agents Collaboration . It integrates with AWS services like bedrock-agent-runtime to provide intelligent responses to user queries.

🚀 Key Features
Interactive Chat Interface : Built with Chainlit .
Amazon Bedrock Integration : Uses bedrock-agent-runtime for orchestrating multi-agent workflows.
Session Management : Tracks conversation history and session IDs.
Structured Logging : Detailed logs for debugging and tracing agent interactions.
AWS SDK (Boto3) : Securely connects to AWS services for backend operations.
📦 Installation
Install Dependencies
bash


1
pip install chainlit boto3
AWS Configuration
Ensure your AWS credentials are configured:
bash


1
aws configure
Set the correct region (default: us-west-2).
Replace the agent ID (26G13YHBTH) and alias ID (KMNFWHMJDN) in invokeAgent() with your Bedrock agent details.
▶️ Usage
Run the Application
bash


1
chainlit run app.py
Access the Chat Interface
Open your browser at http://localhost:8000 and interact with the chatbot.
🧠 Code Structure
1. Core Components
AWS Clients :
boto3.Session for AWS service access.
bedrock_agent_runtime_client for invoking Bedrock agents.
invokeAgent() Function :
Sends user queries to the Bedrock agent.
Processes streaming responses (chunk events) and traces.
Chainlit Event Handlers :
@cl.on_chat_start: Initializes session state and displays headers.
@cl.on_message: Handles user input and agent responses.
@cl.on_stop: Displays a footer after the conversation ends.
2. Session Management
Uses cl.user_session to store chat history and session IDs.
3. Logging
Logs agent responses and traces for debugging.
🧩 Configuration
Agent IDs : Update agentId and agentAliasId in invokeAgent() with your Bedrock agent details.
Region : Modify the AWS region (us-west-2) if needed.
