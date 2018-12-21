import argparse
from typing import List

from dumbpm.parse import parse_input
from dumbpm.prio import prioritize


def cmd(args: argparse.Namespace) -> List[str]:
    csv = parse_input(args.filename)
    projects = prioritize(
        csv["project"],
        csv["cost"],
        csv["value"],
        csv["duration"],
        csv["rigging"],
        args.budget,
    )
    print(projects)
    return projects


def create_parser() -> argparse.ArgumentParser:
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
    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    if args.func:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()