import argparse
from typing import Optional

from pandas import DataFrame

from dumbpm import est
from dumbpm import guess
from dumbpm import prio


def cmd_prioritize(args: argparse.Namespace) -> list[str]:
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
        help="Prioritize a list of projects. See README for more info.",
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


def cmd_estimate(
    args: argparse.Namespace, random_seed: Optional[int] = None
) -> DataFrame:
    csv = est.parse_input(args.filename)
    data = est.estimate(
        scope=args.scope,
        velocity=csv["velocity"],
        change=csv["change"],
        normal=args.normal,
        simulations=args.simulations,
        random_seed=random_seed,
    )
    print(f"{data}")
    return data


def cmd_guesstimate(
    args: argparse.Namespace, random_seed: Optional[int] = None
) -> DataFrame:
    csv = guess.parse_input(args.filename)
    data = guess.guesstimate(
        task=csv["task"],
        best=csv["best"],
        expected=csv["expected"],
        worst=csv["worst"],
        simulations=args.simulations,
        random_seed=random_seed,
    )
    print(f"{data}")
    return data


def create_subparser_estimate(subparsers: argparse._SubParsersAction) -> None:
    est_parser = subparsers.add_parser(
        "estimate",
        help="""Estimate projects duration based on historical data.
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

    est_parser.add_argument(
        "--simulations",
        type=int,
        nargs="?",
        default=10000,
        help="Number of simulations to run",
    )

    est_parser.set_defaults(func=cmd_estimate)


def create_subparser_guesstimate(subparsers: argparse._SubParsersAction) -> None:
    guess_parser = subparsers.add_parser(
        "guesstimate",
        help="""Estimate projects duration without historical data.
        See README for more info.""",
    )
    guess_parser.add_argument(
        "filename", type=str, help="CSV file with tasks estimates"
    )

    guess_parser.add_argument(
        "--simulations",
        type=int,
        nargs="?",
        default=10000,
        help="Number of simulations to run",
    )

    guess_parser.set_defaults(func=cmd_guesstimate)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A very dumb PM")
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(title="subcommands")
    create_subparser_prioritize(subparsers)
    create_subparser_estimate(subparsers)
    create_subparser_guesstimate(subparsers)
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
