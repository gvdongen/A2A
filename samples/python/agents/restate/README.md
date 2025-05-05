## ADK Agent

This sample uses [Restate](https://restate.dev/) and the Agent Development Kit (ADK) to create a simple "Expense Reimbursement" agent that is hosted as an A2A server.

This agent takes text requests from the client and, if any details are missing, returns a webform for the client (or its user) to fill out. 
After the client fills out the form, the agent will complete the task.

## Prerequisites

- Python 3.12 or higher
- [UV](https://docs.astral.sh/uv/)
- Access to an LLM and API Key


## Running the Sample

1. Navigate to the samples directory:
    ```bash
    cd samples/python/agents/restate
    ```
2. Create an environment file with your API key:

   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

4. Run the A2A server and agent:
    ```bash
    uv run .
    ```
   
6. Start the Restate Server with npx or Docker ([for other options check the docs](https://docs.restate.dev/develop/local_dev#running-restate-server--cli-locally)). 

   **Option 1: with npx**
   
   ```shell
   npx @restatedev/restate-server
   ```
   
   Let Restate know where the A2A server is running:
   
   ```shell
   npx @restatedev/restate deployments register http://localhost:9080
   ```
   
   **Option 2: with Docker**
   
   ```shell
   docker run --name restate_dev --rm -p 8080:8080 -p 9070:9070 -p 9071:9071 \
     --add-host=host.docker.internal:host-gateway docker.restate.dev/restatedev/restate:1.3
   ```
   
   Let Restate know where the A2A server is running:
   ```shell
   docker run -it --network=host docker.restate.dev/restatedev/restate-cli:1.3 \
     deployments register http://host.docker.internal:9080
   ```

5. In a separate terminal, run the A2A client:
    ```
    # Connect to the agent (specify the agent URL with correct port)
    cd samples/python/hosts/cli
    uv run . --agent http://localhost:9080

    # If you changed the port when starting the agent, use that port instead
    # uv run . --agent http://localhost:YOUR_PORT
    ```
