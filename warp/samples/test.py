from argparse import ArgumentParser
import multiprocessing

import time
import sys

def f():
    print("Bla from different Process")


def main():
    print("first")
    print("second")
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a')
    group.add_argument('-b')
    group2 = group.add_mutually_exclusive_group()
    group2.add_argument('-c')
    group2.add_argument('-d')
    group3 = group2.add_mutually_exclusive_group()
    group3.add_argument('-e')
    group3.add_argument('-f')

    args = parser.parse_args()

main()
