import os
from threading import Thread
import time

class FileWatcher(Thread):
    '''
    Class that monitors a file and sends out a callback whren the file changes
    '''

    def __init__(self, path, callback, pollIntervalMs=500):
        Thread.__init__(self)

        self.setName(os.path.basename(__file__) + ':' + os.path.basename(path))

        self._path = path

        self._callback = callback

        self._pollIntervaSec = pollIntervalMs / 1000.0

        self._running = True

    def stop(self):
        self._running = False
        self.join()

    def run(self):
        prevTime = None

        fileExists = True

        while self._running:
            fileExists = os.path.exists(self._path)

            if fileExists:
                currTime = os.stat(self._path).st_mtime

                if prevTime and currTime != prevTime:
                    self._callback(self._path)

                prevTime = currTime

            time.sleep(self._pollIntervaSec)
