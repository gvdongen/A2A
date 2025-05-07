## Resilient Agents with Restate

This sample uses [Restate](https://restate.dev/) and the Agent Development Kit (ADK) to create a resilient "Expense Reimbursement" agent that is hosted as an A2A server.

Restate acts as a scalable, resilient task orchestrator that speaks the A2A protocol and gives you:
- **Automatic retries of failed tasks**: for example, LLM API downtime, timeouts, infrastructure failures, etc.
- **Recovery of progress**: Restate preserves progress across failures, recovering exactly where tasks left off without duplicating work.
- **Persistent task handle for long-running tasks**: Restate keeps track of a task's progress across failures, time and processes. Whether tasks execute in milliseconds or months (e.g. human-in-the-loop).
- **Task control**: Restate allows canceling tasks, querying their status, and re-subscribing to ongoing tasks (e.g. when client loses connection).
- **Idempotent task submission**: The Restate A2A server automatically deduplicates requests on task ID. On a retry, the server will attach you to the original request.
- **Long-running Agents with workflow semantics**: implement resilient agentic workflows including human-in-the-loop steps, parallel tool execution, durable session state, and scheduling capabilities.
- **Observability**: Restate provides a web UI to visualize the task progress and status. If you also implement the agent itself with Restate, then you can see the end-to-end task execution log.

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
   
6. Start the Restate Server with Docker ([for other options check the docs](https://docs.restate.dev/develop/local_dev#running-restate-server--cli-locally)).
   
   ```shell
   docker run --name restate_dev --rm -p 8080:8080 -p 9070:9070 -p 9071:9071 \
     --add-host=host.docker.internal:host-gateway docker.restate.dev/restatedev/restate:1.3
   ```
   
   Let Restate know where the A2A server is running:
   ```shell
   docker run -it --network=host docker.restate.dev/restatedev/restate-cli:1.3 \
     deployments register http://host.docker.internal:9080/restate/v1
   ```

5. In a separate terminal, run the A2A client:
    ```
    # Connect to the agent (specify the agent URL with correct port)
    cd sample[README.md](README.md)s/python/hosts/cli
    uv run . --agent http://localhost:9080

    # If you changed the port when starting the agent, use that port instead
    # uv run . --agent http://localhost:YOUR_PORT
    ```

6. Send requests with the A2A client like: `Reimburse my flight of 700 USD`

Open the Restate UI ([http://localhost:9070](http://localhost:9070)) to see the task execution log and the task state.

<img src="https://raw.githubusercontent.com/restatedev/img/refs/heads/main/a2a/journal.png" width="900px" alt="Example of Restate journal view"/>
<img src="https://raw.githubusercontent.com/restatedev/img/refs/heads/main/a2a/state.png" width="900px" alt="Example of Restate state view"/>
