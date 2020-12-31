import subprocess

import pytest
from pandas import DataFrame

from dumbpm.cmd import cmd_estimate
from dumbpm.cmd import cmd_prioritize
from dumbpm.cmd import create_parser


def test_parser_dumbpm() -> None:
    parser = create_parser()
    parser.parse_args([])  # shows help


def test_subparser_prioritize() -> None:
    parser = create_parser()
    args = parser.parse_args(
        ["prioritize", "file/path", "--budget", "10", "--cost-per-duration"]
    )
    assert args.filename == "file/path"
    assert args.budget == 10.0
    assert args.cost_per_duration is True
    args = parser.parse_args(["prioritize", "file/path"])
    assert args.filename == "file/path"
    assert args.budget == float("Inf")
    assert args.cost_per_duration is False
    with pytest.raises(SystemExit):
        parser.parse_args(["prioritize"])


def test_cmd_prioritize() -> None:
    parser = create_parser()
    args = parser.parse_args(
        ["prioritize", "tests/prio/csvs/no_alt.csv", "--budget", "3"]
    )
    assert cmd_prioritize(args) == ["C", "Project B"]
    args = parser.parse_args(
        [
            "prioritize",
            "tests/prio/csvs/no_alt.csv",
            "--budget",
            "10",
            "--cost-per-duration",
        ]
    )
    assert cmd_prioritize(args) == ["Project A", "Project B"]
    args = parser.parse_args(["prioritize", "tests/prio/csvs/no_alt.csv"])
    assert cmd_prioritize(args) == ["Project A", "C", "D", "Project B"]


def test_subparser_estimate() -> None:
    parser = create_parser()
    args = parser.parse_args(["estimate", "file/path", "100", "--normal"])
    assert args.filename == "file/path"
    assert args.scope == 100
    assert args.normal is True
    args = parser.parse_args(["estimate", "file/path", "100"])
    assert args.filename == "file/path"
    assert args.scope == 100
    assert args.normal is False
    with pytest.raises(SystemExit):
        parser.parse_args(["estimate", "file/path"])


def test_cmd_estimate() -> None:
    parser = create_parser()
    args = parser.parse_args(["estimate", "tests/est/csvs/est.csv", "100"])
    assert cmd_estimate(args) == DataFrame()
    args = parser.parse_args(["estimate", "tests/est/csvs/est.csv", "100", "--normal"])
    assert cmd_estimate(args) == DataFrame()


def test_main() -> None:
    subprocess.run(["dumbpm"], check=True)
    subprocess.run(
        [
            "dumbpm",
            "prioritize",
            "tests/prio/csvs/prio.csv",
            "--budget",
            "3",
            "--cost-per-duration",
        ],
        check=True,
    )
    subprocess.run(
        [
            "dumbpm",
            "estimate",
            "tests/est/csvs/sprints.csv",
            "100",
            "--normal",
        ],
        check=True,
    )
