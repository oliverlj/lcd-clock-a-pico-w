#!/usr/bin/env python3
# Combining coroutines running in an asyncio event loop with
# blocking tasks in thread pool and process pool executors.
#
# Based on https://pymotw.com/3/asyncio/executors.html, but this version runs both
# threads and processes at the same time and interleaves them with asyncio coroutines.
#
# All appears to be working.
#

import uasyncio
import concurrent.futures
import logging
import sys
import time


def block_task(prefix, n):
    """A blocking task to be executed in a thread or process executor"""
    log = logging.getLogger(f'{prefix}_blocks({n})')
    log.info('running')
    time.sleep(1.0)
    log.info('done')
    return f'b{n ** 2}'


async def async_task(prefix, n):
    """A coroutine intended to run in the asyncio event loop to verify that it
    works concurrently with the blocking tasks"""
    log = logging.getLogger(f'{prefix}_asyncio({n})')
    for i in range(5):
        log.info(f'running {i}')
        await uasyncio.sleep(0.5)
    log.info('done')
    return f'a{n ** 2}'


async def run_tasks(prefix, executor):
    """Runs blocking tasks in the executor and spawns off a few coroutines to run
    concurrently with the blocking tasks."""
    log = logging.getLogger(f'{prefix}_run_blocking_tasks')
    log.info('starting')

    log.info('creating executor tasks')
    loop = uasyncio.get_event_loop()

    blocking_tasks = [
                         loop.run_in_executor(executor, block_task, prefix, i)
                         for i in range(6)
                     ] + [async_task(prefix, i) for i in range(3)]

    log.info('waiting for executor tasks')
    completed, pending = await uasyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))

    log.info('exiting')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='PID %(process)5s %(threadName)-25s %(name)-25s: %(message)s',
        stream=sys.stderr,
    )

    th_executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    pr_executor = concurrent.futures.ProcessPoolExecutor(max_workers=3)

    event_loop = uasyncio.get_event_loop()
    try:
        w = uasyncio.wait([run_tasks('th', th_executor),
                          run_tasks('pr', pr_executor)
                          ])
        event_loop.run_until_complete(w)
    finally:
        event_loop.close()