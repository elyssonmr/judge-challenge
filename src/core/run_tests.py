import asyncio

from docker_runner import DockerThread

def run_test(name):
    future = asyncio.Future()
    thread = DockerThread(future, name)
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
    print('response: ', loop.run_until_complete(run_test('teste')))
    print('Done')
