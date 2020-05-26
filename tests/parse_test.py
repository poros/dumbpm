import pytest

from dumbpm.parse import parse_input


def test_parse_input_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        parse_input("tests/mamma.csv")


def test_parse_input_negative() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/negative.csv")


def test_parse_no_duration() -> None:
    csv = parse_input("tests/prio_no_duration.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "rigging",
        "alternative",
    }
    assert list(csv["duration"].values) == [1, 1, 1, 1]


def test_parse_no_rigging() -> None:
    csv = parse_input("tests/prio_no_rig.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "rigging",
        "alternative",
    }
    assert list(csv["rigging"].values) == [0, 0, 0, 0]


def test_parse_no_alternatives() -> None:
    csv = parse_input("tests/prio_no_alt.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "rigging",
        "alternative",
    }
    assert list(csv["alternative"].values) == [(), (), (), ()]


def test_parse_wrong_alternatives() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio_wrong_alt.csv")


def test_parse_asymmetrical_alternatives() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio_asym_alt.csv")


def test_parse_input() -> None:
    csv = parse_input("tests/prio.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "rigging",
        "alternative",
    }
    assert list(csv["project"].values) == ["Project A", "Project B", "C", "D"]
    assert list(csv["value"].values) == [0.0, 1.0, 5.0, 0.0]
    assert list(csv["cost"].values) == [4.0, 0.0, 2.0, 2.0]
    assert list(csv["duration"].values) == [2.0, 1.0, 4.0, 6.0]
    assert list(csv["rigging"].values) == [9.0, 0.0, 0.0, 5.0]
    assert list(csv["alternative"].values) == [
        ("Project B",),
        ("Project A", "C"),
        ("Project B",),
        (),
    ]
