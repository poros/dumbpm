import argparse

from dumbpm.parse import parse_input
from dumbpm.prio import prioritize


def cmd(args):
    csv = parse_input(args.filename)
    print(
        prioritize(
            csv["project"],
            csv["cost"],
            csv["value"],
            csv["duration"],
            csv["rigging"],
            args.budget,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A very dumb PM")
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(title="subcommands")
    prio_parser = subparsers.add_parser(
        "prioritize", help="Prioritize projects in a very dumb way"
    )
    prio_parser.add_argument(
        "filename", type=str, help="CSV file with projects definition"
    )
    prio_parser.add_argument(
        "--budget",
        type=float,
        nargs="?",
        default=float("Inf"),
        help="Max budget allowed",
    )
    prio_parser.set_defaults(func=cmd)
    args = parser.parse_args()
    if args.func:
        args.func(args)
    else:
        parser.print_help()
