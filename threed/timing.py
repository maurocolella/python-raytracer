import atexit
from time import process_time
from functools import reduce

class Timer(object):
    def __init__(self):
        self.line = "-" * 40
        atexit.register(self.endlog)
        print()
        print(self.line)
        self.log("Program Start")
        self.start = process_time()

    def seconds_to_str(self, t):
        return "%d:%02d:%02d.%03d" % \
            reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                    [(t * 1000,), 1000, 60, 60])

    def log(self, s, elapsed=None):
        current = process_time()
        print(self.seconds_to_str(current), '-', s)
        if elapsed:
            print(self.line)
            print("Elapsed Time:", self.seconds_to_str(current - self.start))
        print(self.line)

    def endlog(self):
        print()

    def now(self):
        return self.seconds_to_str(process_time())
