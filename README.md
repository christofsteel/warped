# WARP - a Webbased frontend for ARgparser in Python

`warp` can be used to execute single Python file and Python modules. It captures
calls to the `argparse` module of Python and renders a web GUI based on the
options and arguments defined. It also displays the output of the program inside
the web GUI and allows you to stop, pause and resume the program, as well as
downloading the output.

## Install

Either get a stable version from PyPI, or install the current version from git

    # Installation from PyPI
    pip install warp

    # Installation from git
    pip install git+https://git.k-fortytwo.de/christofsteel/warp/

## Usage

    warp [-h] [--port PORT] [--host HOST] [--module] file

    a Webbased frontend for ARgparse in Python

    positional arguments:
    file                  File to run

    optional arguments:
    -h, --help            show this help message and exit
    --port PORT, -p PORT  The port to listen on (default 5000)
    --host HOST           The host to bind to (default 0.0.0.0)
    --module, -m          If set, loads a module instead of a file

## Sample

To test the capabilities of `warp` an example module was included. You can run
it like this:

    warp -m warp.samples.hooked

Since `warp` also makes use of the argparse module, `warp` itself can be //warped//.

    warp -m warp.hook

## How does it work?

When `warp` is executed, it starts a flask webserver. The javascript of the 
website reads the `/arguments` resource of the server, where the configuration
of the argparser returned. In a seperate process the given program is executed
using the `runpy` library, redirecting `sys.stdin` and `sys.stdout` to a 
`multiprocessing.Queue`, which can be read by the warp process to display it
via the web GUI.

Additionally, `warp` adds an entry for `argparse` in the `sys.modules` list. Python
looks first looks at this list, everytime a module is imported, to avoid 
importing a module multiple times. This custom `argparse` module behaves similar
to the original `argparse` module. In fact with the exception of the 
`ArgumentParser.parse_args()` method, it works exactly like the original. 
Once the program calls the `parse_args()` method, it blocks and waits for
user interaction via the web GUI. Once the user submits the data, the process
continues.

