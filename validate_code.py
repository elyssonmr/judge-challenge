import asyncio

from judge.core.models import ExecutionConfig, EnvConfig
from judge.core.docker_runner import DockerThread


def run_test(config):
    future = asyncio.Future()
    thread = DockerThread(future, config)
    thread.start()
    return future


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
