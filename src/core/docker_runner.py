from threading import Thread
import subprocess
import os

from random import randint

class DockerThread(Thread):

    def __init__(self, future, execution_config):
        super().__init__(
            name=f'elysson_test{name}'
        )
        container_img = 'emr.test'
        mapping = f'-v {os.path.abspath(".")}:/app/tests'
        self.container_name = f'--name teste_{name}'
        timeout = f'-e TIMEOUT={randint(10, 20)}s'
        self.cmd = f'docker run --rm {mapping} {self.container_name} {timeout} {container_img}'
        self.future = future


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
        #print(f'{self.container_name}   output: \n\n')
        #print(process.stdout)
        #print('\n\n')
        #print(process.stderr)
        loop = self.future.get_loop()
        loop.call_soon_threadsafe(self.future.set_result, response)
