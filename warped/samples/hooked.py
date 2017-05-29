from argparse import ArgumentParser
import multiprocessing

import time
import sys

def f():
    print("Bla from different Process")


def main():
    print("first")
    print("second")
    bla = ArgumentParser()
    group = bla.add_mutually_exclusive_group()
    group.add_argument('--foo', action='store_true')
    group.add_argument('--bar', action='store_false')
    group2 = group.add_mutually_exclusive_group()
    group2.add_argument('--one')
    group2.add_argument('--two')
    group3 = group2.add_mutually_exclusive_group()
    group3.add_argument('--three')
    group3.add_argument('--four')
    bla.add_argument('--test', '-t', help="Blubb", default="Blabla")
    bla.add_argument('--bla', action="store_true", default=True)
    bla.add_argument('--blubb', action="store_true")
    bla.add_argument('-f', action="append")
    bla.add_argument('Numbers', nargs="*", type=int)
    bla.add_argument('-v', action="count", help="Verbosity Level")
    bla.add_argument('--sum', action="store_const", const=sum, default=max, help="blubb")

    sp = bla.add_subparsers()

    blip = sp.add_parser("blip")
    blip.add_argument("-g", nargs="+")
    blue = sp.add_parser("blue")
    blue.add_argument("-g")
    blue.add_argument("-q")
    subsub = blue.add_subparsers()
    sub1 = subsub.add_parser("sub1")
    sub1.add_argument("-X")
    sub2 = subsub.add_parser("sub2")
    sub2.add_argument("-X")
    nocheins = sp.add_parser("nocheins")
    nocheins.add_argument("-q", action="store_true")

    bla.add_argument('last')

    args = bla.parse_args()
    print(args)

    print(args.sum([1,2,3]))
    print(args)
    print("Blabla", flush=True)
    print(__name__)
    bla.print_help()
    print("Testfehler", file=sys.stderr)

    p = multiprocessing.Process(target=f)
    p.start()
    p.join()

    while True:
        time.sleep(1)
        print("Output")

if __name__ == "__main__":
    main()

