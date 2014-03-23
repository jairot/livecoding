import sys
import signal
import pydevd_reload

from threading import Thread
from time import sleep


if len(sys.argv) < 2:
    print "Decime que archivo queres!"
    sys.exit(1)

ctx = {}

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class mainmodule(Thread):

    def __init__(self, ctx):
        Thread.__init__(self)
        self.ctx = ctx

    def run(self):
        while 1:
            sleep(1)
            try:
                oldasync = self.ctx["m"].async.func_code
                pydevd_reload.xreload(self.ctx["m"])
                if self.ctx["m"].async.func_code != oldasync:
                    self.ctx["m"].async()
            except Exception, e:
                print e

if __name__== "__main__":
    runner = mainmodule(ctx)

    m = __import__(sys.argv[1].replace(".py", ""))

    ctx["m"] = m
    runner.start()

    m.main()
