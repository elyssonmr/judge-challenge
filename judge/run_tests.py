import asyncio

from core.docker_runner import DockerThread
from core.models import ExecutionConfig, EnvConfig

def run_test(config):
    future = asyncio.Future()
    thread = DockerThread(future, config)
    thread.start()
    return future


async def run_multiples_docker(loop):
    futures = []

    for name in ['a', 'b', 'c', 'd', 'e']:
        futures.append(run_test(name))
    
    return await asyncio.gather(*futures)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print('running tests')
    loop.set_debug(True)
    timeout_config = EnvConfig(
        name='TIMEOUT',
        value='10s'
    )
    config = ExecutionConfig(
        image_name='emr.test',
        environment_configs=[timeout_config]
    )
    print('response: ', loop.run_until_complete(run_test(config)))
    print('Done')
