import sys

import io
import argparse

from threading import Thread, Event, Lock
from multiprocessing import Queue
import queue
from os import fdopen, path

from . import argparser_wrapper
from . import views
from . import context


class QueuedOut(io.StringIO):
    def __init__(self, name, shared_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.queue = shared_queue

    def write(self, b, *args, **kwargs):
        # flush at newline
        lines = b.split('\n')
        for line in lines[:-1]:
            super().write(line)
            self.flush()
        super().write(lines[-1])

    def flush(self):
        value = self.getvalue()
        if len(value) > 1:
            self.queue.put((self.name, value))
            self.seek(0)
            self.truncate(0)

class FlaskThread(Thread):
    def __init__(self, port, host):
        super().__init__()
        self.port = port
        self.host = host

    def run(self):
        views.app.run(port=self.port, threaded=True, host=self.host)

class OutputThread(Thread):
    def __init__(self, inqueue, restart):
        super().__init__()
        self.queue = inqueue
        self.restart = restart
        self.cache = []
        self.clients = []
        self.sem = Lock()
        self.stopped = False

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.restart.is_set() or self.stopped:
            item = self.queue.get()
            self.cache.append(item)
            self.sem.acquire()
            for i, (outqueue, active) in enumerate(self.clients):
                try:
                    outqueue.put(item, True, 1)
                except queue.Full:
                    self.clients[i] = self.clients[i][0], False
            self.sem.release()

            self.clients = [client for client in self.clients if client[1] == True]

    def add_client(self):
        print("new connection. Current connections: %s" % len(self.clients))
        new_queue = queue.Queue(10)
        self.clients.append((new_queue, True))
        return new_queue


def start_module(name, is_module):
    views.app.restart.clear()
    views.app.name = path.basename(name)
    views.app.desc = ""
    views.app.actions = []
    views.app.queue = Queue()
    ioout = QueuedOut("out", views.app.queue)
    ioerr = QueuedOut("err", views.app.queue)
    views.app.output = OutputThread(views.app.queue, views.app.restart)
    #Output(views.app.queue, views.app.restart)

    views.app.actionQueue = Queue()  # This holds only one Argparser Object
    views.app.namespaceQueue = Queue()  # This hold only one Namespace Object

    argparser = argparser_wrapper.argParserGenerator(views.app.actionQueue, views.app.namespaceQueue)

    views.app.module_process = context.Context(
        "sub",
        name,
        ioout,
        ioerr,
        overwritten_modules={'argparse': argparser},
        is_module = is_module,
        #original_modules = emptymodules
    )
    views.app.module_process.start()
    views.app.output.start()
    views.app.mutex_groups, views.app.actions, name, views.app.desc = views.app.actionQueue.get()
    if name:
        views.app.name = name

    views.app.module_process.join()
    views.app.output.stop()

    ioerr.write("Process stopped ({})\n".format(views.app.module_process.exitcode))
    views.app.restart.wait()


def main():

    parser = argparse.ArgumentParser(description="a Webbased frontend for ARgparse in Python")
    parser.add_argument('--port', '-p', default=5000, help="The port to listen on (default 5000)")
    parser.add_argument('--host', default="0.0.0.0", help="The host to bind to (default 0.0.0.0)")
    parser.add_argument('--module', '-m', action="store_true", help="If set, loads a module instead of a file")
    parser.add_argument('file', help="File to run")
    args = parser.parse_args()

    flask_thread = FlaskThread(args.port, args.host)
    flask_thread.start()

    views.app.restart = Event()
    while True:
        start_module(args.file, args.module)


if __name__ == "__main__":
    main()
