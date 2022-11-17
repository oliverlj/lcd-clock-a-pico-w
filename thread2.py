import utime
import _thread

# SLEEP_TIME_MSEC = 1 # hangs in the second test
# SLEEP_TIME_MSEC = 2 # hangs in the second test
# SLEEP_TIME_MSEC = 3 # hangs in first test
# SLEEP_TIME_MSEC = 4 # PASSES both
SLEEP_TIME_MSEC = 5 # hangs in second
# SLEEP_TIME_MSEC = 10 # PASSES both tests
# SLEEP_TIME_MSEC = 11 # hangs in first test
# SLEEP_TIME_MSEC = 20 # PASSES both tests
# SLEEP_TIME_MSEC = 21 # hangs in first
# SLEEP_TIME_MSEC = 22 # hangs in first
# SLEEP_TIME_MSEC = 23 # hangs in first
# SLEEP_TIME_MSEC = 24 # hangs in first
# SLEEP_TIME_MSEC = 25 # PASSES both tests

DISP_PER_SEC = 1
DISP_EVERY = 1000 / SLEEP_TIME_MSEC / DISP_PER_SEC
TEST_LEN = 30

crit_sec_lock:_thread.LockType = _thread.allocate_lock()

def safe_print(*args, **kwargs):
    with crit_sec_lock:
        print(*args, **kwargs)


def run_test(use_ms = True):
    ct = utime.time()
    et = ct + TEST_LEN
    counter = 0

    safe_print('Test starting, using {}'.format('sleep_ms' if use_ms else 'sleep_us'))
    while et > ct:
        if counter % DISP_EVERY == 0:
            safe_print(f'Counter = {counter}')
        if use_ms:
            utime.sleep_ms(SLEEP_TIME_MSEC)
        else:
            utime.sleep_us(SLEEP_TIME_MSEC * 1000)
        counter += 1
        ct = utime.time()

    safe_print('Test passed.')


safe_print('starting test 1')
_thread.start_new_thread(run_test, (), {'use_ms':True})
utime.sleep(TEST_LEN + 2)

safe_print('starting test 2')
_thread.start_new_thread(run_test, (), {'use_ms':False})
utime.sleep(TEST_LEN + 2)

safe_print('All done.')
