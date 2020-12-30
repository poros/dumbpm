import argparse
from typing import List

from dumbpm import est
from dumbpm import prio


def cmd_prioritize(args: argparse.Namespace) -> List[str]:
    csv = prio.parse_input(args.filename)
    projects = prio.prioritize(
        projects=csv["project"],
        value=csv["value"],
        cost=csv["cost"],
        duration=csv["duration"],
        risk=csv["risk"],
        rigging=csv["rigging"],
        alternatives=csv["alternative"],
        max_cost=args.budget,
        cost_per_duration=args.cost_per_duration,
    )
    for i, p in enumerate(projects, 1):
        print(f"{i:02d} {p}")
    return projects


def create_subparser_prioritize(subparsers: argparse._SubParsersAction) -> None:
    prio_parser = subparsers.add_parser(
        "prioritize",
        help="Prioritize projects in a very dumb way.  See README for more info.",
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

    prio_parser.add_argument(
        "--cost-per-duration",
        action="store_true",
        help="Cost is to be assumed per unit of duration. Budget = (cost * duration)",
    )

    prio_parser.set_defaults(func=cmd_prioritize)


def cmd_estimate(args: argparse.Namespace) -> List[int]:
    csv = est.parse_input(args.filename)
    data = est.estimate(
        scope=args.scope,
        velocity=csv["velocity"],
        change=csv["change"],
        normal=args.normal,
    )
    print(f"{data}")
    return data


def create_subparser_project_estimate(subparsers: argparse._SubParsersAction) -> None:
    est_parser = subparsers.add_parser(
        "prioritize",
        help="""Estimate projects duration in a reasonably dumb way.
        See README for more info.""",
    )
    est_parser.add_argument(
        "filename", type=str, help="CSV file with velocity and scope change datapoints"
    )

    est_parser.add_argument(
        "scope", type=int, help="Remaining scope in story points for the project"
    )

    est_parser.add_argument(
        "--normal",
        action="store_true",
        help="Use a normal distribution for the input data",
    )

    est_parser.set_defaults(func=cmd_estimate)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A very dumb PM")
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(title="subcommands")
    create_subparser_prioritize(subparsers)
    # create_subparser_project_estimate(subparsers)
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
