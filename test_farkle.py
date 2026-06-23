"""Tests for Farkle scoring logic."""

import pytest
from farkle import score_dice, score_of_a_kind, all_valid_subsets


def test_single_ones():
    assert score_dice([1]) == 100
    assert score_dice([1, 1]) == 200

def test_single_fives():
    assert score_dice([5]) == 50
    assert score_dice([5, 5]) == 100

def test_no_score():
    assert score_dice([2]) == 0
    assert score_dice([3, 4, 6]) == 0

def test_three_of_a_kind():
    assert score_dice([2, 2, 2]) == 200
    assert score_dice([3, 3, 3]) == 300
    assert score_dice([4, 4, 4]) == 400
    assert score_dice([5, 5, 5]) == 500
    assert score_dice([6, 6, 6]) == 600
    assert score_dice([1, 1, 1]) == 1000

def test_four_of_a_kind():
    assert score_dice([2, 2, 2, 2]) == 400
    assert score_dice([1, 1, 1, 1]) == 2000

def test_five_of_a_kind():
    assert score_dice([2, 2, 2, 2, 2]) == 800
    assert score_dice([1, 1, 1, 1, 1]) == 4000

def test_six_of_a_kind():
    assert score_dice([2, 2, 2, 2, 2, 2]) == 1600
    assert score_dice([1, 1, 1, 1, 1, 1]) == 8000

def test_straight():
    assert score_dice([1, 2, 3, 4, 5, 6]) == 1500

def test_three_pairs():
    assert score_dice([1, 1, 2, 2, 3, 3]) == 1500
    assert score_dice([4, 4, 5, 5, 6, 6]) == 1500

def test_mixed():
    assert score_dice([1, 5]) == 150
    assert score_dice([1, 1, 5]) == 250

def test_farkle():
    assert score_dice([2, 3, 4, 6]) == 0

def test_valid_subsets_nonempty():
    subsets = all_valid_subsets([1, 2, 3, 4, 5, 6])
    assert len(subsets) > 0

def test_empty_dice():
    assert score_dice([]) == 0
