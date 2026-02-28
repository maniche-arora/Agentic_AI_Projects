import os
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

from config.constants import WORK_DIR_DOCKER, TIMEOUT_DOCKER, DOCKER_IMAGE


def getDockerCommandLineCodeExecutor():

    # Get absolute path  --updated extra
    work_dir_abs = os.path.abspath(WORK_DIR_DOCKER)
    
    # Create temp directory if it doesn't exist--updated extra
    if not os.path.exists(work_dir_abs):
        os.makedirs(work_dir_abs)

    docker = DockerCommandLineCodeExecutor(
        work_dir=work_dir_abs,
        image=DOCKER_IMAGE,
        timeout=TIMEOUT_DOCKER
    )
    return docker

async def start_docker_container(docker):
    print("Starting Docker container...")   
    await docker.start()
    print("Docker container started.")

async def stop_docker_container(docker):
    print("Stopping Docker container...")   
    await docker.stop()
    print("Docker container stopped.")