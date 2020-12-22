PLAYER1 = 'Player 1'
PLAYER2 = 'Player 2'


def construct_decks(lines):
    decks = []
    deck = None
    for line in lines:
        if not line:
            continue
        if 'Player' in line:
            deck = []
            decks.append(deck)
        else:
            deck.append(int(line))
    return decks


class Game:
    def __init__(self, deck1, deck2):
        self.deck1 = deck1
        self.deck2 = deck2

    def play(self):
        while self.deck1 and self.deck2:
            v1 = self.deck1.pop(0)
            v2 = self.deck2.pop(0)
            if v1 > v2:
                self.deck1.extend([v1, v2])
            else:
                self.deck2.extend([v2, v1])

    def get_score(self):
        score = 0
        winner = self.deck2
        if self.deck1:
            winner = self.deck1
        for i, card in enumerate(winner):
            score += card * (len(winner) - i)
        return score


class RecursiveGame(Game):
    def __init__(self, deck1, deck2):
        super().__init__(deck1, deck2)
        self.history = []
        self.insta_win = False

    def play(self):
        while (self.deck1 and self.deck2) and not self.insta_win:
            winner = self.round()
        return winner

    def _recursive_rule(self):
        if self.deck1 in self.history or self.deck2 in self.history:
            self.insta_win = True
            return PLAYER1
        self.history.append(self.deck1[:])
        self.history.append(self.deck2[:])

    def _start_recursive_game(self, c1, c2):
        if c1 <= len(self.deck1) and c2 <= len(self.deck2):
            rg = RecursiveGame(self.deck1[:c1], self.deck2[:c2])
            return rg.play()

    def round(self):
        winner = self._recursive_rule()
        if winner:
            return winner

        c1, c2 = self.deck1.pop(0), self.deck2.pop(0)

        winner = self._start_recursive_game(c1, c2)
        winner = winner if winner else PLAYER1 if c1 > c2 else PLAYER2

        if winner == PLAYER1:
            self.deck1.extend([c1, c2])
            return PLAYER1
        else:
            self.deck2.extend([c2, c1])
            return PLAYER2


def solve1(puzzle_input):
    game = Game(*construct_decks(puzzle_input))
    game.play()
    return game.get_score()


def solve2(puzzle_input):
    game = RecursiveGame(*construct_decks(puzzle_input))
    game.play()
    return game.get_score()
