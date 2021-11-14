#!/usr/bin/python

class State:
    stones = [0, 0]
    turn = 0
    player = 0
    i = 0
    action = ""
    parent = 0
    is_win = False

    def __init__(self, stones, turn, player, i, action, parent, is_win):
        self.stones = stones
        self.turn = turn
        self.player = player
        self.i = i
        self.action = action
        self.parent = parent
        self.is_win = is_win

    def __str__(self):
        return f"{self.parent}: {self.turn}: {self.player}: {self.action}: {self.i}: {self.stones}: {self.is_win}"

class StonesGame:

    # game params
    win_sum = 0
    max_turns = 0
    last_player = 0
    init_stones = [0, 0]
    actions = {}

    turns = []

    def __init__(self, win_sum, s1, s2, depth, last_player, actions):
        self.win_sum = win_sum
        self.init_stones = [s1, s2]
        self.max_turns = depth
        self.last_player = last_player
        self.actions = actions

        self.turns = []
        self.turns.append(None)

        self.play()

    def play(self, parent=0):

        stones = self.init_stones.copy()
        player = 1
        turn = 1

        parent_turn = self.turns[parent]
        if parent_turn is not None:
            stones = parent_turn.stones.copy()
            player = self.get_player(parent_turn.player)
            turn = self.get_turn(parent_turn.turn, player)

        for i in range(len(stones)):
            for action in self.actions:
                c_stones = stones.copy()
                c_stones[i] = self.actions[action](c_stones[i])
                is_win = self.is_win(c_stones)
                self.turns.append(State(c_stones, turn, player, i, action, parent, is_win))
                if is_win or turn >= self.max_turns and player == self.last_player:
                    continue

                self.play(len(self.turns) - 1)

    def get_player(self, player=0):
        if player == 1:
            return 2
        return 1

    def get_turn(self, turn, player):
        if player == 1:
            return turn + 1
        return turn

    def is_win(self, stones):
        if stones[0] + stones[1] >= self.win_sum:
            return True
        return False

    def __str__(self):
        result = ""
        for i in range(len(self.turns)):
            result = f"{result}{i} = ({self.turns[i]})\n"
        return result

def main():

    actions = {
        "*": lambda x: x * 2,
        "+": lambda x: x + 2
    }

    for s in range(1, 66):
        game = StonesGame(75, 9, s, 1, 1, actions)

        for turn in game.turns:
            if turn is None:
                continue

            if turn.is_win:
                print(f"s = {s}, куча {turn.i + 1} {turn.action}")

main()
