import subprocess

import pytest

from dumbpm.cmd import cmd_prioritize
from dumbpm.cmd import create_parser


def test_parser_dumbpm() -> None:
    parser = create_parser()
    parser.parse_args([])  # shows help


def test_subparser_prioritize() -> None:
    parser = create_parser()
    args = parser.parse_args(
        ["prioritize", "file/path", "--budget", "10", "--duration-cost-budget"]
    )
    assert args.filename == "file/path"
    assert args.budget == 10.0
    assert args.duration_cost_budget is True
    args = parser.parse_args(["prioritize", "file/path"])
    assert args.filename == "file/path"
    assert args.budget == float("Inf")
    assert args.duration_cost_budget is False
    with pytest.raises(SystemExit):
        parser.parse_args(["prioritize"])


def test_cmd_prioritize() -> None:
    parser = create_parser()
    args = parser.parse_args(["prioritize", "tests/prio_no_alt.csv", "--budget", "3"])
    assert cmd_prioritize(args) == ["C", "Project B"]
    args = parser.parse_args(
        [
            "prioritize",
            "tests/prio_no_alt.csv",
            "--budget",
            "10",
            "--duration-cost-budget",
        ]
    )
    assert cmd_prioritize(args) == ["C", "Project B"]
    args = parser.parse_args(["prioritize", "tests/prio_no_alt.csv"])
    assert cmd_prioritize(args) == ["C", "Project B", "Project A", "D"]


def test_main() -> None:
    subprocess.run(["dumbpm"], check=True)
    subprocess.run(
        [
            "dumbpm",
            "prioritize",
            "tests/prio.csv",
            "--budget",
            "3",
            "--duration-cost-budget",
        ],
        check=True,
    )
