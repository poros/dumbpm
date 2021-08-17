import pytest

from dumbpm.guess.parse import parse_input


def test_parse_input_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        parse_input("tests/guess/csvs/mamma.csv")


def test_parse_missing_task() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/no_task.csv")


def test_parse_missing_best() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/no_best.csv")


def test_parse_missing_expected() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/no_expected.csv")


def test_parse_missing_worst() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/no_worst.csv")


def test_parse_missing_one_task() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/missing_one_task.csv")


def test_parse_missing_one_best() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/missing_one_best.csv")


def test_parse_missing_one_expected() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/missing_one_expected.csv")


def test_parse_missing_one_worst() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/missing_one_worst.csv")


def test_parse_duplicate_task() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/duplicate_task.csv")


def test_parse_negative() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/negative.csv")


def test_parse_non_monotonic() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/guess/csvs/non_monotonic.csv")


def test_parse_milestone() -> None:
    csv = parse_input("tests/guess/csvs/milestones.csv")
    assert list(csv["task"].values) == [
        "Task A",
        "Task B",
        "Task C",
        "Task D",
        "Task E",
        "Task F",
    ]


def test_parse_input() -> None:
    csv = parse_input("tests/guess/csvs/tasks.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "task",
        "best",
        "expected",
        "worst",
    }
    assert list(csv["task"].values) == [
        "Task A",
        "Task B",
        "Task C",
        "Task D",
        "Task E",
        "Task F",
    ]
    assert list(csv["best"].values) == [
        5,
        6,
        1,
        10,
        5,
        12,
    ]
    assert list(csv["expected"].values) == [
        10,
        12,
        13,
        13,
        7,
        25,
    ]
    assert list(csv["worst"].values) == [
        20,
        40,
        24,
        15,
        12,
        34,
    ]
