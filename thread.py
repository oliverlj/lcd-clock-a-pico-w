import machine, time, _thread

led = machine.Pin(25, machine.Pin.OUT)

class Thread():
    state = -1 # 1=Running, 0=Stopping, -1=Ended
    def start(func):
        Thread.stop()
        Thread.state = 1
        _thread.start_new_thread(func, ( ))
    def stop():
        if Thread.state > 0:
            Thread.state = 0
        while Thread.state >= 0:
            pass
    def running():
        return Thread.state > 0
    def finished():
        Thread.state = -1
        
def Core1():
    while Thread.running():
        led.toggle()
        time.sleep(0.25)
    led.off()
    Thread.finished()
        
Thread.start(Core1)
time.sleep(5)
Thread.stop()
