# https://microsoft.github.io/autogen/stable//reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.CodeExecutorAgent

from autogen_agentchat.agents import CodeExecutorAgent

def GetCodeExecutorAgent():
    agent = CodeExecutorAgent(
        name="Code Executor Agent",
        description="An agent that executes code and returns the output.",
        system_message="You are a code executor. You will receive code snippets and execute them, returning the output.",
        tools=[],
        max_retries=3,
        retry_delay=1,
    )
    return agent