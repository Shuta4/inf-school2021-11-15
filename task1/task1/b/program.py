#!/usr/bin/python

WIN_SUM = 75
STONES_FIRST = 9
MUL = "*"
MUL_VALUE = 2
ADD = "+"
ADD_VALUE = 2

WINNERS = []

def get_stones(s):
    return [STONES_FIRST, s]

def get_player(player=0):
    if player == 1:
        return 2
    return 1

def get_turn(turn, player):
    if player == 1:
        return turn + 1
    return turn

def make_turn(stones, i, action):
    stones = stones.copy()
    if action == MUL:
        stones[i] *= MUL_VALUE
    if action == ADD:
        stones[i] += ADD_VALUE
    return stones

def check_win(stones):
    if stones[0] + stones[1] >= WIN_SUM:
        return True
    return False

def check_conditions(stones, turn, player, s, actions):
    if turn > 1:
        return True

    if check_win(stones) and player == 2:
        WINNERS.append({
            "stones": stones,
            "turn": turn,
            "player": player,
            "s": s,
            "actions": actions
        })
        return True

    return False

def add_action(actions, turn, player, i, action):
    return [*actions, {
        "turn": turn,
        "player": player,
        "i": i,
        "action": action
    }]

def play(stones, s, actions=[], turn=0, player=0):

    if check_conditions(stones, turn, player, s, actions):
        return

    player = get_player(player)
    turn = get_turn(turn, player)

    play(make_turn(stones, 0, ADD), s, add_action(actions, turn, player, 0, ADD), turn, player)
    play(make_turn(stones, 1, ADD), s, add_action(actions, turn, player, 1, ADD), turn, player)
    play(make_turn(stones, 0, MUL), s, add_action(actions, turn, player, 0, MUL), turn, player)
    play(make_turn(stones, 1, MUL), s, add_action(actions, turn, player, 1, MUL), turn, player)

def main():

    for s in range(1, 66):
        play(get_stones(s), s)

    print(WINNERS[0]["s"])

main()
