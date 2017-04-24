import sys
import io

from threading import Thread, Event
from multiprocessing import Queue

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
    def run(self):
        views.app.run(threaded=True)


def start_module(name):
    views.app.restart.clear()
    views.app.name = ""
    views.app.desc = ""
    views.app.actions = []
    views.app.queue = Queue()
    ioout = QueuedOut("out", views.app.queue)
    ioerr = QueuedOut("err", views.app.queue)

    views.app.actionQueue = Queue()  # This holds only one Argparser Object
    views.app.namespaceQueue = Queue()  # This hold only one Namespace Object

    argparser = argparser_wrapper.argParserGenerator(views.app.actionQueue, views.app.namespaceQueue)

    views.app.module_process = context.Context(
        "sub",
        name,
        ioout,
        ioerr,
        overwritten_modules={'argparse': argparser}
    )
    views.app.module_process.start()
    views.app.module_process.join()

    ioerr.write("Process stopped ({})\n".format(views.app.module_process.exitcode))
    views.app.restart.wait()


def main():
    flask_thread = FlaskThread()
    flask_thread.start()

    views.app.restart = Event()
    while True:
        start_module(sys.argv[1])


if __name__ == "__main__":
    main()
