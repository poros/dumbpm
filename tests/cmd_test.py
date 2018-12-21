import subprocess

import pytest

from dumbpm.cmd import cmd
from dumbpm.cmd import create_parser


def test_create_parser_prioritize() -> None:
    parser = create_parser()
    args = parser.parse_args(["prioritize", "file/path", "--budget", "10"])
    assert args.filename == "file/path"
    assert args.budget == 10.0
    args = parser.parse_args(["prioritize", "file/path"])
    assert args.filename == "file/path"
    assert args.budget == float("Inf")
    with pytest.raises(SystemExit):
        parser.parse_args(["prioritize"])
    parser.parse_args([])


def test_cmd() -> None:
    parser = create_parser()
    args = parser.parse_args(["prioritize", "tests/prio.csv", "--budget", "3"])
    assert cmd(args) == [["C", "Project B"]]
    args = parser.parse_args(["prioritize", "tests/prio.csv"])
    assert cmd(args) == [["C", "Project B", "Project A", "D"]]


def test_main() -> None:
    subprocess.run(["dumbpm"], check=True)
    subprocess.run(
        ["dumbpm", "prioritize", "tests/prio.csv", "--budget", "3"], check=True
    )
