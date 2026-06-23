#!/usr/bin/env python3
"""Farkle dice game - terminal based, 1 or 2 players."""

import random
from collections import Counter
from itertools import combinations


WINNING_SCORE = 10000


def roll_dice(n):
    return [random.randint(1, 6) for _ in range(n)]


def score_dice(dice):
    """Return the score for a given set of dice (must all be scoring dice)."""
    if not dice:
        return 0
    counts = Counter(dice)
    score = 0

    # Straight 1-2-3-4-5-6
    if len(dice) == 6 and len(counts) == 6:
        return 1500

    # Three pairs
    if len(dice) == 6 and len(counts) == 3 and all(v == 2 for v in counts.values()):
        return 1500

    # Six of a kind
    if len(dice) == 6 and len(counts) == 1:
        val = list(counts.keys())[0]
        return score_of_a_kind(val, 6)

    for val, count in counts.items():
        if count >= 3:
            score += score_of_a_kind(val, count)
        else:
            if val == 1:
                score += count * 100
            elif val == 5:
                score += count * 50

    return score


def score_of_a_kind(val, count):
    base = 1000 if val == 1 else val * 100
    # Three of a kind = base; four = base*2; five = base*4; six = base*8
    multiplier = 2 ** (count - 3)
    return base * multiplier


def all_valid_subsets(dice):
    """Return all non-empty subsets of dice indices that score > 0."""
    valid = []
    indices = list(range(len(dice)))
    for r in range(1, len(dice) + 1):
        for combo in combinations(indices, r):
            subset = [dice[i] for i in combo]
            s = score_dice(subset)
            if s > 0:
                valid.append((list(combo), subset, s))
    return valid


def is_farkle(dice):
    return score_dice(dice) == 0 and not any(
        score_dice([d]) > 0 for d in dice
    ) and not any(
        score_dice(list(combo)) > 0
        for r in range(1, len(dice) + 1)
        for combo in combinations(dice, r)
    )


def display_dice(dice, kept_indices=None):
    kept_indices = kept_indices or []
    parts = []
    for i, d in enumerate(dice):
        marker = "*" if i in kept_indices else " "
        parts.append(f"[{d}]{marker}")
    return "  ".join(parts)


def pick_dice(dice):
    """Interactive selection of scoring dice. Returns (kept_dice, score, remaining_count)."""
    print(f"\n  Rolled: {display_dice(dice)}")
    print(f"         (indices: {' '.join(str(i+1) for i in range(len(dice)))})")

    valid = all_valid_subsets(dice)
    if not valid:
        return None, 0, 0  # Farkle

    kept = []
    kept_indices = []
    remaining = list(range(len(dice)))

    while True:
        current_score = score_dice(kept) if kept else 0
        print(f"\n  Kept so far: {[dice[i] for i in kept_indices]} (score: {current_score})")
        print(f"  Remaining dice: {[dice[i] for i in remaining]}")

        if not remaining:
            print("  All dice kept!")
            break

        print("\n  Enter dice numbers to keep (e.g. '1 3 5'), or 'done' to stop selecting:")
        choice = input("  > ").strip().lower()

        if choice == "done":
            if not kept:
                print("  You must keep at least one scoring die.")
                continue
            break

        try:
            selected = [int(x) - 1 for x in choice.split()]
        except ValueError:
            print("  Invalid input. Enter numbers like: 1 3 5")
            continue

        if any(i not in remaining for i in selected):
            print("  Some of those dice are not available.")
            continue

        candidate = kept + [dice[i] for i in selected]
        s = score_dice(candidate)
        if s == 0:
            print("  That selection scores 0. Choose scoring dice.")
            continue

        kept = candidate
        kept_indices.extend(selected)
        remaining = [i for i in remaining if i not in kept_indices]

        if not remaining:
            break

    final_score = score_dice(kept)
    return kept, final_score, len(remaining)


def player_turn(name, current_total, all_scores):
    """Run a full turn for a player. Returns points earned this turn."""
    turn_score = 0
    dice_count = 6
    on_board = name in all_scores  # Has the player gotten on the board?
    ON_BOARD_MIN = 500

    print(f"\n{'='*50}")
    print(f"  {name}'s turn  |  Total: {current_total}")
    print(f"{'='*50}")

    while True:
        input(f"\n  Press Enter to roll {dice_count} dice...")
        dice = roll_dice(dice_count)
        print(f"\n  Rolled: {display_dice(dice)}")

        # Check for Farkle
        any_valid = any(
            score_dice(list(combo)) > 0
            for r in range(1, len(dice) + 1)
            for combo in combinations(dice, r)
        )
        if not any_valid:
            print(f"\n  *** FARKLE! *** You lose {turn_score} points.")
            return 0

        kept, sel_score, remaining = pick_dice(dice)
        if kept is None:
            print(f"\n  *** FARKLE! *** You lose {turn_score} points.")
            return 0

        turn_score += sel_score
        dice_count = remaining if remaining > 0 else 6
        hot_dice = remaining == 0

        if hot_dice:
            print(f"\n  *** HOT DICE! *** All dice scored — roll all 6 again!")

        print(f"\n  Turn score so far: {turn_score}")

        if not on_board and turn_score < ON_BOARD_MIN:
            print(f"  (Need {ON_BOARD_MIN} to get on the board; you have {turn_score} — keep rolling!)")
            if dice_count == 0:
                dice_count = 6
            continue

        print(f"\n  Options:")
        print(f"    [b] Bank {turn_score} points (total would be {current_total + turn_score})")
        print(f"    [r] Roll {dice_count} remaining dice (risk losing {turn_score})")
        choice = input("  > ").strip().lower()

        if choice == "b":
            if not on_board and turn_score < ON_BOARD_MIN:
                print(f"  You need at least {ON_BOARD_MIN} to get on the board!")
                continue
            print(f"\n  Banked {turn_score} points!")
            return turn_score
        elif choice == "r":
            continue
        else:
            print("  Please enter 'b' to bank or 'r' to roll.")


def game():
    print("\n" + "="*50)
    print("         Welcome to FARKLE!")
    print("="*50)
    print(f"\n  First player to {WINNING_SCORE} points wins.")
    print("  You must score 500+ in a single turn to get on the board.")
    print("  Scoring: 1s=100, 5s=50, three-of-a-kind=face×100 (1s=1000)")
    print("  Straights (1-6) and three pairs = 1500 each")
    print("  Four/five/six of a kind double each time\n")

    while True:
        try:
            num_players = int(input("  How many players? (1 or 2): ").strip())
            if num_players in (1, 2):
                break
        except ValueError:
            pass
        print("  Please enter 1 or 2.")

    players = []
    for i in range(num_players):
        name = input(f"  Player {i+1} name: ").strip() or f"Player {i+1}"
        players.append(name)

    scores = {p: 0 for p in players}
    on_board = {p: False for p in players}
    winner = None

    while not winner:
        for player in players:
            earned = player_turn(player, scores[player], on_board)
            if earned > 0:
                if not on_board[player] and earned >= 500:
                    on_board[player] = True
                    print(f"\n  {player} is now ON THE BOARD!")
                if on_board[player]:
                    scores[player] += earned

            print(f"\n  Scoreboard:")
            for p in players:
                print(f"    {p}: {scores[p]}")

            if scores[player] >= WINNING_SCORE:
                winner = player
                break

    print(f"\n{'='*50}")
    print(f"  *** {winner} WINS with {scores[winner]} points! ***")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    game()
