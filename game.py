import networkx as nx
import numpy as np

class Pathword:
    def __init__(self, fname):
        with open(fname) as f:
            self.words = [w.strip() for w in f.readlines()]

        n_words = len(self.words)
        adj = np.zeros((n_words, n_words))

        for i in range(n_words):
            for j in range(i + 1, n_words):
                if self.are_adjacent(self.words[i], self.words[j]):
                    adj[i, j] = adj[j, i] = 1

        self.graph = nx.from_numpy_matrix(adj)

    def get_path(self, start, end):
        i = self.words.index(start)
        j = self.words.index(end)

        try:
            path = nx.shortest_path(self.graph, i, j)
        except nx.NetworkXNoPath:
            raise ValueError(f'No path between {start} and {end}.')

        return [self.words[k] for k in path]

    def get_valid_pair(self):
        while True:
            i, j = np.random.choice(len(self.words), size=2, replace=False)
            start, end = self.words[i], self.words[j]

            try:
                path = self.get_path(start, end)
            except ValueError:
                continue

            return start, end, path

    def start_new_game(self):
        start, end, path = self.get_valid_pair()

        self.start = start
        self.end = end
        self.path = path

    def validate(self, curr, next):
        if len(next) != 4:
            raise ValueError('You must guess a four-letter word.')

        if not self.are_adjacent(curr, next):
            raise ValueError(
                'Your guess must differ from the last word by one letter.'
            )

        if not next in self.words:
            raise ValueError(f'{next} is not a valid word.')

        return True

    @staticmethod
    def are_adjacent(word1, word2):
        return sum([1 for c1, c2, in zip(word1, word2) if c1 != c2]) == 1
