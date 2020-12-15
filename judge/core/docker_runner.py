from threading import Thread
import subprocess
import os

from random import randint
from uuid import uuid4

class DockerThread(Thread):

    def __init__(self, future, execution_config):
        seed = uuid4()
        super().__init__(
            name=f'judge_{seed}'
        )

        mapping = f'-v {os.path.abspath(".")}:/app/tests'
        self.container_name = f'--name judge_{seed}'
        envs = self._build_envs(execution_config.environment_configs)
        self.cmd = f'docker run {mapping} {self.container_name} {envs} {execution_config.image_name}'.strip()
        self.future = future


    def _build_envs(self, config_envs):
        envs = ''
        for config_env in config_envs:
            envs += f'-e {config_env.name}={config_env.value}'

        return envs


    def run(self):
        process = subprocess.run(
            self.cmd.split(' '),
            capture_output=True,
            encoding='utf-8'
        )
        response = {
            'status': 'Failed',
            'message': '',
            'err_code': 0
        }
        if process.returncode == 0:
            print('Congratulations!!')
            response['status'] = 'Success'
            response['message'] = 'Congratulations!!'
            del response['err_code']
        else:
            print('try again')
            response['status'] = 'failed'
            if process.returncode == 137:
                print("Your solution took more than expected to run")
                response['err_code'] = 599
                response['message'] = 'you solution took to long to run'
            else:
                response['err_code'] = 400
                response['message'] = 'one or more test did not pass'

        print(f'{self.container_name} finished')
        print(f'{self.container_name}   output: \n\n')
        print(process.stdout)
        print('\n\n')
        print(process.stderr)
        loop = self.future.get_loop()
        loop.call_soon_threadsafe(self.future.set_result, response)
