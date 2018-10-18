#!/usr/bin/env python3
# coding=UTF-8

"""Provides unit testing for the Boggle solver."""


from boggle import solve


def test_boggle():
    """Checks for twelve known words in a specific board."""
    board = """CATER
XLUAW
BDFGH
IJKMN
OPQST"""

    board2 = """CATERWAULING
ASDFGHJKLZXC
QAZWSXEDCRFV
TGBYHNUJMIKL
OKMIJNUHBYGV
TFCRDXESZWAQ
ASDFGHJKLZXC
QAZWSXEDCRFV
TGBYHNUJMIKL
OKMIJNUHBYGV
TFCRDXESZWAQ
ABABABABABAB"""

    known_words = set(["cat", "cater", "caterwaul", "ate", "tea",
                       "eta", "late", "lute", "later", "wag",
                       "jib", "poi"])
    found_words = set()
    for word in solve(board):
        assert word in known_words
        found_words.add(word)
    assert known_words == found_words
