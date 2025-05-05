"""A an example of serving a resilient agent using restate.dev"""
import os
from fastapi import FastAPI
import httpx
import restate

from agent import ReimbursementAgent
from middleware import AgentMiddleware

from common.types import AgentCapabilities, AgentCard, AgentSkill

RESTATE_HOST = os.getenv("RESTATE_HOST", "http://localhost:8080")
AGENT_HOST = os.getenv("AGENT_HOST", "http://localhost")
AGENT_PORT = os.getenv("AGENT_PORT", "9080")

AGENT_CARD = AgentCard(
    name="ReimbursementAgent",
    description="This agent handles the reimbursement process for the employees given the amount and purpose of the reimbursement.",
    url=f"{AGENT_HOST}:{AGENT_PORT}/process_request",
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

REIMBURSEMENT_AGENT = AgentMiddleware(AGENT_CARD, ReimbursementAgent())

app = FastAPI()

@app.get("/.well-known/agent.json")
async def agent_json():
    """server the agent card"""
    return REIMBURSEMENT_AGENT.agent_card_json()

@app.post("/process_request")
async def process_request(request: dict):
    """Forward the request to the agent server for processing"""
    async with httpx.AsyncClient(base_url=RESTATE_HOST) as client:
        return await REIMBURSEMENT_AGENT.forward_to_restate(client, request)

app.mount("/restate/v1", restate.app(REIMBURSEMENT_AGENT))

def main():
    """Serve the agent at port 9080"""
    import asyncio
    import hypercorn
    import hypercorn.asyncio

    conf = hypercorn.Config()
    conf.bind = [f"0.0.0.0:{AGENT_PORT}"]
    asyncio.run(hypercorn.asyncio.serve(app, conf))

if __name__ == "__main__":
    main()
