from threading import Thread
import subprocess
import os
from tempfile import mkdtemp

from random import randint
from uuid import uuid4
import shutil

class DockerThread(Thread):

    def __init__(self, future, execution_config):
        seed = uuid4()
        super().__init__(
            name=f'judge_{seed}'
        )
        self.files = execution_config.files
        self.temp_dir = mkdtemp(prefix=str('judge_'))

        mapping = f'-v {self.temp_dir}:/app/test'
        user = f'-u {os.getuid()}'
        self.container_name = f'--name judge_{seed}'
        envs = self._build_envs(execution_config.environment_configs)
        self.cmd = f'docker run --rm {user} {mapping} {self.container_name} {envs} {execution_config.image_name}'.strip()
        print(self.cmd)
        self.future = future


    def _build_envs(self, config_envs):
        envs = ''
        for config_env in config_envs:
            envs += f'-e {config_env.name}={config_env.value}'

        return envs

    def _process_files(self):
        for file_io in self.files:
            file_name = file_io.name.split('/')[-1]
            with open(f'{self.temp_dir}/{file_name}', 'w') as temp_file:
                temp_file.write(file_io.read())

    def run(self):
        loop = self.future.get_loop()
        try:
            self._process_files()
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
            loop.call_soon_threadsafe(self.future.set_result, response)
        except Exception as ex:
            print(ex)
            loop.call_soon_threadsafe(self.future.set_exception, ex)
        finally:
            shutil.rmtree(self.temp_dir)
