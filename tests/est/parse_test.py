import pytest

from dumbpm.est.parse import parse_input


def test_parse_input_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        parse_input("tests/est/csvs/mamma.csv")


def test_parse_missing_velocity() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/est/csvs/no_velocity.csv")


def test_parse_missing_one_velocity() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/est/csvs/missing_one_velocity.csv")


def test_parse_negative_velocity() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/est/csvs/negative_velocity.csv")


def test_parse_no_change() -> None:
    csv = parse_input("tests/est/csvs/sprints_no_change.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "velocity",
        "change",
    }
    assert list(csv["change"].values) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def test_parse_missing_one_change() -> None:
    csv = parse_input("tests/est/csvs/missing_one_change.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "velocity",
        "change",
    }
    assert list(csv["change"].values) == [
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        -3.0,
        -2.0,
        5.0,
        0.0,
        2.0,
        -4.0,
    ]


def test_parse_input() -> None:
    csv = parse_input("tests/est/csvs/sprints.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "velocity",
        "change",
    }
    assert list(csv["velocity"].values) == [
        17.0,
        19.0,
        10.0,
        12.0,
        21.0,
        7.0,
        15.0,
        12.0,
        12.0,
        14.0,
        18.0,
    ]
    assert list(csv["change"].values) == [
        5.0,
        1.0,
        0.0,
        0.0,
        1.0,
        -3.0,
        -2.0,
        5.0,
        0.0,
        2.0,
        -4.0,
    ]
