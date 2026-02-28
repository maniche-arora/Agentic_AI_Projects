import asyncio
from team.analyzer_gpt import getDataAnalyzerTeam
from config.openai_model_client import get_model_client
from config.docker_utils import getDockerCommandLineCodeExecutor,start_docker_container,stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult



async def main():
    openai_model_client = get_model_client()
    docker = getDockerCommandLineCodeExecutor()

    team = getDataAnalyzerTeam(docker, openai_model_client)

    try:
        task = 'Can you tell me how many rows are in titanic.csv data in your working directory?'

        await start_docker_container(docker)
        
        async for message in team.run_stream(task=task):
            print('='*40)
            if isinstance(message, TextMessage):
                print(f"{message.source} said: {message.content}")
            elif isinstance(message,TaskResult):
                print("Stop Reason: ", message.stop_reason)

    except Exception as e:
        print('Error: ', e)
    finally:
        await stop_docker_container(docker)

if __name__ == "__main__":
    asyncio.run(main())



    

