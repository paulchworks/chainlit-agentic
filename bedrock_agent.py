import boto3
import logging
from botocore.exceptions import ClientError
# Set up logging    
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BedrockAgentManager:
    def __init__(self):
        self.agents_runtime_client = boto3.client('bedrock-agent-runtime')

    def invoke_agent(self, agent_id, agent_alias_id, session_id, prompt):
        try:
            response = self.agents_runtime_client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=prompt,
            )

            completion = ""
            for event in response.get("completion", []):
                chunk = event.get("chunk", {})
                if "bytes" in chunk:
                    decoded = chunk["bytes"].decode()
                    completion += decoded
                    yield decoded  # Stream individual chunks

        except ClientError as e:
            logger.error(f"Couldn't invoke agent. {e}")
            raise
