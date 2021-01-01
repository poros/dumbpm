import subprocess

import pandas.testing
import pytest

from dumbpm.cmd import cmd_estimate
from dumbpm.cmd import cmd_prioritize
from dumbpm.cmd import create_parser
from dumbpm.est import est


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
    args = parser.parse_args(
        ["estimate", "tests/est/csvs/sprints.csv", "100", "--simulations", "10"]
    )
    actual = cmd_estimate(args, random_seed=1234)
    expected = est.compute_stats([6, 7, 8, 8, 8, 7, 9, 8, 6, 7])
    pandas.testing.assert_frame_equal(expected, actual)
    args = parser.parse_args(
        [
            "estimate",
            "tests/est/csvs/sprints.csv",
            "100",
            "--normal",
            "--simulations",
            "10",
        ]
    )
    actual = cmd_estimate(args, random_seed=1234)
    expected = est.compute_stats([6, 7, 8, 8, 8, 7, 9, 8, 6, 7])
    pandas.testing.assert_frame_equal(expected, actual)


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
