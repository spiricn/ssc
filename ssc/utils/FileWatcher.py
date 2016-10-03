import os
from threading import Thread, currentThread
import time

class FileWatcher():
    '''
    Class that monitors a file and sends out a callback whren the file changes
    '''

    def __init__(self, path, callback, pollIntervalMs=500):
        self._path = path

        self._callback = callback

        self._pollIntervaSec = pollIntervalMs / 1000.0

        self._running = False

    def stop(self):
        if not self._running:
            raise  RuntimeError('already stopped')

        self._running = False

    def start(self):
        self._thread = Thread(target=self._run,
                              name=os.path.basename(__file__) + ':' + os.path.basename(self._path)
                              )
        self._thread.start()

    def _run(self):
        self._running = True

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
