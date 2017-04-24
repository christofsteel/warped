import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    first = subparsers.add_parser("first")
    first.add_argument("-f")
    second = subparsers.add_parser("second")
    first.add_argument("-g")

    args = parser.parse_args()

    print("Subparser %s was selected" % args.command)
