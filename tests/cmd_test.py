import subprocess

import pandas.testing
import pytest

from dumbpm.cmd import cmd_estimate
from dumbpm.cmd import cmd_guesstimate
from dumbpm.cmd import cmd_prioritize
from dumbpm.cmd import create_parser
from dumbpm.shared import compute_stats


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
    assert cmd_prioritize(args) == ["Project B", "Project A"]
    args = parser.parse_args(["prioritize", "tests/prio/csvs/no_alt.csv"])
    assert cmd_prioritize(args) == ["C", "Project B", "Project A", "D"]


def test_subparser_estimate() -> None:
    parser = create_parser()
    args = parser.parse_args(
        ["estimate", "file/path", "100", "--normal", "--simulations", "1000"]
    )
    assert args.filename == "file/path"
    assert args.scope == 100
    assert args.normal is True
    assert args.simulations == 1000
    args = parser.parse_args(["estimate", "file/path", "100"])
    assert args.filename == "file/path"
    assert args.scope == 100
    assert args.normal is False
    with pytest.raises(SystemExit):
        parser.parse_args(["estimate", "file/path"])


def test_subparser_guesstimate() -> None:
    parser = create_parser()
    args = parser.parse_args(["guesstimate", "file/path", "--simulations", "1000"])
    assert args.filename == "file/path"
    assert args.simulations == 1000
    with pytest.raises(SystemExit):
        parser.parse_args(["guesstimate"])


def test_cmd_estimate() -> None:
    parser = create_parser()
    args = parser.parse_args(
        ["estimate", "tests/est/csvs/sprints.csv", "100", "--simulations", "10"]
    )
    actual = cmd_estimate(args, random_seed=1234)
    expected = compute_stats([6, 7, 8, 8, 8, 7, 9, 8, 6, 7])
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
    expected = compute_stats([7, 7, 7, 8, 8, 7, 8, 7, 7, 7])
    pandas.testing.assert_frame_equal(expected, actual)


def test_cmd_guesstimate() -> None:
    parser = create_parser()
    args = parser.parse_args(
        ["guesstimate", "tests/guess/csvs/tasks.csv", "--simulations", "10"]
    )
    actual = cmd_guesstimate(args, random_seed=1234)
    expected = compute_stats([88, 92, 82, 93, 80, 97, 84, 95, 102, 86])
    pandas.testing.assert_frame_equal(expected, actual)


def test_main() -> None:
    subprocess.run(["dumbpm"], check=True)
    subprocess.run(
        [
            "dumbpm",
            "prioritize",
            "tests/prio/csvs/prio.csv",
            "--budget",
            "30",
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
            "--simulations",
            "10000",
        ],
        check=True,
    )
