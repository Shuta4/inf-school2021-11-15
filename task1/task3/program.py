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

    def find_parent_turn(self, turn):
        return self.turns[turn.parent]

    def find_child_turns(self, i):
        return [x for x in self.turns if x is not None and x.parent == i]

def print_tp_section(padding, turn, player):
    print(f"{'| ' * padding}|-Turn {turn}, player {player}")

def print_ar_section(padding, turn):
    print(f"{'| ' * padding}|-Action: {turn.i + 1} {turn.action} -> {turn.stones}")
    if turn.is_win:
        print(f"{'| ' * (padding + 1)}|-WIN!")

def main():

    actions = {
        "*": lambda x: x * 2,
        "+": lambda x: x + 2
    }

    for s in range(1, 66):
        game = StonesGame(75, 9, s, 2, 2, actions)

        strategy = {}
        win_counts = 0
        guarantees = 0
        turns = game.find_child_turns(0)
        for turn in turns:

            if turn is None:
                continue
            if turn.is_win:
                break

            children = game.find_child_turns(game.turns.index(turn))
            for child in children:
                if child.is_win:
                    guarantees += 1
                    win_counts += 1
                    strategy[game.turns.index(turn)] = game.turns.index(child)
                    break

                win_counts_2 = 0
                children_2 = game.find_child_turns(game.turns.index(child))
                for child_2 in children_2:
                    if child_2.is_win:
                        break

                    children_3 = game.find_child_turns(game.turns.index(child_2))
                    for child_3 in children_3:
                        if child_3.is_win:
                            index_1 = game.turns.index(turn)
                            index_2 = game.turns.index(child)
                            index_3 = game.turns.index(child_2)
                            index_4 = game.turns.index(child_3)

                            strategy[index_1] = strategy.get(index_1, {})
                            strategy[index_1][index_2] = strategy[index_1].get(index_2, {})
                            strategy[index_1][index_2][index_3] = index_4
                            win_counts_2 += 1
                            break

                if win_counts_2 == len(children_2):
                    win_counts += 1

        if guarantees == len(turns):
            continue

        if win_counts == len(turns):
            print(s)
            print("Strategy:")
            print_tp_section(0, 1, 1)
            for key in strategy:
                print_ar_section(1, game.turns[key])
                print_tp_section(2, 1, 2)
                if isinstance(strategy[key], int):
                    print_ar_section(3, game.turns[strategy[key]])
                else:
                    for key_2 in strategy[key]:
                        print_ar_section(3, game.turns[key_2])
                        print_tp_section(4, 2, 1)
                        for key_3 in strategy[key][key_2]:
                            print_ar_section(5, game.turns[key_3])
                            print_tp_section(6, 2, 2)
                            print_ar_section(7, game.turns[strategy[key][key_2][key_3]])

main()
