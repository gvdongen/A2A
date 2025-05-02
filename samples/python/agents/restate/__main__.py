"""A an example of serving a resilient agent using restate.dev"""
import os
from fastapi import FastAPI
import httpx

from agent import ReimbursementAgent
import middleware

from common.types import AgentCapabilities, AgentCard, AgentSkill

RESTATE_HOST = os.getenv("RESTATE_HOST", "http://localhost:8080")
AGENT_HOST = os.getenv("AGENT_HOST", "0.0.0.0:9080")

AGENT_CARD = AgentCard(
    name="ReimbursementAgent",
    description="This agent handles the reimbursement process for the employees given the amount and purpose of the reimbursement.",
    url=f"{AGENT_HOST}/process_request",
    version="1.0.0",
    defaultInputModes=ReimbursementAgent.SUPPORTED_CONTENT_TYPES,
    defaultOutputModes=ReimbursementAgent.SUPPORTED_CONTENT_TYPES,
    capabilities=AgentCapabilities(streaming=False),
    skills=[
        AgentSkill(id="process_reimbursement",
                   name="Process Reimbursement Tool",
                   description="Helps with the reimbursement process for users given the amount and purpose of the reimbursement.",
                   tags=["reimbursement"],
                   examples=["Can you reimburse me $20 for my lunch with the clients?"])],
)

app = FastAPI()

@app.get("/.well-known/agent.json")
async def agent_json():
    """server the agent card"""
    return AGENT_CARD.model_dump()

@app.post("/process_request")
async def process_request(request: dict):
    """Forward the request to the agent server for processing"""
    async with httpx.AsyncClient() as client:
        #
        # restate's a2a middleware (see below) automatically creates a restate service (https://docs.restate.dev/concepts/services/)
        # for the agent to drive it's computation durably.
        # The service name is the agent name + "A2AServer" (e.g. ReimbursementAgentA2AServer)
        # And the main handler is "process_request".
        #
        # You can skip this step and call the restate service directly by exposing it at the agent's url card.
        #
        restate_service = f"{AGENT_CARD.name}A2AServer"
        restate_handler = "process_request"
        url = f"{RESTATE_HOST}/{restate_service}/{restate_handler}"
        response = await client.post(url, json=request)
        response.raise_for_status()
        return response.json()

app.mount("/restate/v1", middleware.a2a(AGENT_CARD.name, ReimbursementAgent()))

def main():
    """Serve the agent at port 9080"""
    import asyncio
    import hypercorn
    import hypercorn.asyncio

   
    conf = hypercorn.Config()
    conf.bind = [AGENT_HOST]
    asyncio.run(hypercorn.asyncio.serve(app, conf))

if __name__ == "__main__":
    main()
