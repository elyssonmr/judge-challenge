import asyncio

import argparse
import sys

from judge.core.models import ExecutionConfig, EnvConfig
from judge.core.docker_runner import DockerThread


def run_test(config):
    future = asyncio.Future()
    thread = DockerThread(future, config)
    thread.start()
    return future


def process_env_config(env_configs):
    configs = []
    for env_config in env_configs:
        splited_config = env_config.split('=')
        configs.append(
            EnvConfig(
                name=splited_config[0],
                value='='.join(splited_config[1:]),
            )
        )

    return configs


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    parser = argparse.ArgumentParser(
        description='Code Validator CLI.\nRuns the test validations in the code files passes as argument'
    )
    parser.add_argument(
        'files',
        action='extend',
        metavar='path/to/file path/to/test',
        nargs='+',
        type=argparse.FileType('r'),
        help='Files and tests files to validate'
    )
    parser.add_argument(
        '-image_name',
        default='judge-challange/simple-python3',
        help='Docker image name'
    )
    parser.add_argument(
        '-ec',
        action='extend',
        metavar='ENV_CONFIG=value',
        nargs='*',
        default=[],
        help='Environment configs to be passed to execution container',
        dest='env_configs'
    )
    args = parser.parse_args()
    if args:
        env_config = process_env_config(args.env_configs)
        config = ExecutionConfig(
            image_name=args.image_name,
            environment_configs=env_config,
            files=args.files
        )
        print('running tests')
        print('response: ', loop.run_until_complete(run_test(config)))
        print('Done')
