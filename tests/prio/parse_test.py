import pytest

from dumbpm.prio.parse import parse_input


def test_parse_input_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        parse_input("tests/prio/csvs/mamma.csv")


def test_parse_input_negative() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/negative.csv")


def test_parse_missing_projects() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/no_proj.csv")


def test_parse_duplicate_projects() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/duplicate_proj.csv")


def test_parse_missing_value() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/no_value.csv")


def test_parse_missing_cost() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/no_cost.csv")


def test_parse_missing_one_project() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/missing_one_proj.csv")


def test_parse_missing_one_value() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/missing_one_value.csv")


def test_parse_missing_one_cost() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/missing_one_cost.csv")


def test_parse_no_duration() -> None:
    csv = parse_input("tests/prio/csvs/no_dur.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "risk",
        "pick",
        "alternative",
    }
    assert list(csv["duration"].values) == [0, 0, 0, 0]


def test_parse_missing_one_duration() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/missing_one_dur.csv")


def test_parse_no_risk() -> None:
    csv = parse_input("tests/prio/csvs/no_risk.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "risk",
        "pick",
        "alternative",
    }
    assert list(csv["risk"].values) == [0, 0, 0, 0]


def test_parse_missing_one_risk() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/missing_one_risk.csv")


def test_parse_no_pick() -> None:
    csv = parse_input("tests/prio/csvs/no_pick.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "risk",
        "pick",
        "alternative",
    }
    assert list(csv["pick"].values) == [False, False, False, False]


def test_parse_missing_one_pick() -> None:
    csv = parse_input("tests/prio/csvs/missing_one_pick.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "risk",
        "pick",
        "alternative",
    }
    assert list(csv["pick"].values) == [False, True]


def test_parse_input_pick_no_bool() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/pick_wrong.csv")


def test_parse_no_alternatives() -> None:
    csv = parse_input("tests/prio/csvs/no_alt.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "risk",
        "pick",
        "alternative",
    }
    assert list(csv["alternative"].values) == [(), (), (), ()]


def test_parse_missing_one_alternative() -> None:
    csv = parse_input("tests/prio/csvs/missing_one_alt.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "risk",
        "pick",
        "alternative",
    }
    assert list(csv["alternative"].values) == [("B",), ("A",), ()]


def test_parse_wrong_alternatives() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/wrong_alt.csv")


def test_parse_pick_conflicts_alternatives() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/pick_vs_alts.csv")


def test_parse_asymmetrical_alternatives() -> None:
    with pytest.raises(ValueError):
        parse_input("tests/prio/csvs/asym_alt.csv")


def test_parse_input() -> None:
    csv = parse_input("tests/prio/csvs/prio.csv")
    assert not csv.isnull().values.any()
    assert set(csv.columns) == {
        "project",
        "value",
        "cost",
        "duration",
        "risk",
        "pick",
        "alternative",
    }
    assert list(csv["project"].values) == ["Project A", "Project B", "C", "D"]
    assert list(csv["value"].values) == [0.0, 1.0, 5.0, 0.0]
    assert list(csv["cost"].values) == [4.0, 0.0, 2.0, 2.0]
    assert list(csv["duration"].values) == [2.0, 1.0, 4.0, 6.0]
    assert list(csv["risk"].values) == [5.0, 1.0, 1.0, 1.0]
    assert list(csv["pick"].values) == [True, False, False, True]
    assert list(csv["alternative"].values) == [
        ("Project B",),
        ("Project A", "C"),
        ("Project B",),
        (),
    ]
