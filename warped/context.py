import argparse
import sys
import io
import runpy
from traceback import print_exc
from contextlib import redirect_stdout, redirect_stderr

from multiprocessing import Process

class Context(Process):
    def __init__(self, name, path, stdout, stderr, arguments=[], is_module = False, overwritten_modules={}, original_modules=None):
        super().__init__()
        self.name = name
        self.stdout = stdout
        self.stderr = stderr
        self.path = path
        self.is_module = is_module
        self.arguments = arguments
        self.overwritten_modules = overwritten_modules
        self.original_modules = original_modules

    def run(self):
        if self.arguments is not None:
            sys.argv = [''] + self.arguments
        else:
            sys.argv = ['']
        #if not self.original_modules is None:
        #    sys.modules = self.original_modules
        #    print(sys.modules)
        sys.modules.update(self.overwritten_modules)
        with redirect_stdout(self.stdout):
            with redirect_stderr(self.stderr):
                try:
                    if self.is_module:
                        runpy.run_module(self.path, run_name='__main__')
                    else:
                        runpy.run_path(self.path, run_name='__main__')
                except Exception:
                    print_exc(file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path")
    parser.add_argument("--arguments", '-a',  default=None)
    parser.add_argument("--is-module", "-m", default=False, action="store_true", dest="is_module")
    args = parser.parse_args()

    context = Context("test", args.path, sys.stdout, sys.stderr, None if args.arguments is None else [args.arguments], args.is_module)
    context.start()
