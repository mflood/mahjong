import json

import pytest

from mahjong.cli import main

WINNER = ["B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "C5", "C6", "D5", "D5"]
NEARLY = WINNER[:-1]


def test_solve_reports_a_winning_hand(capsys):
    assert main(["solve"] + WINNER) == 0
    out = capsys.readouterr().out

    assert "winning hand" in out
    assert "pair D5 D5" in out


def test_solve_exits_nonzero_for_a_losing_hand(capsys):
    assert main(["solve"] + NEARLY) == 1
    assert "not a winning hand" in capsys.readouterr().out


def test_solve_json_lists_the_melds(capsys):
    assert main(["solve", "--json"] + WINNER) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["winning"] is True
    assert payload["tile_count"] == 14
    assert len(payload["melds"]) == 4
    assert payload["pair"] == ["D5", "D5"]
    assert {m["kind"] for m in payload["melds"]} == {"chow"}


def test_solve_json_for_a_hand_with_no_decomposition(capsys):
    assert main(["solve", "--json", "B1", "C5", "D9", "WE", "WS"]) == 1
    payload = json.loads(capsys.readouterr().out)

    assert payload["winning"] is False
    assert payload["melds"] == []
    assert payload["pair"] is None


def test_solve_explains_a_partial_decomposition(capsys):
    assert main(["solve", "B1", "B2", "B3", "D5", "D5"]) == 1
    out = capsys.readouterr().out

    assert "decomposes, but into 1 melds" in out


def test_waiting_names_the_tile_that_completes(capsys):
    assert main(["waiting"] + NEARLY) == 0
    out = capsys.readouterr().out

    assert "completed by:" in out
    assert "D5" in out


def test_waiting_json_reports_the_shortfall(capsys):
    assert main(["waiting", "--json"] + NEARLY) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["tiles_missing"] == 1
    assert payload["completions"] == [["D5"]]


def test_waiting_on_a_dead_hand_exits_nonzero(capsys):
    dead = ["B1", "B4", "B7", "C1", "C4", "C7", "D1", "D4", "D7", "WE", "WS", "WW", "WN"]
    assert main(["waiting"] + dead) == 1
    assert "nothing completes" in capsys.readouterr().out


def test_deal_produces_the_requested_number_of_tiles(capsys):
    assert main(["deal", "--count", "13", "--seed", "1"]) == 0
    assert len(capsys.readouterr().out.split()) == 13


def test_deal_is_reproducible_with_a_seed(capsys):
    main(["deal", "--seed", "42"])
    first = capsys.readouterr().out
    main(["deal", "--seed", "42"])

    assert capsys.readouterr().out == first


def test_deal_json(capsys):
    assert main(["deal", "--count", "5", "--seed", "3", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert len(payload["tiles"]) == 5


def test_a_bad_tile_code_reports_without_a_traceback(capsys):
    assert main(["solve", "B1", "ZZ"]) == 2
    assert "error:" in capsys.readouterr().err


def test_a_command_is_required():
    with pytest.raises(SystemExit):
        main([])


def test_lowercase_tile_codes_are_accepted(capsys):
    assert main(["solve"] + [c.lower() for c in WINNER]) == 0
    assert "winning hand" in capsys.readouterr().out
